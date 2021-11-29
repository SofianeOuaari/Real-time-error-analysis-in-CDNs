import numpy as np 
import pandas as pd 
from sklearn.cluster import DBSCAN
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType,StructField,StringType,TimestampType,FloatType
from pyspark.ml import Pipeline
from joblib import dump
import gower





if __name__=="__main__":
    
    
    spark =SparkSession.builder.appName("Create DBSCAN with gower").getOrCreate()
    
    
    clustering_features=['channel_id','host_id', 'content_type', 'protocol','content_id', 'geo_location', 'user_id']
    
    df_train=pd.read_csv("../data/train_cdn.csv")
    df_train=df_train.fillna(-1)
    data=df[:10000]
    gower_mat = gower.gower_matrix(data,  cat_features = [True,True ,True,True, True,True,True])
    model_4 = DBSCAN(eps=0.3,min_samples=5,metric = "precomputed").fit(gower_mat)
    
    model_4_path_name="models/dbscan_with_gower.pickle"
    dump(model_4,model_4_path_name)    