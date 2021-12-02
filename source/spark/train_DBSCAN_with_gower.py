import numpy as np 
import pandas as pd 
from sklearn.cluster import DBSCAN
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType,StructField,TimestampType,IntegerType
from joblib import dump
import gower





if __name__=="__main__":
    
    
    spark =SparkSession.builder.appName("Create DBSCAN with gower").getOrCreate()

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
    model_4 = DBSCAN(n_jobs=-1,eps=0.2,min_samples=50,metric = "precomputed").fit(gower_mat)
    
    model_4_path_name="models/dbscan_with_gower.pickle"
    dump(model_4,model_4_path_name)    