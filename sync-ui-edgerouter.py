from netmiko import ConnectHandler
# from getpass import getpass
from datetime import datetime


DEVICES = 'Devices.txt'
COMMANDS = 'Commands.txt'

start_time = datetime.now()

with open(DEVICES) as f:
    lines = [line for line in f.read().splitlines()]

for ip in lines:
    
    device = {
        'device_type': 'vyatta_vyos',
        'ip': ip,
        'username': 'ubnt',
        'password': 'ubnt',
        # 'password': getpass(),
        }

    with ConnectHandler(**device) as net_connect:
        print(f'\n---------- Configuring device {ip} ----------\n')
        output = net_connect.send_config_from_file(COMMANDS)
        print(output)
        print('\n-------------------- Done! --------------------\n')

run_time = datetime.now() - start_time
print(f'Elapsed time: {run_time}\n')
