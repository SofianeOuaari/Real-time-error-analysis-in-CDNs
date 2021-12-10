from pyspark.sql import SparkSession
from pyspark.sql.types import StructType,StructField,StringType,TimestampType,FloatType
from pyspark.ml.clustering import KMeans
from pyspark.ml.feature import VectorAssembler
from pyspark.ml import Pipeline



if __name__=="__main__":
    #Accelerometer1RMS,Accelerometer2RMS,Current,Pressure,Temperature,Thermocouple,Voltage,Volume Flow RateRMS,anomaly,changepoint
    spark =SparkSession.builder.appName("Create K Means Model").getOrCreate()

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


    '''df=spark.read.csv("train.csv").option("header", value = True)\
        .option("delimiter", ",")\
        .schema(schema)'''

    df=spark.read.csv("./data/train.csv",mode="DROPMALFORMED",schema=schema)

    columns_to_drop = ['anomaly', 'changepoint']
    df = df.drop(*columns_to_drop)

    print(df.printSchema())
    print(df.show(50))

    cols = ("accelo1rms", "accelo2rms","current","pressure","temperature","thermocouple","voltage","volumeflow")
    assembler = VectorAssembler().setInputCols(cols).setOutputCol("features")
    
    featureDf = assembler.transform(df)
    print(featureDf)
    kmeans=KMeans().setK(5).setFeaturesCol("features").setPredictionCol("predictions")
    
    kmeansModel=kmeans.fit(featureDf)
    clusters=kmeansModel.clusterCenters()

    #kmeansModel.write.overwrite().save("python_code_samples/kmean_model")
    kmeansModel.save("models/kmean_model")

    for cluster in clusters: 
        print(cluster)
