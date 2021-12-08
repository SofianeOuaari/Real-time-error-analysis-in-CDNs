from pyspark.sql.session import SparkSession
from pyspark.sql.functions import explode, split, col, from_json,udf
from pyspark.sql.types import StructType, StructField, StringType, TimestampType,IntegerType
import pandas as pd
import numpy as np
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
        model_kmeans=joblib.load("models/kmeans_7.pickle")
        encoder=joblib.load("processing_obj/ohe.pickle")
        
        d = json.loads(row)
        p = pd.DataFrame.from_dict(d, orient = "index").transpose()
        p = p.replace(r'^\s*$', np.NaN, regex=True)
        p=p.fillna(-1)
        p[features]=p[features].astype(float)
        preds=model_kmeans.predict(encoder.transform(p[features]))
        p["pred"]=np.array(preds)
        #result = {'prediction_ID':uuid.uuid4().int & (1<<64)-1,'prediction_timestamp': d['timestamp'], 'prediction': preds[0]} 
        result = {'prediction_timestamp': d['timestamp'], 'prediction': preds[0]} 
        return str(json.dumps(result))
    
    
    score_udf = udf(predict, StringType())    
    df_prediction = string_df.select(score_udf("value").alias("value"))
    df_prediction.writeStream.format("kafka").outputMode("append").option("kafka.bootstrap.servers", "localhost:9092") \
  .option("topic", "cdn_result") \
  .option("checkpointLocation", "checkpoints").start().awaitTermination()
  
  
  # Schemas CDN*json
