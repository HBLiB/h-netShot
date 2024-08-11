import warnings
from cryptography.utils import CryptographyDeprecationWarning
with warnings.catch_warnings():
    warnings.filterwarnings('ignore', category=CryptographyDeprecationWarning)
    import paramiko
import getpass
import json
from netmiko import ConnectHandler
import datetime
from netmiko.ssh_autodetect import SSHDetect
from netmiko.ssh_dispatcher import ConnectHandler
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import subprocess
import platform

devicesDir = "Devices/"
outputDir = "Output/"
finalOutput = {}
notReachable = []

def menuListFiles(devicesDir,pattern):
    list_files = sorted([f for f in os.listdir(devicesDir) if f.endswith(pattern)])

    if not list_files:
        print(f"No {pattern} files found in the working directory.")
    else:
        print(f"Available {pattern} files:")
        for idx, file in enumerate(list_files):
            print(f"{idx + 1}. {file}")
        
        # Prompt the user to select a file
        while True:
            try:
                choice = int(input("Enter the number of the file you want to use: ")) - 1
                if 0 <= choice < len(list_files):
                    selected_file = list_files[choice]
                    break
                else:
                    print("Invalid choice. Please select a number from the list.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")
        
        # Use the selected file
        print(f"Using file: {selected_file}")
        return selected_file 

def unreachable(notReachable):        
    # Write unreachable devices to file
    if len(notReachable) != 0:
        with open(f"{devicesDir}unreachable.list", 'w') as fp:
            for item in notReachable:
                fp.write("%s\n" % item)


def startMultiThread(devices,function, *args, **kwargs):
    # Multithreaded execution
    with ThreadPoolExecutor(max_workers=20) as executor:
        future_to_host = {executor.submit(function, host, *args, **kwargs): host for host in devices.keys()}
        for future in as_completed(future_to_host):
            host = future_to_host[future]
            try:
                future.result()
            except Exception as exc:
                print(f'{host} generated an exception: {exc}')

