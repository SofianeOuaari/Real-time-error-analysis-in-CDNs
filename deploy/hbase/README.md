# HBase

## Creating The HBase environment:

        docker-compose up -d
The HBase daemons (the HMaster, the HRegionServer, and the ZooKeeper daemon) will all run in the same JVM. 

## Accessing the HBase environment:
**Go to [http://localhost:16010](http://localhost:16010) to view the HBase Web UI.**

**Connect to the running instance of HBase using the following command:**
         
        docker exec -it cdn-hbase hbase shell

## Querying HBase
**Please note that you might have to wait some time for the starting of the server after having created the containers. 
If you get the error "Server is not running yet" after sending a query just try again a few seconds later.**

### Create a table:

        create 'table name', 'ColumnFamily name'

Example:

        create 'test', 'cf'

### List Information about the Table

        list 'test'
Use the describe command to see details, including configuration defaults:

        describe 'test'

### Put data into the table:
        put 'test', 'row1', 'cf:a', 'value1'

### Scan the table to access the data:
        scan 'test'

## Documentation:
Please refer to the official documentation to look at more advanced options: https://hbase.apache.org/book.html#quickstart

