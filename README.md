# labview2happi
Scripts to add devices to a MongoDB using the happi client on startup of the Labview-to-EPICS bridge.

## Usage
 - Copy the conf_template.env from template folder to a local folder on the beamline machine. Edit all variables values to match your system/database parameters.
 - LabView's Python extension should then call the script "wipe_labview_collection.py" once in the beginning on startup like this: wipe_labview_collection.py $path_to_conf.env --> this wipes the existing documents from the collection
 - LabView's Python extension should then call the script "write_pv_to_mongo.py" like this: write_pv_to_mongo.py $path_to_conf.env $list_of_devices_to_write
