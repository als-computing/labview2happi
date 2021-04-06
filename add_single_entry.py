import re
from happi.backends.mongo_db import MongoBackend
from happi import Client
from happi.errors import EntryError, DuplicateError
import os

USER_MONGO = os.getenv("USER_MONGO")
PASSWD_MONGO = os.getenv("PASSWD_MONGO")

db = MongoBackend(host='131.243.73.172',
                  db='happi',
                  user = USER_MONGO,
                  pw = PASSWD_MONGO,
                  collection='labview_static',
                  timeout=None, )

pv_prefix = "BCS701"
device_name = "DetectorDiodeCurrent"

client = Client(db)
device = client.create_device("Device",
                                   name=device_name,
                                   prefix=f"{pv_prefix}:{device_name}",
                                   beamline="7.0.1.1 COSMIC",
                                   location_group="Loc1",
                                   functional_group="Func1",
                                   device_class="ophyd.EpicsMotor",
                                   args=["{{prefix}}"],
                                   source=  "labview" )
device.save()