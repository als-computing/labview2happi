import sys
import warnings
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
# PREFIX = conf.get("PREFIX_HAPPI")
PREFIX = "SR"
BEAMLINE = conf.get("BEAMLINE_HAPPI")

db = MongoBackend(host=HOST,
                  db=DB,
                  user=USER,
                  pw=PASSWD,
                  collection=COLLECTION,
                  timeout=None)

try:
    device_name = sys.argv[2]
    source = sys.argv[3]
except:
    warnings.warn("No device name or source given as arguments. "
                  "Please run 'python add_single_entry.py $path_to_conv.env_file $device_name $source_name' ")

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
