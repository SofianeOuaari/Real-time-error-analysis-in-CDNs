#!/usr/bin/env python
from pyspark.ml.clustering import KMeansModel
from pyspark.ml.feature import VectorAssembler
from pyspark.sql.functions import col, from_json
from pyspark.sql.session import SparkSession
from pyspark.sql.types import StructType, StructField, StringType

if __name__ == "__main__":
    spark = SparkSession \
        .builder \
        .appName("Stream_Reader").getOrCreate()

    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "stream-CDN") \
        .option("startingOffsets", "earliest") \
        .load()

    print(df)
    string_df = df.selectExpr("CAST(value AS STRING)")
    print(string_df)

    schema = StructType([StructField("channel_id", StringType()),
                         StructField("timestamp", StringType()),
                         StructField("host_id", StringType()),
                         StructField("content_type", StringType()),
                         StructField("protocol", StringType()),
                         StructField("content_id", StringType()),
                         StructField("geo_location", StringType()),
                         StructField("user_id", StringType())])

    json_df = string_df.withColumn("jsonData", from_json(col("value"), schema)).select("jsondata.*")

    # Print out the dataframa schema
    int_columns = ["channel_id", "host_id", "content_type", "protocol", "geo_location", "user_id"]
    for col_name in int_columns:
        json_df = json_df.withColumn(col_name, col(col_name).cast('int'))

    json_df = json_df.na.drop("any")
    cols = ("channel_id", "host_id", "content_type", "protocol", "geo_location", "user_id")
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
