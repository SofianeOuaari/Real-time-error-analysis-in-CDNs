import pymongo  # package for working with MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["prediction"]
customers = db["prediction"]



for x in customers.find():
    print(x)