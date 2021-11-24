#!/usr/bin/env python

"""Generates a stream to Kafka from a time series csv file.
"""

import argparse
import csv
from json import dumps
import sys
import time
from dateutil.parser import parse
from kafka import KafkaProducer
import socket


def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg.value()), str(err)))
    else:
        print("Message produced: %s" % (str(msg.value())))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('filename', type=str,
                        help='Path to CSV file.')
    parser.add_argument('topic', type=str,
                        help='Name of the Kafka topic to stream.')
    parser.add_argument('--speed', type=float, default=1, required=False,
                        help='Speed up time series by a given multiplicative factor.')
    args = parser.parse_args()

    topic = args.topic
    p_key = args.filename
    
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=lambda x: dumps(x).encode('utf-8'))

    rdr = csv.reader(open(args.filename))
    next(rdr)  # Skip header

    try:
        line = next(rdr, None)
        channel_id,timestamp,host_id,content_type,protocol,content_id,geo_location,user_id = line[1],line[0],line[2],line[3],line[4],line[5],line[6],line[7]
        # Convert csv columns to key value pair
        result = {"channel_id":channel_id,"timestamp":timestamp,"host_id":host_id,"content_type":content_type,"protocol":protocol,"content_id":content_id,"geo_location":geo_location,"user_id":user_id}
        # Convert dict to json as message format
        jresult = dumps(result)

        producer.send(topic, value=jresult)
        #producer.send(topic, key=p_key, value=jresult).add_callback(acked)

    except Exception as e:
            print("Error: unable to read csv file, end of program")
            print(e)
            sys.exit()

    while True:
        try:
            line = next(rdr, None)
            d1 = parse(timestamp)
            d2 = parse(line[0])
            diff = ((d2 - d1).total_seconds())/args.speed
            if(diff<0): diff=0
            print("Next message in ", diff, " seconds")
            time.sleep(diff)
            channel_id,timestamp,host_id,content_type,protocol,content_id,geo_location,user_id = line[1],line[0],line[2],line[3],line[4],line[5],line[6],line[7]
            result = {"channel_id":channel_id,"timestamp":timestamp,"host_id":host_id,"content_type":content_type,"protocol":protocol,"content_id":content_id,"geo_location":geo_location,"user_id":user_id}
            jresult = dumps(result)

            producer.send(topic, value=jresult)
            #producer.send(topic, key=p_key, value=jresult).add_callback(acked)

            producer.flush()

        except Exception as e:
            print("End of program")
            print(e)
            sys.exit()


if __name__ == "__main__":
    main()
