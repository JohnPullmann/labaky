from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException
from getpass import getpass

protocol = None	
while protocol != "ssh" and protocol != "telnet":
    protocol = input("Enter the protocol to use ('ssh'/'telnet'): ")

username = None
if protocol == "ssh":
    username = input("Enter your SSH username: ")
    device_type = "cisco_ios"
elif protocol == "telnet":
    device_type = "cisco_ios_telnet"

password = getpass("Enter password:")
priv_password = getpass("Enter privilage mode password:")

Switch3 = {
    "host": "192.168.0.30",
    "device_type": device_type,
    "username": username,
    "password": password,
    'secret': priv_password,
    "global_delay_factor": 2,
}
Localhost_Switch = {
    "host": "192.168.247.129",
    "port": "5000",
    "username": "Admin",
    "password": password,
    "device_type": "extreme_exos_telnet",
}



with ConnectHandler(**Switch3) as net_connect:
    #print(net_connect.find_prompt())
    #net_connect.enable()

    output = net_connect.send_command("show user")
    print(f"Show user output:\n{output}")