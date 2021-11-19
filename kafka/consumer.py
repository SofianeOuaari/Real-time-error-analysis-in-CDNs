#!/usr/bin/env python
from json import loads
from kafka import KafkaConsumer
import argparse


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('topic', type=str,
                        help='Name of the Kafka topic to stream.')

    args = parser.parse_args()
    print("Connecting to consumer ...")
    consumer = KafkaConsumer(
        args.topic,
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='my-group',
        value_deserializer=lambda x: loads(x.decode('utf-8')))
    print("Connection established")
    for message in consumer:
        print(f"{message.value}")


if __name__ == "__main__":
    main()
