from sklearn.preprocessing import OneHotEncoder
from sklearn.cluster import KMeans
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType,StructField,IntegerType,TimestampType
from joblib import dump




if __name__=="__main__":
    
    
    spark =SparkSession.builder.appName("Create KMeans One Hot Encoding").getOrCreate()

    schema = StructType([StructField("timestamp", TimestampType()),
                         StructField("channel_id", IntegerType()),
                         StructField("host_id", IntegerType()),
                         StructField("content_type", IntegerType()),
                         StructField("protocol", IntegerType()),
                         StructField("content_id", IntegerType()),
                         StructField("geo_location", IntegerType()),
                         StructField("user_id", IntegerType())])

    clustering_features = ['channel_id', 'host_id', 'content_type', 'protocol', 'geo_location', 'user_id']

    df = spark.read.csv("./data/train_cdn.csv", header="true", schema=schema)
    df_train = df.toPandas().fillna(-1)
    encoder=OneHotEncoder(handle_unknown = 'ignore')
    df_train_ohe=encoder.fit_transform(df_train[clustering_features].iloc[:10000])
    
    model_1=KMeans(7,n_jobs=-1)
    
    model_1.fit(df_train_ohe)

    model_1_path_name="models/kmeans_7.pickle"
    encoder_path_name="processing_obj/ohe.pickle"
    
    dump(model_1,model_1_path_name)
    
    dump(encoder,encoder_path_name)
    
    



    