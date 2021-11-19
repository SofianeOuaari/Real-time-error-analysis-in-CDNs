# Base image to start from.
FROM ubuntu:20.04

LABEL version="0.1"
LABEL description="Docker image to setp up Apache Spark For Clusetring and Data Streaming"

ARG MAVEN_VERSION=3.6.3
ARG USER_HOME_DIR="/root"
#ARG USER_HOME_DIR="/root"
ARG BASE_URL=https://apache.osuosl.org/maven/maven-3/$MAVEN_VERSION/binaries

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
# Install Maven 
#FROM openjdk:8-jdk-slim
#RUN apk add --no-cache curl tar bash procps
#RUN mkdir -p /usr/share/maven /usr/share/maven/ref \
# && curl -fsSL -o /tmp/apache-maven.tar.gz https://www.apache.org/dist/maven/maven-3/3.6.3/binaries/apache-maven-3.6.3-bin.tar.gz \
# && tar -xzf /tmp/apache-maven.tar.gz -C /usr/share/maven --strip-components=1 \
# && rm -f /tmp/apache-maven.tar.gz \
# && ln -s /usr/share/maven/bin/mvn /usr/bin/mvn
RUN apt-get update 
RUN apt-get install -y git
RUN apt-get install -y wget
RUN wget --no-verbose -O /tmp/apache-maven-3.6.3.tar.gz http://archive.apache.org/dist/maven/maven-3/3.6.3/binaries/apache-maven-3.6.3-bin.tar.gz

# verify checksum
#RUN echo "516923b3955b6035ba6b0a5b031fbd8b /tmp/apache-maven-3.6.3.tar.gz" | md5sum -c

# install maven
RUN tar xzf /tmp/apache-maven-3.6.3.tar.gz -C /opt/
RUN ln -s /opt/apache-maven-3.6.3 /opt/maven
RUN ln -s /opt/maven/bin/mvn /usr/local/bin
RUN rm -f /tmp/apache-maven-3.6.3.tar.gz
ENV MAVEN_HOME /opt/maven

# remove download archive files
RUN apt-get clean
# Install Spark
#RUN apk update
#RUN apk add
RUN apt-get update -y \
 && apt-get install -y curl \
 && curl https://archive.apache.org/dist/spark/spark-3.2.0/spark-3.2.0-bin-hadoop2.7.tgz -o spark.tgz \
 && tar -xf spark.tgz \
 && mv spark-3.2.0-bin-hadoop2.7 /opt/spark/ \
 && rm spark.tgz




# Set Maven Environment

ENV MAVEN_HOME=/usr/share/maven
ENV MAVEN_CONFIG=$USER_HOME_DIR/.m2
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
COPY requirements.txt $SPARK_HOME/requirements.txt

RUN pip3 install -r requirements.txt
COPY spark-iforest $SPARK_HOME/spark-iforest

# Run commands
CMD ["bin/spark-class", "org.apache.spark.deploy.master.Master", "org.apache.spark.deploy.worker.Worker"]
