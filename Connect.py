from netmiko import ConnectHandler

eltex = {
    'device_type': 'eltex',
    'host': '10.50.80.3',
    'username': 'admin',
    'password': 'admin',
}

huawei = {
    'device_type': 'huawei',
    'host': '10.50.80.4',
    'username': 'admin',
    'password': 'admin',

}

dlink_ds = {
    'device_type': 'dlink_ds',
    'host': '10.50.80.5',
    'username': 'admin',
    'password': 'admin',
}

on, off = 0,1
def lldp(port: str, com_type, on_off):
    global on, off
    connect_device = ConnectHandler(**com_type)
    connect_device.enable()
    connect_device.config_mode()
    if on_off == on:
        output = connect_device.send_command('lldp run')
        print(output, "on the " + str(com_type) + " lldp is enabled")
    elif on_off == off:
        output = connect_device.send_command('no lldp run')
        print(output, "on the " + str(com_type) + " lldp is disable")


# def no_lldp_run(port: str, com_type):
#     connect_device = ConnectHandler(**com_type)
#     connect_device.enable()
#     connect_device.config_mode()
#     output = connect_device.send_command('no lldp run')
#     print(output, "on the " + str(com_type) + " lldp is disable")


lldp(22, eltex, 0)
#no_lldp_run(22, eltex,)
