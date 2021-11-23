from time import sleep
import csv
from json import dumps
from kafka import KafkaProducer



def json_serializer(data):
    return dumps(data).encode('utf-8')

producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=lambda x: dumps(x).encode('utf-8'))
rdr = csv.reader(open("../data/test_cdn.csv"))

next(rdr)


while True:
    try:
        line=next(rdr,None)
        if line is None:
            break
        sleep(5)
        timestamp,channel_id,host_id,content_type,protocol,content_id,geo_location,user_id=line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7]
        #timestamp,accelo1rms, accelo2rms,current,pressure,temperature,thermocouple,voltage,volumeflow=line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8]

        result={"timestamp":timestamp,"channel_id":channel_id,"host_id":host_id,"content_type":content_type,"protocol":protocol,"content_id":content_id,"geo_location":geo_location,"user_id":user_id}
        producer.send('cdn_data',value=result)
        print(result)
    except Exception as e: 

        print("Errrrrrrrrrrrrrrrrrrrrrrrrror")
        print(f"Type {e}")
        break
