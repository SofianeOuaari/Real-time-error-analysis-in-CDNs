import numpy as np 
import pandas as pd 
from sklearn.svm import OneClassSVM
from sklearn.ensemble import IsolationForest 
from sklearn.cluster import DBSCAN
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType,StructField,StringType,TimestampType,FloatType
from pyspark.ml.clustering import KMeans
from pyspark.ml.feature import VectorAssembler
from pyspark.ml import Pipeline
from joblib import dump




if __name__=="__main__":
    
    model_1=OneClassSVM()
    model_2= IsolationForest()
    #model_3=DBSCAN()
    
    spark =SparkSession.builder.appName("Create Ensemble Anomaly Detector").getOrCreate()
    
    
    clustering_features=['channel_id','host_id', 'content_type', 'protocol','content_id', 'geo_location', 'user_id']
    
    df_train=pd.read_csv("../data/train_cdn.csv")
    df_train=df_train.fillna(-1)
    model_1.fit(df_train[clustering_features].iloc[:1000])
    model_2.fit(df_train[clustering_features].iloc[:1000])
    model_1_path_name="models/svm.pickle"
    model_2_path_name="models/iforest.pickle"
    
    dump(model_1,model_1_path_name)
    dump(model_2,model_2_path_name)
    
    



    