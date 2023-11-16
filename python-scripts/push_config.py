from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException
import os
from datetime import datetime
import time

def push_config(logger, Devices):
	"""Push configuration to devices."""
	for device in Devices:
		logger.info(f"Configuring {device}...")
		try:
			with ConnectHandler(**Devices[device]) as net_connect:
				logger.info(f"\tConnected to {device}\n")
				net_connect.enable()
				time.sleep(1)
				net_connect.config_mode()
				# load options of config files from backup-config folder and configs based on device (for backup-config folder and configs there is directory for each device) give user options to choose
				exit = False
				while True:
					logger.info(f"\tChoose one of available configuration files for {device}:")   
					config_files = {}
					for i, config_file in enumerate(os.listdir("configs/"+device+"/")):
						logger.info(f"\t{i+1}. - { 'configs/'+device+'/'+config_file }")
						config_files[config_file] = 'configs/'+device+'/'+config_file
					logger.info("\tTo choose configuration, type it's number or name. To stop choosing, type 'exit'.")
					logger.info("\tEnter configuration: ")
					user_input = input("\t").strip()
					if "".join(user_input) == "exit":
						exit = True
						break
					elif user_input.isdigit():
						if 0 < int(user_input) <= len(config_files):
							config = config_files[list(config_files.keys())[int(user_input)-1]]
							break
						else:
							logger.error("Wrong configuration number\n")
					elif user_input not in config_files:
						logger.error("Wrong configuration name\n")
					else:
						config = config_files[user_input]
						break

				if exit:
					break
				# load config file
				with open(config, 'r') as config_file:
					config_file.seek(0)
					config_file.close()
                
				#parse config file to config_commands
				config_commands = []
				for each_line in config_file.readlines():
					config_commands.append(each_line)
				
				net_connect.send_config_set(config_commands)
				logger.info(f"\tConfiguration pushed to {device}\n")

		except (TimeoutError) as error:
			logger.error(f"\tCould not connect to {device}, Connection timed out\n")
		except (NetmikoAuthenticationException) as error:
			logger.error(f"\tCould not connect to {device}, Authentication failed\n")
		except (NetmikoTimeoutException) as error:
			logger.error(error)
			logger.error(f"\tFailed to connect to {device}\n")



















net_connect = ConnectHandler(**AUTOLAB)
net_connect.enable()
time.sleep(1)
print ("\n\n ***** SSH connection was succesful ***** ")
net_connect.config_mode()

print ("\n\n ***Pushing the configuration on the device***")

config_file = open(user_path, 'r')
config_file.seek(0)

for each_line in config_file.readlines():
	net_connect.send_command_expect(each_line + '\n')
	time.sleep(1)

print ("\n ***Configuration loaded***")
print ("\n\n Aborting Connection with " + IP_ADD)
config_file.close()
net_connect.disconnect()
time.sleep(1)
print ("\n\n Connection closed")