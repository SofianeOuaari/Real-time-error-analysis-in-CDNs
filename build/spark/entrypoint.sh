#!/bin/bash
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0 /opt/spark/spark_code/train_ensemble_anomaly.py
#spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0 /opt/spark/spark_code/test_ensemble_anomaly.py
#spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0 /opt/spark/spark_code/windowing.py
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0 /opt/spark/spark_code/real_time_cdn_anomaly.py