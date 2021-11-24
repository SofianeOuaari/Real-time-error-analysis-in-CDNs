from pyspark.sql import SparkSession
from pyspark.sql.types import StructType,StructField,StringType,TimestampType,FloatType
from pyspark.ml.clustering import KMeansModel
from pyspark.ml.feature import VectorAssembler



if __name__=="__main__":

    spark =SparkSession.builder.appName("Inference K Means Model").getOrCreate()

    schema=StructType([StructField("datetime",TimestampType()),
    StructField("accelo1rms",FloatType()),
    StructField("accelo2rms",FloatType()),
    StructField("current",FloatType()),
    StructField("pressure",FloatType()),
    StructField("temperature",FloatType()),
    StructField("thermocouple",FloatType()),
    StructField("voltage",FloatType()),
    StructField("volumeflow",FloatType()),
    StructField("anomaly",FloatType()),
    StructField("changepoint",FloatType())])

    df=spark.read.csv("python_code_samples/test.csv",mode="DROPMALFORMED",schema=schema)

    columns_to_drop = ['anomaly', 'changepoint']
    df = df.drop(*columns_to_drop)

    print(df.printSchema())
    print(df.show(50))

    cols = ("accelo1rms", "accelo2rms","current","pressure","temperature","thermocouple","voltage","volumeflow")
    assembler = VectorAssembler().setInputCols(cols).setOutputCol("features")
    featureDf = assembler.transform(df)
    print(featureDf)

    kmeansModelLoded = KMeansModel.load("python_code_samples/kmean_model")
    df_prediction=kmeansModelLoded.transform(featureDf)

    print(df_prediction.show(10))



