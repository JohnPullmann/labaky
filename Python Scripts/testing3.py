from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException
from getpass import getpass
from pprint import pprint
import sys
import os
from logging_setup_simple import logger

os.system("color")

# Saved devices
Devices = {"Switch1": {
                "host": "192.168.0.10",
                "device_type": "cisco_ios",
                "username": "Admin",
                "password": "cisco",
                'secret': "class",
                "global_delay_factor": 2,
                },
            "Switch2": {
                "host": "192.168.0.20",
                "device_type": "cisco_ios",
                "username": "Admin",
                "password": "cisco",
                'secret': "class",
                "global_delay_factor": 2,
                },
            "Switch3": {
                "host": "192.168.0.30",
                "device_type": "cisco_ios",
                "username": "Admin",
                "password": "cisco",
                'secret': "class",
                "global_delay_factor": 2,
                },
            "Localhost_Switch": {
                "host": "192.168.247.129",
                "port": "5000",
                "username": "",
                "password": "",
                "device_type": "extreme_exos",
                }
           }


# Choose devices to connect to
destination_devices = []

valid_devices = False
while not valid_devices:
    valid_devices = True

    logger.info("Choose devices to which you want to connect.")
    logger.info("Saved devices: ")
    for i, device in enumerate(Devices):
        logger.info(f"\t{i+1}. - {device}: {Devices[device]['host']} ({Devices[device]['device_type']})")
    print("") # Empty line
    logger.info("To choose device, type its number or name separated by comma. To stop choosing, type 'exit'. To choose all devices type 'all'. For examle: 1, Switch3")
    logger.info("Enter devices: ")
    destination_devices = input("").replace(' ', '').split(',')

    if "".join(destination_devices) == "exit":
        sys.exit()
    elif "".join(destination_devices) == "all":
        destination_devices = list(Devices.keys())
    for device in destination_devices:
        if device.isdigit():
            if 0 > int(device) > len(Devices):
                logger.error("Wrong device number\n")
                valid_devices = False
                break
            else:
                destination_devices[destination_devices.index(device)] = list(Devices.keys())[int(device)-1]
        elif device not in Devices:
            logger.error("Wrong device name\n")
            valid_devices = False
            break

logger.info(f"Devices to connect: { ', '.join(destination_devices)}")



#sys.exit()

# Choose protocol
protocol = None	
while protocol != "ssh" and protocol != "telnet":
    protocol = input("Choose protocol for connection ('ssh'/'telnet'): ")

# Set protocol to use for all devices
if protocol == "telnet":
    for device in Devices:
        Devices[device]["device_type"] = Devices[device]["device_type"] + "_telnet"

    

#def send_show_command(connection, command):
#    try:
#        return connection.send_command(command)
#    except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
#        print(error)

#for device in destination_devices:
#    with ConnectHandler(**device) as net_connect:
#        print(net_connect.find_prompt())
#        #net_connect.enable()
#
#        output = net_connect.send_command("show session")
#
#    pprint(output)




