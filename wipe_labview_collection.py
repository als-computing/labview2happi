import os
from pymongo import MongoClient

USERNAME = os.getenv("USERNAME_MONGO")
PASSWD = os.getenv("PASSWD_MONGO")
#connect to mongoDB on tsuru
client =  MongoClient(f'mongodb://{USERNAME}:{PASSWD}@131.243.73.172:27017/happi?authsource=happi')
#TODO: add authentication
db = client['happi']
collection = db['labview']

collection.remove({})
print("removed labview collection")