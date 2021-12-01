import pandas as pd
from sklearn.svm import OneClassSVM
from sklearn.ensemble import IsolationForest 
from sklearn.preprocessing import OneHotEncoder
from sklearn.cluster import DBSCAN
from pyspark.sql import SparkSession
import hdbscan
from joblib import dump




if __name__=="__main__":
    
    model_1 = OneClassSVM()
    model_2 = IsolationForest()
    model_3 = hdbscan.HDBSCAN(metric="hamming", min_samples=2000, cluster_selection_epsilon=0.5, prediction_data=True)
    #model_4=DBSCAN()

    spark =SparkSession.builder.appName("Create Ensemble Anomaly Detector").getOrCreate()
    
    
    clustering_features=['channel_id','host_id', 'content_type', 'protocol','content_id', 'geo_location', 'user_id']
    
    df_train=pd.read_csv("./data/train_cdn.csv")
    df_train=df_train.fillna(-1)
    print("Models training in progress, please wait a few minutes...")
    
    encoder=OneHotEncoder()
    df_train_ohe=encoder.fit_transform(df_train.iloc[:10000])
    
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
    