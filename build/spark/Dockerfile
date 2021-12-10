ARG CDN_HOME

# Base image to start from.
FROM ubuntu:20.04

LABEL version="0.1"
LABEL description="Docker image to setp up Apache Spark For Clusetring and Data Streaming"

ARG USER_HOME_DIR="/root"
#ARG USER_HOME_DIR="/root"

# Update the system.

RUN apt-get update \ 
 && apt-get install -qq -y curl vim net-tools \
 && rm -rf /var/lib/apt/lists/*

# Install Python
FROM python:3.9-slim
RUN pip install --no-cache-dir matplotlib pandas numpy sklearn

# Install Java
RUN apt-get update \
 && apt-get install -y openjdk-11-jre \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*
#ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64/bin/java
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
#ENV JAVE_HOME=/usr/lib/jvm/java-11-oracle
ENV PATH=$JAVA_HOME/jre/bin:$PATH


# remove download archive files
RUN apt-get clean
# Install Spark
#RUN apk update
#RUN apk add
RUN apt-get update -y \
 && apt install -y build-essential \
 && apt-get install -y curl \
 && curl https://archive.apache.org/dist/spark/spark-3.2.0/spark-3.2.0-bin-hadoop2.7.tgz -o spark.tgz \
 && tar -xf spark.tgz \
 && mv spark-3.2.0-bin-hadoop2.7 /opt/spark/ \
 && rm spark.tgz

# Set Spark environment
ENV SPARK_HOME=/opt/spark
ENV PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin
COPY ${CDN_HOME}/build/spark/requirements.txt $SPARK_HOME/requirements.txt
RUN pip3 install -r ${SPARK_HOME}/requirements.txt

# EXPOSE CONTAINER PORTS
EXPOSE 4040 6066 7077 8080

# SET WORKING DIR
WORKDIR $SPARK_HOME

# Copy files
COPY ${CDN_HOME}/build/spark/log4j.properties $SPARK_HOME/conf
COPY ${CDN_HOME}/source/data $SPARK_HOME/data
COPY ${CDN_HOME}/source/spark/ $SPARK_HOME/spark_code
COPY ${CDN_HOME}/source/spark/models $SPARK_HOME/models
COPY ${CDN_HOME}/source/spark/processing_obj $SPARK_HOME/processing_obj

# Run commands
ADD ${CDN_HOME}/build/spark/entrypoint.sh ${SPARK_HOME}
RUN chmod +x ${SPARK_HOME}/entrypoint.sh

ENTRYPOINT ["/bin/bash", "./entrypoint.sh"]
CMD ["bin/spark-class", "org.apache.spark.deploy.master.Master", "org.apache.spark.deploy.worker.Worker"]