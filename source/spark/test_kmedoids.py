import joblib
import numpy as np 
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType, StructType,StructField,TimestampType
from joblib import dump
import gower
from sklearn_extra.cluster import KMedoids




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
    
    features=['channel_id','host_id', 'content_type', 'protocol','content_id', 'geo_location', 'user_id']
    model_kmedoids = joblib.load("models/kmedoids.pickle")
    data=pd_df[:5000]
    gower_mat = gower.gower_matrix(data[features],  cat_features = [True,True ,True,True, True,True,True])
    pred_5 = model_kmedoids.fit_predict(gower_mat) 
    pd_df["pred"]=np.array(pred_5)
    
    sparkDF=spark.createDataFrame(data)
    sparkDF.printSchema()
    sparkDF.show()
    #sparkDF.filter(sparkDF.pred == 1).show()
    