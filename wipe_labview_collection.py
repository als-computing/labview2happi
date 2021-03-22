from pymongo import MongoClient

#connect to mongoDB on tsuru
client =  MongoClient('mongodb://131.243.73.51:27017')
#TODO: add authentication
db = client['happi']
collection = db['labview']

collection.remove({})
print("removed labview collection")