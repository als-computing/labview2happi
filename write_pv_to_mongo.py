import re
import sys
import os
from happi.backends.mongo_db import MongoBackend
from happi import Client
from happi.errors import EntryError, DuplicateError

#TODO:
# for now copy from labview server --> later create a mongo db

#selecting a database backend and initialze database file if not already existing
USERNAME = os.getenv("USERNAME_MONGO")
PASSWD = os.getenv("USERNAME_MONGO")

db = MongoBackend(host='131.243.73.51',
                  db='happi',
                  user=USERNAME,
                  pw=PASSWD,
                  collection='labview',
                  timeout=None, )

#connect client to database
client = Client(db)
#use device name from input when calling this script in labview, each time an EPICS PV gets registered
dev = sys.argv[-1]
#comply with happi naming conventions
if re.search('LS_LLHTA', dev):
    dev = dev.replace('LS_LLHTA', 'ls_llhta')
if re.search('LS_LLHTB', dev):
    dev = dev.replace('LS_LLHTB', 'ls_llhtb')
if re.search('TCP', dev):
    dev = dev.replace('TCP', 'tcp')
if re.search('CCD', dev):
    dev = dev.replace('CCD', 'ccd')
if re.search('UDP', dev):
    dev = dev.replace('UDP', 'udp')
if re.search('EPU', dev):
    dev = dev.replace('EPU', 'epu')
if re.search('AI', dev):
    dev = dev.replace('AI', 'ai')
if re.search('CAEN', dev):
    dev = dev.replace('CAEN', 'caen_')

device_name = re.sub(r'(?<!^)(?=[A-Z])', '_', dev).lower()
try:
    device = client.create_device("Device",
                              name=device_name,
                              prefix=f"BS701:{device_name}",
                              beamline="7.0.1.1 COSMIC",
                              location_group="Loc1",
                              functional_group="Func1",
                              device_class="ophyd.EpicsMotor",
                              args=["{{prefix}}"],
                              source="labview")
    device.save()

except EntryError as err:
    print(f"{err}: {device_name} Could not write device!")
    pass

except DuplicateError as err:
    print(f"{err} Maybe database was not cleared out properly on startup, please run wipe_labview_collection.py")
