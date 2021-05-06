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

device_name = "TestDevice"
source = "test"

client = Client(db)
device = client.create_device("Device",
                                   name=device_name,
                                   prefix=f"{PREFIX}:{device_name}",
                                   beamline="ALS beamline",
                                   location_group="Loc1",
                                   functional_group="Func1",
                                   device_class="ophyd.EpicsMotor",
                                   args=["{{prefix}}"],
                                   source=source)
device.save()