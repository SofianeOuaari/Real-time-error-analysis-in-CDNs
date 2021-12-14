from pyspark.sql.session import SparkSession
from pyspark.sql.functions import col, from_json,udf
from pyspark.sql.types import StructType, StructField, StringType, TimestampType,IntegerType
import gower
import pandas as pd
import numpy as np
import json
import joblib
from sklearn_extra.cluster import KMedoids


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
        features=['channel_id','host_id', 'content_type', 'protocol','geo_location', 'user_id']
        model=joblib.load("models/kmedoids.pickle")
        
        d = json.loads(row)
        p = pd.DataFrame.from_dict(d, orient = "index").transpose()
        p = p.replace(r'^\s*$', np.NaN, regex=True)
        p=p.fillna(-1)
        p[features]=p[features].astype(float)
        gower_mat = gower.gower_matrix(p,  cat_features = [True,True ,True,True, True,True,True])
        preds=model.fit_predict(gower_mat)
        p["pred"]=np.array(preds)
        cluster_number=str(p["pred"][0]+1)
        tag="Cluster_"+cluster_number
        result = {'sample_id':d['sample_id'],'prediction_timestamp': d['timestamp'], 'prediction': preds[0],"tag":tag,"pipeline_type":"KMedoids"}
        print(result)
        return str(json.dumps(result))
    
    
    score_udf = udf(predict, StringType())    
    df_prediction = string_df.select(score_udf("value").alias("value"))
    df_prediction.writeStream.format("kafka").outputMode("append").option("kafka.bootstrap.servers", "localhost:9092") \
  .option("topic", "cdn_result") \
  .option("checkpointLocation", "checkpoints").start().awaitTermination()
  
  
  
  # Schemas CDN*json