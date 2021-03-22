import re
import sys
from happi.backends.mongo_db import MongoBackend
from happi import Client
from happi.errors import EntryError, DuplicateError

#TODO:
# for now copy from labview server --> later create a mongo db

#selecting a database backend and initialze database file if not already existing

# cl = pymongo.MongoClient('mongodb://happi.labview.com')
db = MongoBackend(host='131.243.73.51',
                  db='happi',
                  collection='labview',
                  timeout=None, )

#connect client to database
client = Client(db)
#use device name from input when calling this script in labview, each time an EPICS PV gets registered
dev = sys.argv[0]
#comply with happi naming conventions
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
