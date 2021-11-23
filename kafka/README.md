# Running Kafka for CDN Client Error dataset

## Kafka 
1. Installation
Run the related kafka containers using *docker-compose*, execute the following command from this directory:

        docker-compose up -d

2. Producer
The Kafka Producer has the role to turn the test csv file into streamed data and send it to spark for real-time clustering prediction.
	
    From this directory the following command can be used to run the producer:

        python sendStream.py [Path to the CSV File] [Name of the Kafka topic] [Optional: Multiplying factor for the sending speed]
		
    Therefore, to launch a producer for the CDN Clienr Error dataset (in actual speed):
        
        python sendStream.py "../data/CDN Client Error.csv" stream-CDN 
		
    It is also possible to add a third argue to specify a multiplying factor to the speed. For example to multiply the speed by 1000 (compared to the original timestamp) the following command should be used:

        python sendStream.py "../data/CDN Client Error.csv" stream-CDN --speed=1000
		
3. Consumer 
From another command line interpreter you can run the basic customer that will just receive and read the data:
		
        python consumer.py stream-CDN