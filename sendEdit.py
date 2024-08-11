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