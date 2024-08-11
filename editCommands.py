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
    output = f"{net_connect.host}\n"
    output +=  f"{net_connect.config_mode()}"
    for command in commandsList:
        output +=  f"{net_connect.send_config_set(command)}"
    output +=  f"{net_connect.commit()}"
    dOutput[net_connect.host][command] = output
    #net_connect.exit_config_mode()




juniper_junosEdit = ['set system host-name NETMIKO']

arista_eosEdit = ["hostname NETMIKO"]