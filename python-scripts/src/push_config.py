from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException
import os
from datetime import datetime
import time

def push_config(logger, Devices):
	"""Push configuration to devices."""
	script_dir = os.path.dirname(os.path.abspath(__file__))

	for device in Devices:
		logger.info(f"Configuring {device} ...")
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
					config_dir = os.path.join(script_dir, "labaky/python-scripts/configs", device)
					for i, config_file in enumerate(os.listdir(config_dir)):
						logger.info(f"\t{i+1}. - {device+'/'+config_file }")
						config_files[config_file] = os.path.join(config_dir, config_file)
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
							logger.error("\tWrong configuration number\n")
					elif user_input not in config_files:
						logger.error("\tWrong configuration name\n")
					else:
						config = config_files[user_input]
						break

				if exit:
					break
				# load config file
				with open(config, 'r') as config_file:
					config_file.seek(0)
                
					#parse config file to config_commands
					config_commands = []
					for each_line in config_file.readlines():
						config_commands.append(each_line)
				
				#net_connect.send_config_set(config_commands, delay_factor=2)
				#net_connect.set_base_prompt()
				#logger.info(f"\tConfiguration pushed to {device}\n")

				for command in config_commands:
					net_connect.send_config_set([command], delay_factor=2)
					net_connect.set_base_prompt()
				logger.info(f"\tConfiguration pushed to {device}\n")

		except (TimeoutError, NetmikoTimeoutException) as error:
			logger.error(f"\tCould not connect to {device}, Connection timed out\n")
		except (NetmikoAuthenticationException) as error:
			logger.error(f"\tCould not connect to {device}, Authentication failed\n")


