"""
Usage:
    call this script like this
        python write_pv_to_mongo.py config_file device_list_file

    A template of the config file can be found in the template folder, make a copy on your system and change fields
    accordingly.

    For updating an existing database collection make sure to run wipe_labview_collection.py first before calling write_pv_to_mongo.py
"""


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
    print("Could not open device exclusion list. All devices will be added to database.")
    pass

# connect to database
db = MongoBackend(host=HOST,
                  db=DB,
                  user=USER,
                  pw=PASSWD,
                  collection=COLLECTION,
                  timeout=None)

# connect client to database
client = Client(db)

dev_list = sys.argv[2:]
# iterate through devices in the device list provided on labview startup unless device is excluded
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

### Notes for future development

# Option A:
#    - add another config file with user group specifics (somewhere on drive or maybe call params directly from LV?)
#    - call that config file and parse specific fields
#    - write these fields to happi db (have specific conditions on what goes where etc to automate)
#    - create a new collection for that db (names after ESAF ID?)

# Thoughts:
    # structure of that code --> is more granularity needed here?
    # what config files make sense?

# Questions:
    # How much will the different configs differ? --> Are multiple collections useful or is it better to just have
        # additional fields that can be used for filtering?
    # What fields/params are required?
        # mainly 2 different configs, related to type of experiment --> use of different endstation (selecting primary devices)
    # Preferences for read in/import? New collection with different authentication? Or simply different filtering? --> xicam example

    # Saving the config to reload when users come back
    # how/when do we need to store the device status (like gain etc)
    # --> Is Happi the place to store that
    # maybe bluesky is the better place to store these details (e.g with different sensitivity for different samples)
    # Pete Jemian might have a good examples

# Padraic:
# I'm hoping to be able to export LV config to happi db, with option of "Save as..." for multiple configs.
#   --> sure several options to discuss
#
# * Would need to also be able to import a selected config from happi back into LV
#   --> ask Lee/Damon about LV's capabilities
#
# * Ideally could do the same with bluesky (and potentially even BS->LV or LVBS)
#   --> that's possible, as it is all Python
#
# * When saving to happi, I would also like to select an ESAF ID that gets tied to the user group
#   --> could be written in config file, called by LV to write to happi db