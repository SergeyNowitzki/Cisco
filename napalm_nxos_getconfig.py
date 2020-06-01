from concurrent.futures import ThreadPoolExecutor
from napalm import get_network_driver
from datetime import datetime
from itertools import repeat
import getpass
import json
import time

username = input('username: ')
password = getpass.getpass(prompt='Enter password: ')

devices = ['10.0.20.64', '10.0.21.48', '10.0.21.53', '10.0.21.57']

now = datetime.now()
str_time = now.strftime("%Y-%m-%d_%H:%M:%S")

start_msg = '===> {} Connection to device: {}'
received_msg = '<=== {} Received result from device: {}'


def connection_to_device(ip, user, psswd):
    print(start_msg.format(datetime.now().time(), ip))
    driver = get_network_driver('nxos')
    nxos = driver(ip, user, psswd)
    nxos.open()

    output = nxos.get_config(full=True)
    output_list = output['startup']. split('\n')


    for i in output_list:
        if 'switchname' in i:
            hostname = i.split()[1]

            result = output['startup']

            with open(f'config_{hostname}_{str_time}.ios', 'w') as f:
                f.write(result)
    nxos.close()

def threads_conn(function, devices, user, passwd, limit=4):
    with ThreadPoolExecutor(max_workers=limit) as executor:
        f_result = executor.map(function, devices, repeat(user), repeat(passwd))
    return list(f_result)

if __name__ == '__main__':
    threads_conn(connection_to_device, devices, username, password)
