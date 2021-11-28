import numpy as np 
import pandas as pd 
from sklearn.svm import OneClassSVM
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import OneHotEncoder
from sklearn.cluster import KMeans
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType,StructField,StringType,TimestampType,FloatType
from pyspark.ml.feature import VectorAssembler
from pyspark.ml import Pipeline
from joblib import dump




if __name__=="__main__":
    
    
    spark =SparkSession.builder.appName("Create KMeans One Hot Encoding").getOrCreate()
    
    
    clustering_features=['channel_id','host_id', 'content_type', 'protocol','content_id', 'geo_location', 'user_id']
    
    df_train=pd.read_csv("../data/train_cdn.csv")
    df_train=df_train.fillna(-1)
    encoder=OneHotEncoder()
    df_train_ohe=encoder.fit_transform(df_train.iloc[:1000])
    
    model_1=KMeans(7)
    
    model_1.fit(df_train_ohe)

    model_1_path_name="models/kmeans.pickle"
    encoder_path_name="processing_obj/ohe.pickle"
    
    dump(model_1,model_1_path_name)
    
    dump(encoder,encoder_path_name)



    