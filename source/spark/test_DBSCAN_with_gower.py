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
    df_dbscan = pd.read_csv(test_data)
    df_dbscan = df_dbscan.drop(columns=['timestamp', 'content_id']).fillna(df_dbscan.drop(columns=['timestamp', 'content_id']).mean())
    data=df_dbscan[:10000]
    gower_mat = gower.gower_matrix(data,  cat_features = [True,True ,True,True, True,True,True,True])
    model_4 = DBSCAN(min_samples=5, eps=0.3,metric = "precomputed").fit(gower_mat)
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
    
    df=spark.read.csv("../data/test_cdn.csv",mode="DROPMALFORMED",schema=schema)
    pd_df=df.toPandas()
    pd_df=pd_df.fillna(-1)
    
    features=['channel_id','host_id', 'content_type', 'protocol','content_id', 'geo_location', 'user_id']

    dbscan_prediction("../data/test_cdn.csv")
    model_dbscan_with_gower = joblib.load("models/dbscan_with_gower.pickle")

    pred_4=model_dbscan.labels_

    
    data["pred"]=np.array(pred_4)
    
    sparkDF=spark.createDataFrame(data)
    sparkDF.printSchema()
    sparkDF.show()
    #sparkDF.filter(sparkDF.pred == 1).show()
    