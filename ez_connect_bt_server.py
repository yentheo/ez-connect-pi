import bluetooth
import threading
import json
import traceback
import asyncio
from wifi import Cell, Scheme
import re
import uuid
import subprocess
import sys
import time
from bt_utils import bluetooth_mac_address
from wifi_utils import get_current_connected_wifi, connect_to_wifi

print('test')

def start_bluetooth():
    subprocess.call(['hciconfig', 'hci0', 'piscan'])


def recv_timeout(the_socket, timeout=2):
    # make socket non blocking
    the_socket.setblocking(0)

    # total data partwise in an array
    total_data = []
    data = ''

    # beginning time
    begin = time.time()
    while 1:
        # if you got some data, then break after timeout
        if total_data and time.time()-begin > timeout:
            break

        # if you got no data at all, wait a little longer, twice the timeout
        elif time.time()-begin > timeout*2:
            break

        # recv something
        try:
            data = the_socket.recv(8192)
            if data:
                total_data.append(data.decode('utf-8'))
                # change the beginning time for measurement
                begin = time.time()
            else:
                # sleep for sometime to indicate a gap
                time.sleep(0.1)
        except bluetooth.BluetoothError as btError:
            if btError.errno != 11:
                raise
            else:
                pass

    # join all parts to make final string
    return ''.join(total_data)


def listening(client_socket):
    while True:
        data = recv_timeout(client_socket)
        if data:
            # try:
            message = json.loads(data)
            print('got message from client')
            if message['request'] == 'wifi_networks':
                current_connected_ssid = get_current_connected_wifi()
                networks = list(map(lambda cell: {
                    'name': cell.ssid,
                    'address': cell.address,
                    'isSecured': cell.encrypted,
                    'isConnected': current_connected_ssid == cell.ssid,
                    'quality': cell.quality,
                    'signal': cell.signal
                }, list(Cell.all('wlan0'))))
                load = json.dumps(
                    {'data': networks, 'response': 'wifi_networks'})
                client_socket.send(load)
            elif (message['request'] == 'connect_wifi'):
                connect_to_wifi(message['ssid'], message['passkey'])
            # except:
            #     print("Couldn't parse json", sys.exc_info()[0])
            #     print(data)


def start_accept(server_socket):
    try:
        print('starting accept')
        client, clientInfo = server_socket.accept()
        print('accepted client')
        time.sleep(.2)
        listening(client)
    except:
        start_accept(server_socket)


def start_server():
    print('starting server')
    port = 3
    backlog = 1
    s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    s.bind(('', 1))
    s.listen(backlog)
    start_accept(s)

threading.Thread(target=start_bluetooth).start()
time.sleep(5)
threading.Thread(target=start_server).start()
