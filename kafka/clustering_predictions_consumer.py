from json import dumps,loads
from kafka import KafkaProducer
from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
from time import sleep

def json_serializer(data):
    return dumps(data).encode('utf-8')

print("Connecting to consumer ...")
es = Elasticsearch([ "localhost:9200"])
consumer = KafkaConsumer(
        'cdn_result',
     bootstrap_servers=['localhost:9092'],
     auto_offset_reset='earliest',
     enable_auto_commit=True,
     group_id='cdn-group',
     value_deserializer=lambda x: loads(x.decode('utf-8')))
producer_elk = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=lambda x: dumps(x).encode('utf-8'))

if "predictions" in es.indices.get('*'):
    es.indices.delete("predictions")

request_body = {
    "settings" : {
        "number_of_shards": 1,
        "number_of_replicas": 0
    }
}
es.indices.create(index='predictions',body=request_body)
for index in es.indices.get('*'):
  print(index)


for message in consumer:

 print(f"{message.value}")
 response = es.index(index = 'predictions',document = message.value)
 print(response)
 customers_list = [message.value]



