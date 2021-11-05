# Base image to start from.
FROM ubuntu:20.04

LABEL version="0.1"
LABEL description="Docker image to setp up Apache Spark For Clusetring and Data Streaming"

# Update the system.
RUN apt-get update \ 
 && apt-get install -qq -y curl vim net-tools \
 && rm -rf /var/lib/apt/lists/*

# Install Python
FROM python:3.9-slim
RUN pip install --no-cache-dir matplotlib pandas numpy
# Install Java
RUN apt-get update \
 && apt-get install -y openjdk-11-jre \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Install Spark
RUN apt-get update -y \
 && apt-get install -y curl \
 && curl https://archive.apache.org/dist/spark/spark-3.2.0/spark-3.2.0-bin-hadoop2.7.tgz -o spark.tgz \
 && tar -xf spark.tgz \
 && mv spark-3.2.0-bin-hadoop2.7 /opt/spark/ \
 && rm spark.tgz

# Set Spark environment
ENV SPARK_HOME=/opt/spark
ENV PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin

# EXPOSE CONTAINER PORTS
EXPOSE 4040 6066 7077 8080

# SET WORKING DIR
WORKDIR $SPARK_HOME

# Copy files
COPY log4j.properties $SPARK_HOME/conf
COPY data $SPARK_HOME/data
COPY spark_code $SPARK_HOME/spark_code
COPY models $SPARK_HOME/models

# Run commands
CMD ["bin/spark-class", "org.apache.spark.deploy.master.Master", "org.apache.spark.deploy.worker.Worker"]
