# Real-time-error-analysis-in-CDNs



**Technologies Involved**

For this university project related to the "Stream Mining" + "Open-Source Technologies" course, where the main aim is to build a data streaming infrastructure using a stack of technologies to cluster and detect anomalies within the content delivery network data. 

The different technologies used are : Python-Docker-Kafka-Spark. 

## Installing The Python Dependencies: 

        pip install -r requirements.txt

## Creating the Spark Environment 
1. Building the Spark Image
On docker run the command:
        docker build -t voltage_spark -f Dockerfile .
The Dockerfile contains all the necessary instructions to build and assemble an image which contains spark (and its Python variant pyspark) and run containers as an instance of this image. 
The Dockerfile will first create a Ubuntu environment, then install Python (we used python-slim since it gives a faster installation than the default Alpine Linux distribution) and Java (JRE is necessary for spark to run) and Spark 3.2.0. As a last step it will copy the data,spark_code and models folders to the built image.


After that run a container for spark by executing the command: 
        docker run --rm --network host -it voltage_spark /bin/bash

2. Training a Clustering Model In PySpark

Inside the spark shell run the command: 
        spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0 spark_code/train_kmeans.py

Here a KMeans model (using 5 clusters) will be trained and the centroids will be outputted in the end and the model will be saved uner thd folder "/models".


## Kafka 
1. Installation
We will run the related kafka containers using *docker-compose*, execute the following commands: 
        cd kafka
        docker-compose -f docker-compose.yml up -d
2. Producer
The Kafka Producer will have the role to turn the test csv file into streamed data and send it to spark for real-time clustering prediction.
3. Consumer 
It is the python script called *clustering_predictions_consumer.py* which will receive the predictions made by Spark.


## Executing the whole 
Using 3 command line windows:
- One for the Spark container shell 
- One for running the Kafka producer
- One for running the Kafka consumer 

In one of the windows run 
        cd kafka 
        python producer.py


In the spark shell run : 
        spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0 spark_code/real_time_clustering.py

In the 3rd and last window run : 
        cd kafka 
        python clustering_predictions_consumer.py
