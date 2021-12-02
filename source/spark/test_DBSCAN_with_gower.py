import joblib
import numpy as np 
import pandas as pd
from sklearn.cluster import DBSCAN
from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType, StructType,StructField,TimestampType
from joblib import dump
import gower


def dbscan_prediction(test_data):
    model_4_path_name = "models/dbscan_with_gower.pickle"
    gower_mat = gower.gower_matrix(test_data, cat_features = [True,True ,True,True, True,True,True])
    model_4 = DBSCAN(min_samples=50, eps=0.2,metric = "precomputed").fit(gower_mat)
    dump(model_4, model_4_path_name)    

if __name__=="__main__":
    spark=SparkSession.builder.appName("Real Anomaly Ensemble Prediction").getOrCreate()
    schema=StructType([StructField("timestamp",TimestampType()),
                       StructField("channel_id",IntegerType()),
    StructField("host_id",IntegerType()),
    StructField("content_type",IntegerType()),
    StructField("protocol",IntegerType()),
    StructField("content_id",IntegerType()),
    StructField("geo_location",IntegerType()),
    StructField("user_id",IntegerType())])
    
    df=spark.read.csv("./data/test_cdn.csv",mode="DROPMALFORMED",schema=schema)
    pd_df=df.toPandas()
    pd_df=pd_df.fillna(-1)
    pd_df=pd_df[:5000]
    features=['channel_id','host_id', 'content_type', 'protocol', 'geo_location', 'user_id']
    dbscan_prediction(pd_df[features])
    model_dbscan_with_gower = joblib.load("models/dbscan_with_gower.pickle")
    pred_4=model_dbscan_with_gower.labels_  
    pd_df["pred"]=np.array(pred_4)
    
    sparkDF=spark.createDataFrame(pd_df)
    sparkDF.printSchema()
    sparkDF.show()
    #sparkDF.filter(sparkDF.pred == 1).show()
    