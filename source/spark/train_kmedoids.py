from pyspark.sql import SparkSession
from pyspark.sql.types import StructType,StructField,TimestampType,IntegerType
from joblib import dump
import gower
from sklearn_extra.cluster import KMedoids






if __name__=="__main__":
    
    
    spark =SparkSession.builder.appName("Create Kmedoids with gower").getOrCreate()

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
    data=df_train[:10000]
    gower_mat = gower.gower_matrix(data,  cat_features = [True,False,True ,True,True, True,True,True])
    model_5 = KMedoids(n_clusters = 6, random_state = 0, metric = 'precomputed', method = 'pam', init =  'k-medoids++').fit(gower_mat)
    
    model_5_path_name="models/kmedoids.pickle"
    dump(model_5,model_5_path_name)    