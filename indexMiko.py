#!/usr/bin/env python3
from defaults import *

user = input("Enter your username: ")
print("Enter your password")
password = getpass.getpass()

devicesRaw = []
devices = {}
finalDevices = {}
notReachable  = []
devicesDir = "Devices/"


devList = []

# Use the menuListFiles function to list all .list files in the Devices directory and use the entries for devicesRaw
selected_file = menuListFiles("Devices/",".list")

# Read device list from the selected file
devicesRaw = []
with open(f"{devicesDir}{selected_file}") as f:
    devicesRaw = f.readlines()


group = input("Enter tag to save with ")

# Clean up device entries, and create initial MikoIndex for auto detection
for entry in devicesRaw:
    entry = entry.strip()
    devices[entry] = {
    "device_type": "autodetect",
    "host": entry,
    "username": user,
    "password": password,
    "conn_timeout": 10,
    "timeout": 60,
    "session_timeout": 60,
    "blocking_timeout": 60,
    #"ssh_config_file": baseDir + "jumphost.conf"
    }


#Guessing of OS of the device, going through a list of device names based on the device dictonary previously created
def guessOS(host,dDict,dFinal,dNotReachable):
    try:
        print(f"Trying to autodetect {host}")
        guess = SSHDetect(**dDict[host])
        best_match = guess.autodetect()
        dFinal[host] = {
        "device_type": best_match ,
        "host": host,
        "conn_timeout": 10,
        "timeout": 60,
        "session_timeout": 60,
        "blocking_timeout": 60,
        #"ssh_config_file": baseDir + "jumphost.conf"
        }
    except Exception as err:
        exception_type = type(err).__name__
        print(exception_type)
        dNotReachable.append(host)
    except OSError as error :
        print(error)
        dNotReachable.append(host)


startMultiThread(devices, guessOS, devices,finalDevices,notReachable)

unreachable()

# Write devices to JSON file
current_time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M")

with open(f"{devicesDir}MikoIndex-{group}-{current_time}.json", 'w') as fp:
    json.dump(finalDevices, fp,indent=4)

devices = {}
