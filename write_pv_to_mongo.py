import sys
from dotenv import dotenv_values

from happi.backends.mongo_db import MongoBackend
from happi import Client
from happi.errors import EntryError, DuplicateError

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

exclude_dev_list = []
try:
    exclude_file = open(EXCLUDE_LIST_PATH, 'r')
    for line in exclude_file:
        exclude_dev_list.append(line.strip())
except:
    print("Could not open device exclusion list")

db = MongoBackend(host=HOST,
                  db=DB,
                  user=USER,
                  pw=PASSWD,
                  collection=COLLECTION,
                  timeout=None)

#connect client to database
client = Client(db)
dev_list = sys.argv[2:]
for dev in dev_list:
    if dev in exclude_dev_list:
        pass
    else:
        try:
            device = client.create_device("Device",
                                      name=dev,
                                      prefix=f"{PREFIX}:{dev}",
                                      beamline=BEAMLINE,
                                      location_group="Loc1",
                                      functional_group="Func1",
                                      device_class="ophyd.EpicsMotor",
                                      args=["{{prefix}}"],
                                      source="labview")
            device.save()

        except EntryError as err:
            print(f"{err}: {dev} Could not write device!")
            pass

        except DuplicateError as err:
            print(f"{err} Maybe database was not cleared out properly on startup, please run wipe_labview_collection.py")
