#!/usr/bin/env python
from json import loads
from kafka import KafkaConsumer
import argparse
import json
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('topic', type=str,
                        help='Name of the Kafka topic to stream.')

    args = parser.parse_args()
    print("Connecting to consumer ...")

    # You can generate an API token from the "API Tokens Tab" in the UI
    token = "REPLACE BY YOUR TOKEN"
    # Please replace the org and bucket by your own values
    org = "ELTE"
    bucket = "CDN"

    with InfluxDBClient(url="http://localhost:8086", token=token, org=org) as client:
        write_api = client.write_api(write_options=SYNCHRONOUS)
        consumer = KafkaConsumer(
        args.topic,
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='my-group',
        value_deserializer=lambda x: loads(x.decode('utf-8')))
        print("Connection established")
        count=0
        for message in consumer:
            dict = json.loads(message.value)
            print(f"{message.value}")
            point = Point("CDN-data") \
                .tag("timestamp", dict["timestamp"]) \
                .field("channel_id", dict["channel_id"]) \
                .field("host_id", dict["host_id"]) \
                .field("content_type", dict["content_type"]) \
                .field("protocol", dict["protocol"]) \
                .field("content_id", dict["content_id"]) \
                .field("geo_location", dict["geo_location"]) \
                .field("user_id", dict["user_id"]) \
                .time(datetime.utcnow(), WritePrecision.NS)
            write_api.write(bucket, org, point)
            print("Message sent to influxDB")


if __name__ == "__main__":
    main()