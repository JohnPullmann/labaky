from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException
from getpass import getpass
from pprint import pprint
import sys
import os
from logging_setup_simple import logger

from test_connectivity import test_connectivity

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
                "username": "Admin",
                "password": "",
                "device_type": "extreme_exos",
                }
           }


# Choose devices to connect to
destination_devices = {}

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
    user_input = input("").replace(' ', '').split(',')

    if "".join(user_input) == "exit":
        sys.exit()
    elif "".join(user_input) == "all":
        destination_devices = Devices
        break
    for device in user_input:
        if device.isdigit():
            if 0 < int(device) <= len(Devices):
                destination_devices[list(Devices.keys())[int(device)-1]] = Devices[list(Devices.keys())[int(device)-1]]
            else:
                logger.error("Wrong device number\n")
                valid_devices = False
                break
                
        elif device not in Devices:
            logger.error("Wrong device name\n")
            valid_devices = False
            break
        else:  
            destination_devices[device] = Devices[device]

print() # Empty line
logger.info(f"Devices to connect: { ', '.join(destination_devices.keys())}\n")



#sys.exit()

# Choose protocol
protocol = None	
while True:
    logger.info("Choose protocol for connection ('ssh'/'telnet'): ")
    protocol = input("").strip()
    if protocol != "ssh" and protocol != "telnet":
        logger.error("Wrong protocol\n")
    else:
        break
print() # Empty line

# Set protocol to use for all devices
if protocol == "telnet":
    for device in Devices:
        Devices[device]["device_type"] = Devices[device]["device_type"] + "_telnet"

    

#def send_show_command(connection, command):
#    try:
#        return connection.send_command(command)
#    except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
#        print(error)

operation = None
available_operations = {
                        "Test Connectivity": {
                            "name": "Test Connectivity",
                            "description": "Test connectivity to devices",
                            "function": test_connectivity,
                            }
                        }
while True:
    logger.info("Choose one of available configuration and operations:")   
    for i, operation in enumerate(available_operations):
        logger.info(f"\t{i+1}. - {operation}{':' if available_operations[operation]['description'] else ''} {available_operations[operation]['description']}")
    print("") # Empty line
    logger.info("To choose operation, type its number or name. To stop choosing, type 'exit'.")
    logger.info("Enter operation: ")
    user_input = input("").strip()

    if "".join(user_input) == "exit":
        sys.exit()

    elif user_input.isdigit():
        if 0 < int(user_input) <= len(available_operations):
            operation = available_operations[list(available_operations.keys())[int(user_input)-1]]
            break
        else:
            logger.error("Wrong operation number\n")
    elif user_input not in available_operations:
        logger.error("Wrong operation name\n")
    else:
        operation = available_operations[user_input]
        break
print() # Empty line

# Start operation
logger.info("Starting operation: " + operation["name"] + "\n")
operation["function"](logger, destination_devices)

#for device in destination_devices:
#    pass
    #try:
    #    with ConnectHandler(**Devices[device]) as net_connect:
    #        which_prompt = net_connect.find_prompt()
    #        print(which_prompt)
            #if '>' in which_prompt:
            #    net_connect.enable() # Go to Priv EXEC mode only 'if' '>' is present in the output
            #net_connect.config_mode() # Global config mode
    #        print(net_connect.find_prompt())
    #        #net_connect.enable()
    #
    #        output = net_connect.send_command("show session")
    #
    #    pprint(output)
    #except (TimeoutError) as error:
    #    logger.error(f"Could not connect to {device}")

    #except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
    #    logger.error(error)



