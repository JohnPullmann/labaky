import telnetlib

# Set the IP address and port of your GNS3 virtual switch
host = "192.168.247.129"
port = 5000  # Typically 23 for telnet

# Telnet username and password (if applicable)
username = ""
password = ""

# Connect to the virtual switch
tn = telnetlib.Telnet(host, port)

# Optionally, login if required
if username:
    tn.read_until(b"Username: ")
    tn.write(username.encode('ascii') + b"\n")

if password:
    tn.read_until(b"Password: ")
    tn.write(password.encode('ascii') + b"\n")

# Now you are connected and can send commands
tn.write(b"show session\n")

# Read the response
output = tn.read_until(b"prompt")  # Adjust "prompt" to match your switch's prompt
print(output.decode('ascii'))

# Close the connection
tn.close()