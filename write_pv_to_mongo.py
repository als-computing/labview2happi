import os
import re
import sys
from dotenv import dotenv_values

from happi.backends.mongo_db import MongoBackend
from happi import Client
from happi.errors import EntryError, DuplicateError


conf = dotenv_values(sys.argv[1])

USER = conf.get("USER_HAPPI")
PASSWD = conf.get("PASSWD_HAPPI")
HOST = conf.get("HOST_HAPPI")
DB = conf.get("DB_HAPPI")
COLLECTION = conf.get("COLLECTION_HAPPI")
PREFIX = conf.get("PREFIX_HAPPI")
BEAMLINE = conf.get("BEAMLINE_HAPPI")
EXCLUDE_LIST_PATH = conf.get("EXCLUDE_LIST_HAPPI")

exclude_file = open(EXCLUDE_LIST_PATH, 'r')
exclude_dev_list = []
for line in exclude_file:
    exclude_dev_list.append(line.strip())

db = MongoBackend(host=HOST,
                  db=DB,
                  user=USER,
                  pw=PASSWD,
                  collection=COLLECTION,
                  timeout=None)

#connect client to database
client = Client(db)
#use device name from input when calling this script in labview, each time an EPICS PV gets registered
dev_list = sys.argv[1:]
for dev in dev_list:
    if dev not in (exclude_dev_list):
        try:
            device = client.create_device("Device",
                                      name=dev,
                                      prefix=f"BCS701:{dev}",
                                      beamline="7.0.1.1 COSMIC",
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
