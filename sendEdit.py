#!/usr/bin/env python3
from defaults import *
from editCommands import *

selected_file = menuListFiles("Devices/",".json")

with open(f"{devicesDir}{selected_file}", 'r') as jsonFile:
    devices = json.load(jsonFile)

print(json.dumps(devices, indent=4))


#user = input("Enter your username: ")
#print("Enter your password")
#password = getpass.getpass()

user = "halil"
passWord = "1234qwer"

group = input("Enter tag to save with ")


def sendCommand(dHost, dDict, dNotReachable,dOutput):
    try:
        dDict[dHost]["username"] = user
        dDict[dHost]["password"] = passWord
        dOutput[dHost] = {}
        with ConnectHandler(**dDict[dHost]) as net_connect:
            if dDict[dHost]['device_type'] == "juniper_junos":
                try:
                    JuniperSendEdit(net_connect,juniper_junosEdit,dOutput)
                except Exception as exc:
                        print(f'{dHost} generated an exception: {exc}')
            elif dDict[dHost]['device_type'] == "arista_eos":
                try:
                    AristaSendEdit(net_connect,arista_eosEdit)
                except Exception as exc:
                    print(f'{dHost} generated an exception: {exc}')
        print(f"Done with host {dHost}\t")
    except Exception as err:
        paramiko.util.log_to_file('paramiko.log')
        dNotReachable.append(dHost)
        dDict.pop(dHost, None)
    except OSError as error:
        paramiko.util.log_to_file('paramiko.log')
        dNotReachable.append(dHost)
        dDict.pop(dHost, None)

startMultiThread(devices, sendCommand, devices, notReachable,finalOutput)

unreachable(notReachable)

print("everything is done ")
for host in finalOutput.keys():
    print(f"--------{host}")
    for x in finalOutput[host].keys():
        print(finalOutput[host][x])



current_time = datetime.datetime.now().strftime("%Y_%m_%d_%H:%M")
filename = f"Output/Data_{group}_{current_time}.json"

json_string = json.dumps(finalOutput, indent=4)

# Replace double-escaped newlines with actual newlines for better readability in terminal
json_string = json_string.replace('\\n', '\n')

# Write the modified JSON string to the file
with open(filename, 'w') as fp:
    fp.write(json_string)
