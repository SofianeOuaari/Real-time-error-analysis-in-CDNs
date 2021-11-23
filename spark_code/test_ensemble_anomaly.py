import joblib
import numpy as np 
import pandas as pd 
from sklearn.svm import OneClassSVM
from sklearn.ensemble import IsolationForest 
from sklearn.cluster import DBSCAN
from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType, StructType,StructField,StringType,TimestampType,FloatType
from pyspark.ml.clustering import KMeans
from pyspark.ml.feature import VectorAssembler
from pyspark.ml import Pipeline
from pyspark.sql.functions import explode, split, col, from_json
from joblib import dump



if __name__=="__main__":
    
    spark=SparkSession.builder.appName("Real Anomaly Ensemble Prediction").getOrCreate()
    model_svm=joblib.load("models/svm.pickle")
    model_iforest=joblib.load("models/iforest.pickle")
    schema=StructType([StructField("timestamp",TimestampType()),
                       StructField("channel_id",IntegerType()),
    StructField("host_id",IntegerType()),
    StructField("content_type",IntegerType()),
    StructField("protocol",IntegerType()),
    StructField("content_id",IntegerType()),
    StructField("geo_location",IntegerType()),
    StructField("user_id",IntegerType())])
    
    df=spark.read.csv("data/test_cdn.csv",mode="DROPMALFORMED",schema=schema)
    pd_df=df.toPandas()
    
    pd_df=pd_df.fillna(-1)
    
    features=['channel_id','host_id', 'content_type', 'protocol','content_id', 'geo_location', 'user_id']

    pred_1=model_svm.predict(pd_df[features])
    pred_2=model_iforest.predict(pd_df[features])
    pred_3=DBSCAN().fit_predict(pd_df[features])
    
    preds=[]
    
    for p_1,p_2,p_3 in zip(pred_1,pred_2,pred_3):
        if p_1==-1 and p_2==-1 and p_3==-1:
            preds.append(1)
        else:
            preds.append(0)
    
    pd_df["pred"]=np.array(preds)
    
    sparkDF=spark.createDataFrame(pd_df)
    print(sparkDF.printSchema())
    print(sparkDF.show())
    
    
    
    
    

    

    
    
    
    