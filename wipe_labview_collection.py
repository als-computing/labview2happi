import sys
from dotenv import dotenv_values
from happi.backends.mongo_db import MongoClient

print(sys.argv[1])
conf = dotenv_values(sys.argv[1])

USER = conf.get("USER_HAPPI")
PASSWD = conf.get("PASSWD_HAPPI")
HOST = conf.get("HOST_HAPPI")
DB = conf.get("DB_HAPPI")
COLLECTION = conf.get("COLLECTION_HAPPI")
PREFIX = conf.get("PREFIX_HAPPI")
BEAMLINE = conf.get("BEAMLINE_HAPPI")
EXCLUDE_LIST_PATH = conf.get("EXCLUDE_LIST_HAPPI")

client =  MongoClient(f'mongodb://{USER}:{PASSWD}@{HOST}:27017/{DB}?authsource={DB}')
db = client[DB]
collection = db[COLLECTION]

collection.remove({})
print(f"removed {COLLECTION} collection")