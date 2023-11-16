from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException
import os
from datetime import datetime

def backup_config(logger, Devices):
    """Backup configuration of devices."""
    if not os.path.exists('backup-config'):
        os.makedirs('backup-config')

    outputs = {}

    for device in Devices:
        logger.info(f"Backing up {device}...")
        try:
            with ConnectHandler(**Devices[device]) as net_connect:
                logger.info(f"\tConnected to {device}\n")
                net_connect.enable()

                # Gets the running configuration.
                output = net_connect.send_command("show run")
                outputs[device] = output
                logger.info("\tConfig retrieved")
                # Gets and splits the hostname for the output file name.
                hostname = net_connect.send_command("show conf | i hostname").split()[1]
                # Creates the file name, which is the hostname, and the date and time.
                fileName = hostname + "_" + dt_string
                # Creates the text file in the backup-config folder with the special name, and writes to it.
                if not os.path.exists('backup-config/'+hostname+"/"):
                    os.makedirs('backup-config')
                file_path = "backup-config/"+hostname+"/" + fileName + ".txt"

                backupFile = open(file_path, "w+")
                backupFile.write(output)
                logger.info("\tOutputted to " + file_path + "\n")

        except (TimeoutError) as error:
            logger.error(f"\tCould not connect to {device}, Connection timed out\n")
        except (NetmikoAuthenticationException) as error:
            logger.error(f"\tCould not connect to {device}, Authentication failed\n")
        except (NetmikoTimeoutException) as error:
            logger.error(error)
            logger.error(f"\tFailed to connect to {device}\n")

        while True:
            logger.info("Would you like to show configurations (y/n).\n")
            user_input = input("").strip()
            if user_input == "y":
                for device in outputs:
                    output = outputs[device]
                    logger.info(f"Config for {device}:\n")
                    logger.info(outputs[device]+"/n/n")
                break
            elif user_input == "n":
                break
            else:
                logger.error("Wrong input\n")


        logger.info("Done\n"), 
        return True

    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y_%H-%M")



     # Creates the connection to the device.
    net_connect = ConnectHandler(**cisco_ios)
    net_connect.enable()
    # Gets the running configuration.
    output = net_connect.send_command("show run")
    # Gets and splits the hostname for the output file name.
    hostname = net_connect.send_command("show conf | i hostname")
    hostname = hostname.split()
    hostname = hostname[1]
    # Creates the file name, which is the hostname, and the date and time.
    fileName = hostname + "_" + dt_string
    # Creates the text file in the backup-config folder with the special name, and writes to it.
    backupFile = open("backup-config/" + fileName + ".txt", "w+")
    backupFile.write(output)
    print("Outputted to " + fileName + ".txt")