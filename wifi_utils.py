import re, subprocess
from wifi import Scheme, Cell

def get_current_connected_wifi():
    current_ssid_regex = "wlan[0-9]     ESSID:\"(.*)\""
    output = subprocess.check_output(['iwgetid']).decode('utf-8')
    match = re.search(current_ssid_regex, output)
    if match is not None:
        return match.group(1)
    else:
        return None

def connect_to_wifi(ssid, passkey):
    print('connection to wifi ' + ssid)