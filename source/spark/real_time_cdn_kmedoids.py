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

    schema =StructType([StructField("timestamp",TimestampType()),
                       StructField("channel_id",IntegerType()),
    StructField("host_id",IntegerType()),
    StructField("content_type",IntegerType()),
    StructField("protocol",IntegerType()),
    StructField("content_id",IntegerType()),
    StructField("geo_location",IntegerType()),
    StructField("user_id",IntegerType())])

    json_df = string_df.withColumn("jsonData", from_json(col("value"), schema)).select("jsondata.*")

    # Print out the dataframe schema
    features=['channel_id','host_id', 'content_type', 'protocol', 'geo_location', 'user_id']
    for col_name in features:
        json_df = json_df.withColumn(col_name, col(col_name).cast('int'))
    
    
    
    def predict(row):
        features=['channel_id','host_id', 'content_type', 'protocol','content_id', 'geo_location', 'user_id']
        model=joblib.load("models/kmedoids.pickle")
        
        d = json.loads(row)
        p = pd.DataFrame.from_dict(d, orient = "index").transpose()
        p = p.replace(r'^\s*$', np.NaN, regex=True)
        p=p.fillna(-1)
        p[features]=p[features].astype(float)
        gower_mat = gower.gower_matrix(p,  cat_features = [True,True ,True,True, True,True,True])
        preds=model.fit_predict(gower_mat)
        p["pred"]=np.array(preds)
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