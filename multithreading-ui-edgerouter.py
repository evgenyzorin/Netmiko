import re
from time import time, sleep
from netmiko import ConnectHandler
from concurrent.futures import ThreadPoolExecutor


DEVICES = "Devices.txt"
COMMANDS = "Commands.txt"


def get_devices():
    with open(DEVICES, "r") as file:
        devices = [device for device in file.read().splitlines()]
    return devices


def set_config(ip):
    device = {
              "ip": ip,
              "username": "ubnt",
              "password": "ubnt",
              "device_type": "vyatta_vyos",
             }

    with ConnectHandler(**device) as net_connect:
        raw_output = net_connect.send_config_from_file(COMMANDS)
        cleaned_output = re.sub(r"\x1B(?:[=>]|\[[0-9;]*[mK])", "", raw_output)

    print(f"\n---------- Configuring Device {ip} ----------\n")
    print(f"\n{cleaned_output}\n")

    return cleaned_output


def main(function, devices, workers):
    with ThreadPoolExecutor(workers) as executor:
        result = executor.map(function, devices)
    return list(result)


if __name__ == "__main__":
    t0 = time()
    main(set_config, get_devices(), 8)
    t1 = time() - t0
    print(f"\n----------- Elapsed time: {t1:.2f} sec -----------\n")
    sleep(60)
