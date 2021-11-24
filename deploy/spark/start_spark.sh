docker run --rm --network host -it ${CDN_REGISTRY}/cdn_spark:1.0.0 /bin/bash

# spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0 spark_code/train_ensemble_anomaly.py

# spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0 spark_code/real_time_cdn_anomaly.py