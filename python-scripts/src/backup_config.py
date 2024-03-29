from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException
import os
from datetime import datetime

def backup_config(logger, Devices):
    """Backup configuration of devices."""
    if not os.path.exists('backup-config'):
        os.makedirs('backup-config')

    outputs = {}
    script_dir = os.path.dirname(os.path.abspath(__file__))
    backup_dir = os.path.join(script_dir, 'labaky/python-scripts/backup-config', device)

    for device in Devices:
        logger.info(f"Backing up {device} ...")
        logged = False
        try:
            with ConnectHandler(**Devices[device]) as net_connect:
                logger.info(f"\tConnected to {device}")
                net_connect.enable()

                # Gets the running configuration.
                output = net_connect.send_command("show run")
                outputs[device] = output
                logger.info("\tConfig retrieved")
                # Gets and splits the hostname for the output file name.
                hostname = net_connect.send_command("show run | i hostname").split()[1]

                # Creates the file name, which is the hostname, and the date and time.
                now = datetime.now()
                dt_string = now.strftime("%d-%m-%Y_%H-%M")
                fileName = hostname + "_" + dt_string
                # Creates the text file in the backup-config folder with the special name, and writes to it.
                if not os.path.exists(backup_dir):
                    os.makedirs(backup_dir)
                file_path = os.path.join(backup_dir, fileName + ".txt")
                with open(file_path, "w+") as backupFile:
                    backupFile.write(output)
                logger.info("\tOutputted to " + file_path + "\n")
                logged = True

        except (TimeoutError, NetmikoTimeoutException) as error:
            logger.error(f"\tCould not connect to {device}, Connection timed out\n")
        except (NetmikoAuthenticationException) as error:
            logger.error(f"\tCould not connect to {device}, Authentication failed\n")

    if logged:
        while True:
            logger.info("Would you like to show configurations (y/n).\n")
            user_input = input("").strip()
            if user_input == "y":
                for device in outputs:
                    output = outputs[device]
                    logger.info(f"Config for {device}:\n")
                    logger.info(outputs[device])
                    logger.info(f"\n\n")
                break
            elif user_input == "n":
                break
            else:
                logger.error("Wrong input\n")


    logger.info("\n\nDone\n"), 
    return True
