import re

def JuniperSendEditORG(net_connect, commandsList):
    net_connect.config_mode()
    for command in commandsList:
        net_connect.send_config_set(command)
    net_connect.commit()
    #net_connect.exit_config_mode()

def AristaSendEdit(net_connect, commandsList):
    net_connect.enable()
    net_connect.config_mode()
    for command in commandsList:
        net_connect.send_config_set(command)
    #net_connect.exit_config_mode()
    net_connect.save_config()


catchOutput = []

def JuniperSendEdit(net_connect, commandsList,dOutput):
    output =  f"{net_connect.config_mode()}"
    for command in commandsList:
        output +=  f"{net_connect.send_config_set(command)}"
        #output += re.sub(r'^\s*$\n', '', net_connect.send_config_set(command), flags=re.MULTILINE)
    output +=  f"{net_connect.commit()}"
    #output = re.sub(r'^\s*$\n', '', output, flags=re.MULTILINE)
    #output = output.replace('\n\n', '\\n')
    dOutput[net_connect.host][command] = output
    #net_connect.exit_config_mode()


juniper_junosEdit = ['set system host-name NETMIKO114',
                     'set system host-name NETMIKO115']

arista_eosEdit = ["hostname NETMIKO"]