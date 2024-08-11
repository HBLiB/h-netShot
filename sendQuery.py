#!/usr/bin/env python3
from defaults import *
from queryCommands import *

selected_file = menuListFiles("Devices/",".json")
group = input("Enter tag to save with ")

with open(f"{devicesDir}{selected_file}", 'r') as jsonFile:
    devices = json.load(jsonFile)

print(json.dumps(devices, indent=4))


#user = input("Enter your username: ")
#print("Enter your password")
#password = getpass.getpass()

user = "halil"
passWord = "1234qwer"



def sendCommand(dHost, dDict, dNotReachable, dOutput):
    try:
        dDict[dHost]["username"] = user
        dDict[dHost]["password"] = passWord
        dOutput[dHost] = {}
        with ConnectHandler(**dDict[dHost]) as net_connect:
            dOutput[dHost]['device_type'] = dDict[dHost]['device_type']
            if dDict[dHost]['device_type'] == "juniper_junos":
                for command in juniper_junosCommands.keys():
                    try:
                        output = net_connect.send_command(juniper_junosCommands[command], read_timeout=90)
                        dOutput[dHost][command] = output
                    except Exception as exc:
                        print(f'{dHost} generated an exception: {exc}')
        dDict[dHost].pop("username", None)
        dDict[dHost].pop("password", None)
        print(f"Done with host {dHost}\t")
    except Exception as err:
        paramiko.util.log_to_file('paramiko.log')
        dNotReachable.append(dHost)
        dDict.pop(dHost, None)
    except OSError as error:
        paramiko.util.log_to_file('paramiko.log')
        dNotReachable.append(dHost)
        dDict.pop(dHost, None)

startMultiThread(devices, sendCommand, devices, notReachable, finalOutput)

unreachable(notReachable)


current_time = datetime.datetime.now().strftime("%Y_%m_%d_%H:%M")
filename = f"Output/Data_{group}_{current_time}.json"

with open(filename, 'w') as fp:
    json.dump(finalOutput, fp,indent=4)

