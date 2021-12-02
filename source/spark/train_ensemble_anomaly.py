import pandas as pd
from sklearn.svm import OneClassSVM
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import OneHotEncoder
from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType, StructType,StructField,TimestampType
from joblib import dump
import hdbscan




if __name__=="__main__":
    
    model_1 = OneClassSVM()
    model_2 = IsolationForest(n_jobs=-1)
    model_3 = hdbscan.HDBSCAN(metric="hamming", min_samples=2000, cluster_selection_epsilon=0.5, prediction_data=True)
    #model_4=DBSCAN()

    spark =SparkSession.builder.appName("Create Ensemble Anomaly Detector").getOrCreate()

    schema=StructType([StructField("timestamp",TimestampType()),
                       StructField("channel_id",IntegerType()),
    StructField("host_id",IntegerType()),
    StructField("content_type",IntegerType()),
    StructField("protocol",IntegerType()),
    StructField("content_id",IntegerType()),
    StructField("geo_location",IntegerType()),
    StructField("user_id",IntegerType())])

    clustering_features=['channel_id','host_id', 'content_type', 'protocol', 'geo_location', 'user_id']

    df = spark.read.csv("./data/train_cdn.csv", header="true", schema=schema)
    df_train = df.toPandas().fillna(-1)
    print("Models training in progress, please wait a few minutes...")
    
    encoder=OneHotEncoder(handle_unknown = 'ignore')
    df_train_ohe=encoder.fit_transform(df_train[clustering_features].iloc[:10000])
    
    model_1.fit(df_train_ohe)
    model_2.fit(df_train[clustering_features].iloc[:10000])
    model_3.fit(df_train[clustering_features].iloc[:10000])
    
    
    
    model_1_path_name="models/svm.pickle"
    model_2_path_name="models/iforest.pickle"
    model_3_path_name = "models/hdbscan.pickle"
    encoder_path_name="processing_obj/ohe.pickle"
    
    
    dump(model_1,model_1_path_name)
    dump(model_2,model_2_path_name)
    dump(model_3, model_3_path_name)
    dump(encoder,encoder_path_name)
    spark.stop()