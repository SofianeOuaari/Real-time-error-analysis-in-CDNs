import pyspark
from pyspark.sql.session import SparkSession
from pyspark.sql.functions import explode, split, col, from_json
from pyspark.sql.types import StructType, StructField, StringType, TimestampType, FloatType
from pyspark.ml.clustering import KMeansModel
from pyspark.ml.feature import VectorAssembler

if __name__ == "__main__":
    spark = SparkSession \
        .builder \
        .appName("Csv_Reader").getOrCreate()

    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "voltage_data") \
        .option("startingOffsets", "earliest") \
        .load()

    print(df)
    string_df = df.selectExpr("CAST(value AS STRING)")
    print(string_df)

    schema = StructType([StructField("timestamp", StringType()),
                         StructField("accelo1rms", StringType()),
                         StructField("accelo2rms", StringType()),
                         StructField("current", StringType()),
                         StructField("pressure", StringType()),
                         StructField("temperature", StringType()),
                         StructField("thermocouple", StringType()),
                         StructField("voltage", StringType()),
                         StructField("volumeflow", StringType())])

    json_df = string_df.withColumn("jsonData", from_json(col("value"), schema)).select("jsondata.*")

    # Print out the dataframe schema
    numerical_columns = ["accelo1rms", "accelo2rms", "current", "pressure", "temperature", "thermocouple", "voltage", "volumeflow"]
    for col_name in numerical_columns:
        json_df = json_df.withColumn(col_name, col(col_name).cast('float'))

    json_df = json_df.na.drop("any")
    cols = ("accelo1rms", "accelo2rms", "current", "pressure", "temperature", "thermocouple", "voltage", "volumeflow")
    assembler = VectorAssembler().setInputCols(cols).setOutputCol("features")
    featureDf = assembler.transform(json_df)
    print(featureDf)

    kmeansModelLoded = KMeansModel.load("models/kmean_model")
    df_prediction = kmeansModelLoded.transform(featureDf)

    df_prediction = df_prediction.drop(*["features"])
    df_prediction.writeStream.outputMode("append").format("console").option("truncate", "false").start()

    df_prediction.selectExpr("timestamp AS key", "to_json(struct(*)) AS value") \
        .writeStream \
        .format("kafka") \
        .outputMode("append") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("topic", "spark_result") \
        .option("checkpointLocation", "checkpoints") \
        .start() \
        .awaitTermination()
