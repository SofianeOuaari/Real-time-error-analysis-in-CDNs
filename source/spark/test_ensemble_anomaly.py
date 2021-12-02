import joblib
import numpy as np 
import pandas as pd
from sklearn.cluster import DBSCAN
from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType, StructType,StructField,TimestampType
from sklearn.preprocessing import StandardScaler
from joblib import dump
import hdbscan

def dbscan_prediction(df_dbscan):
    model_3_path_name = "models/dbscan.pickle"
    X = StandardScaler().fit_transform(df_dbscan)
    model_3 = DBSCAN(min_samples=1000, eps=1.0).fit(X)
    dump(model_3, model_3_path_name)

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
    
    df=spark.read.csv("./data/test_cdn.csv",schema=schema)
    pd_df=df.toPandas()
    pd_df=pd_df.fillna(-1)
    
    features=['channel_id','host_id', 'content_type', 'protocol','content_id', 'geo_location', 'user_id']

    dbscan_prediction(pd_df[features])
    
    model_svm = joblib.load("models/svm.pickle")
    model_iforest = joblib.load("models/iforest.pickle")
    model_hdbscan = joblib.load("models/hdbscan.pickle")
    model_dbscan = joblib.load("models/dbscan.pickle")
    encoder=joblib.load("processing_obj/ohe.pickle")
    pred_1=model_svm.predict(encoder.transform(pd_df[features]))
    pred_2=model_iforest.predict(pd_df[features])
    pred_3, _ = hdbscan.approximate_predict(model_hdbscan, pd_df[features])
    pred_4=model_dbscan.labels_

    preds=[]
    
    for p_1,p_2,p_3,p_4 in zip(pred_1,pred_2,pred_3, pred_4):
        if p_1==-1 and p_2==-1 and p_3==-1 and p_4==-1:
            preds.append(1)
        else:
            preds.append(0)
    
    pd_df["pred"]=np.array(preds)
    
    sparkDF=spark.createDataFrame(pd_df)
    sparkDF.printSchema()
    sparkDF.show()
    #sparkDF.filter(sparkDF.pred == 0).show()