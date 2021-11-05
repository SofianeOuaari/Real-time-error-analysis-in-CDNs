from time import sleep
import csv
from json import dumps
from kafka import KafkaProducer

#producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=lambda x: dumps(x).encode('utf-8'))

'''print("Please insert a number --> 'stop' to exit")
input_user = input()
index = 0'''

def json_serializer(data):
    return dumps(data).encode('utf-8')

producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=lambda x: dumps(x).encode('utf-8'))
rdr = csv.reader(open("../data/test.csv"))

next(rdr)
#firstline = True


while True:
    try:
        line=next(rdr,None)
        if line is None:
            break
        sleep(5)
        
        timestamp,accelo1rms, accelo2rms,current,pressure,temperature,thermocouple,voltage,volumeflow=line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8]

        result={"timestamp":timestamp,"accelo1rms":accelo1rms,"accelo2rms":accelo2rms,"current":current,"pressure":pressure,"temperature":temperature,"thermocouple":thermocouple,"voltage":voltage,"volumeflow":volumeflow}
        #result[timestamp]=open
        producer.send('voltage_data',value=result)
        print(result)
    except Exception as e: 

        print("Errrrrrrrrrrrrrrrrrrrrrrrrror")
        print(f"Type {e}")
        break
