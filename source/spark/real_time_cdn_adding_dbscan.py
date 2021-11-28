import pyspark
from pyspark.sql.session import SparkSession
from pyspark.sql.functions import explode, split, col, from_json,udf
from pyspark.sql.types import StructType, StructField, StringType, TimestampType, FloatType,IntegerType
from pyspark.ml.clustering import KMeansModel
from pyspark.ml.feature import VectorAssembler
import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
import json
import joblib
import time
import uuid

if __name__ == "__main__":
    spark = SparkSession \
        .builder \
        .appName("Csv_Reader").getOrCreate()

    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "cdn_data") \
        .option("startingOffsets", "earliest") \
        .load()

    print(df)
    string_df = df.selectExpr("CAST(value AS STRING)")
    print(string_df)

    schema =StructType([StructField("timestamp",TimestampType()),
                       StructField("channel_id",IntegerType()),
    StructField("host_id",IntegerType()),
    StructField("content_type",IntegerType()),
    StructField("protocol",IntegerType()),
    StructField("content_id",IntegerType()),
    StructField("geo_location",IntegerType()),
    StructField("user_id",IntegerType())])

    json_df = string_df.withColumn("jsonData", from_json(col("value"), schema)).select("jsondata.*")
    
    df_train_dbscan=pd.read_csv("../data/train_cdn.csv").iloc[:1000]

    # Print out the dataframe schema
    features=['channel_id','host_id', 'content_type', 'protocol','content_id', 'geo_location', 'user_id']
    for col_name in features:
        json_df = json_df.withColumn(col_name, col(col_name).cast('int'))

    
    def predict(row,df_train_dbscan):
        features=['channel_id','host_id', 'content_type', 'protocol','content_id', 'geo_location', 'user_id']
        model_svm=joblib.load("models/svm.pickle")
        model_iforest=joblib.load("models/iforest.pickle")
        df_train_dbscan_fea=df_train_dbscan[features].fillna(-1)
        model_dbscan=DBSCAN()
        
        
        
        d = json.loads(row)
        p = pd.DataFrame.from_dict(d, orient = "index").transpose()
        p = p.replace(r'^\s*$', np.NaN, regex=True)
        p=p.fillna(-1)
        p[features]=p[features].astype(float)
        pred_1=model_svm.predict(p[features].astype(float))
        pred_2=model_iforest.predict(p[features]).astype(float)
        df_dbscan_one_hot=pd.get_dummies(pd.concat[df_train_dbscan_fea,p[features]])
        pred_dbscan=model_dbscan.fit_predict(df_dbscan_one_hot)
        preds=[]
        for p_1,p_2 in zip(pred_1,pred_2):
            if p_1==-1 and p_2==-1 and pred_dbscan[-1]==-1: 
                preds.append(1)
            else: 
                preds.append(0)
        
        p["pred"]=np.array(preds)
        #result = {'prediction_ID':uuid.uuid4().int & (1<<64)-1,'prediction_timestamp': d['timestamp'], 'prediction': preds[0]} 
        result = {'prediction_timestamp': d['timestamp'], 'prediction': preds[0]} 
        return str(json.dumps(result))
    
    
    score_udf = udf(predict, StringType())    
    df_prediction = string_df.select(score_udf("value").alias("value"))
        
    schema =StructType([StructField("prediction_timestamp",StringType()),
                       StructField("prediction",IntegerType())])
    df_prediction = df_prediction.withColumn("jsonData", from_json(col("value"), schema)).select("jsondata.*")
        
    df_prediction.selectExpr("prediction_timestamp AS key", "to_json(struct(*)) AS value").writeStream.format("kafka").outputMode("append").option("kafka.bootstrap.servers", "localhost:9092") \
  .option("topic", "cdn_result") \
  .option("checkpointLocation", "checkpoints").start().awaitTermination()
  
  
  # Schemas CDN*json
