import numpy as np 
import pandas as pd 
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType,StructField,StringType,TimestampType,FloatType
from pyspark.ml import Pipeline
from joblib import dump
import gower
from sklearn_extra.cluster import KMedoids






if __name__=="__main__":
    
    
    spark =SparkSession.builder.appName("Create Kmedoids with gower").getOrCreate()
    
    
    clustering_features=['channel_id','host_id', 'content_type', 'protocol','content_id', 'geo_location', 'user_id']
    
    df_train=pd.read_csv("./data/train_cdn.csv")
    df_train=df_train.fillna(-1)
    data=df_train[:10000]
    gower_mat = gower.gower_matrix(data,  cat_features = [True,False,True ,True,True, True,True,True])
    model_5 = KMedoids(n_clusters = 6, random_state = 0, metric = 'precomputed', method = 'pam', init =  'k-medoids++').fit(gower_mat)
    
    model_5_path_name="models/kmedoids.pickle"
    dump(model_5,model_5_path_name)    