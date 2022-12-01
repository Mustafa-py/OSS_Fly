
from netmiko import ConnectHandler
import time
import re

# huawei = {
#     'device_type': 'huawei',
#     'host': '10.50.80.4',
#     'username': 'admin',
#     'password': 'admin',
#
# }


eltex = {
    'device_type': 'eltex',
    'host': '10.50.80.3',
    'username': 'admin',
    'password': 'admin'
}


def show_port_status(port: str, com_type):
    connect_device = ConnectHandler(**com_type)
    output = connect_device.send_command('show interfaces status')
    time.sleep(3)
    # connect_device.send_command("\\N{0020}")
    output2 = output.split("\n")
    #pattern = re.search(r'gi1/0/')
    #print(output)
    for i in output2:
        output3 = re.split(r"\s+", i)
        if output3[0] == f"gi1/0/{port}":
            if output3[6] == "Up":
                return True
            else:
                return False


prt5 = show_port_status(22, eltex)
print(prt5)


def show_mac_by_port(port, com_type):
    connect_device = ConnectHandler(**com_type)
    output = connect_device.send_command('show arp')
    time.sleep(1)
    output2 = output.split("\n")
    mas = []
    for i in output2:
        output3 = re.split(r"\s+", i)
        if len(output3) > 2:
            if output3[2] == f"gi1/0/{port}" and len(output3) > 4:
                mas.append(output3[4])
    print(mas)
    return mas




# connect_huawei = ConnectHandler(**huawei)
# connect_eltex = ConnectHandler(**eltex)
#
# output = connect_eltex.send_command('show vlan')
# print(f'--------{connect_eltex}--------')
# print(output)

show_mac_by_port(23, eltex)
