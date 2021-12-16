from pyspark.sql.session import SparkSession
from pyspark.sql.functions import explode, split, col, from_json,udf
from pyspark.sql.types import StructType, StructField, StringType, TimestampType, FloatType,IntegerType
import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
import json
import joblib

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

    

    
    def predict(row):
        features=['channel_id','host_id', 'content_type', 'protocol', 'geo_location', 'user_id']
        model_svm=joblib.load("models/svm.pickle")
        model_iforest=joblib.load("models/iforest.pickle")
        df_train_dbscan=pd.read_csv("./data/train_cdn.csv").iloc[:1000]
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
        if preds[0]==0:
            tag="Normal"
        else:
            tag="Anomaly"
        result = {'sample_id':d['sample_id'],'prediction_timestamp': d['timestamp'], 'prediction': preds[0],"tag":tag,"pipeline_type":"Consensus_With_DBSCAN"}
        print(result)
        return str(json.dumps(result))
    
    
    score_udf = udf(predict, StringType())    
    df_prediction = string_df.select(score_udf("value").alias("value"))
    df_prediction.writeStream.format("kafka").outputMode("append").option("kafka.bootstrap.servers", "localhost:9092") \
  .option("topic", "cdn_result") \
  .option("checkpointLocation", "checkpoints").start().awaitTermination()
  
  
  
  # Schemas CDN*json
