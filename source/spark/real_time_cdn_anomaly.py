from pyspark.sql.session import SparkSession
from pyspark.sql.functions import col, from_json,udf
from pyspark.sql.types import StructType, StructField, StringType, TimestampType, FloatType,IntegerType
import pandas as pd
import numpy as np
import json
import joblib
import hdbscan

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
        model_hdbscan = joblib.load("models/hdbscan.pickle")
        encoder=joblib.load("processing_obj/ohe.pickle")
        
        d = json.loads(row)
        print(d)
        p = pd.DataFrame.from_dict(d, orient = "index").transpose()
        p = p.replace(r'^\s*$', np.NaN, regex=True)
        p=p.fillna(-1)
        p[features]=p[features].astype(float)
        #pred_1=model_svm.predict(p[features].astype(float))
        pred_1=model_svm.predict(encoder.transform(p[features]))
        pred_2=model_iforest.predict(p[features])
        #pred_3 = hdbscan.approximate_predict(model_hdbscan, p[features])[0][0].astype(float)
        pred_3, _ = hdbscan.approximate_predict(model_hdbscan, p[features])
        print(p)

        preds=[]
        for p_1,p_2,p_3 in zip(pred_1,pred_2,pred_3):
            if p_1==-1 and p_2==-1 and p_3==-1:
                preds.append(1)
            else: 
                preds.append(0)
        
        p["pred"]=np.array(preds)
        if preds[0]==0:
            tag="Normal"
        else:
            tag="Anomaly"
        result = {'sample_id':d['sample_id'],'prediction_timestamp': d['timestamp'], 'prediction': preds[0],"tag":tag,"pipeline_type":"Consensus_Model"}
        print(result)
        return str(json.dumps(result))
    
    
    score_udf = udf(predict, StringType())    
    df_prediction = string_df.select(score_udf("value").alias("value"))
    df_prediction.writeStream.format("kafka").outputMode("append").option("kafka.bootstrap.servers", "localhost:9092") \
  .option("topic", "cdn_result") \
  .option("checkpointLocation", "checkpoints").start().awaitTermination()
  
  # Schemas CDN*json
