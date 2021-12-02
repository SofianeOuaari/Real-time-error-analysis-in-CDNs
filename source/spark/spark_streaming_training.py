from pyspark.mllib.clustering import StreamingKMeans
from pyspark.sql.session import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, TimestampType, FloatType,IntegerType
from pyspark.streaming import StreamingContext

def main():
    # Create a local StreamingContext with two working thread and batch interval of 1 second
    spark = SparkSession \
        .builder \
        .appName("Csv_Reader").getOrCreate()

    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "cdn_data") \
        .option("startingOffsets", "earliest") \
        .load()

    ssc = StreamingContext(spark.sparkContext, 1)
    ssc.start()

    print(df)
    string_df = df.selectExpr("CAST(value AS STRING)")
    print(string_df)

    schema =StructType([StructField("timestamp",TimestampType()),
    StructField("channel_id",FloatType()),
    StructField("host_id",FloatType()),
    StructField("content_type",FloatType()),
    StructField("protocol",FloatType()),
    StructField("content_id",FloatType()),
    StructField("geo_location",FloatType()),
    StructField("user_id",FloatType())])

    df_train = spark.read.csv("./data/train_cdn.csv", schema=schema)
    df_test = spark.read.csv("./data/test_cdn.csv", schema=schema)
    df_train = df_train.na.fill(value=-1)
    df_test = df_test.na.fill(value=-1)

    features = ['channel_id', 'host_id', 'content_type', 'protocol', 'geo_location', 'user_id']

    trainingData = df_train[features]
    testingData = df_test[features]

    trainingQueue = [trainingData]
    testingQueue = [testingData]

    trainingStream = ssc.queueStream(trainingQueue)
    testingStream = ssc.queueStream(testingQueue)

    # We create a model with random clusters and specify the number of clusters to find
    model = StreamingKMeans(k=2, decayFactor=1.0).setRandomCenters(3, 1.0, 0)

    # Now register the streams for training and testing and start the job,
    # printing the predicted cluster assignments on new data points as they arrive.
    model.trainOn(trainingStream)

    result = model.predictOnValues(testingStream)
    result.pprint()

    ssc.stop(stopSparkContext=True, stopGraceFully=True)

if __name__ == "__main__":
    main()