#!/usr/bin/env python3
from defaults import *

devicesRaw = []
devList = []
devices = {}
notReachable = []
devices = {}

def is_host_alive(host):
    # Determine the command based on the operating system
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "2", host]

    try:
        # Run the ping command
        output = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Check return code
        return output.returncode == 0
    except Exception as e:
        print(f"Error pinging {host}: {e}")
        return False
    
# Prepare device connection details, adjust to the manual Vendor
def processHostsByName(host,devicesD,dNotReachable):
    if is_host_alive(host):
        if "192.168.178.199" in host.lower():
            devType = "arista_eos"
        else:
            devType = "juniper_junos"
        devicesD[host]["device_type"] = devType
    else:
        print(f"Host {host} is not reachable and will not be added.")
        dNotReachable.append(host)


selected_file = menuListFiles("Devices/",".list")

# Read device list from the selected file
devicesRaw = []
with open(f"{devicesDir}{selected_file}") as f:
    devicesRaw = f.readlines()

tag = input("Enter tag to save with ")

# Clean up device entries, and create initial MikoIndex for auto detection
for entry in devicesRaw:
    entry = entry.strip()
    devices[entry] = {
    "device_type": "autodetect",
    "host": entry,
    "conn_timeout": 10,
    "timeout": 60,
    "session_timeout": 60,
    "blocking_timeout": 60,
    #"ssh_config_file": baseDir + "jumphost.conf"
    }


startMultiThread(devices, processHostsByName, devices, notReachable)

unreachable(notReachable)

current_time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M")

with open(f"{devicesDir}PingIndex{tag}-{current_time}.json", 'w') as fp:
   json.dump(devices, fp,indent=4)