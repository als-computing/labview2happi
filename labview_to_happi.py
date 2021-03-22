import re
from happi.backends.json_db import JSONBackend
from happi import Client
from happi.errors import EntryError, DuplicateError

#TODO:
# for now copy from labview server --> later create a mongo db

#selecting a database backend and initialze database file if not already existing
try:
    db = JSONBackend(path='happi-test.json', initialize=True)
except PermissionError:
    db = JSONBackend(path='happi-test.json', initialize=False)


### TODO replace this with procedual labview output
bcs_file = open('./motorPV_names.txt')

dev_dict ={}
for line in bcs_file.readlines():
    dev_dict[line.split(":")[-1].strip('\n')] = line.strip('\n')
###

#connect client to database
client = Client(path='happi-test.json')
for dev in dev_dict:
    pv_prefix = dev_dict[dev]
    try:
        # make sure device name fulfills happi requirements
    # convert Uppercase to snake_case with exceptions for EGU,LS_LLHTAEGU, LS_LLHTBEGU, EPU, CPY
        if re.search('EGU', dev):
            dev = dev.replace('EGU', '_egu')
        if re.search('LS_LLHTA', dev):
            dev = dev.replace('LS_LLHTA', 'ls_llhta')
        if re.search('LS_LLHTB', dev):
            dev = dev.replace('LS_LLHTB', 'ls_llhtb')
        if re.search('EPU', dev):
            dev = dev.replace('EPU', 'epu')
        if re.search('CPY', dev):
            dev = dev.replace('CPY', 'cpy')
        device_name = re.sub(r'(?<!^)(?=[A-Z])', '_', dev).lower()
        # add device to happi db
        device = client.create_device("Device",
                                   name=device_name,
                                   prefix=pv_prefix,
                                   beamline='7.0.1.1 COSMIC',
                                   location_group="Loc1",
                                   functional_group="Func1",
                                   device_class='ophyd.EpicsMotor',
                                   args=[])
        device.save()
    except EntryError as err:
    #     #TODO catch specific exception
        print(f"{err}: {device_name}")
        pass

    except DuplicateError as err:
        print(err)
