import re, subprocess
from wifi import Scheme, Cell
from subprocess import Popen, PIPE, STDOUT
import os

def get_current_connected_wifi():
    current_ssid_regex = "wlan[0-9]     ESSID:\"(.*)\""
    output = subprocess.check_output(['iwgetid']).decode('utf-8')
    match = re.search(current_ssid_regex, output)
    if match is not None:
        return match.group(1)
    else:
        return None

def connect_to_wifi(ssid, passkey):
    p = Popen(['sudo', '/sbin/wpa_cli'], stdout=PIPE, stdin=PIPE, stderr=PIPE)
    p.communicate(input=('set_network 0 ssid "' + ssid  + '"').encode())
    p = Popen(['sudo', '/sbin/wpa_cli'], stdout=PIPE, stdin=PIPE, stderr=PIPE)
    p.communicate(input=('set_network 0 psk "' + passkey + '"').encode())
    p = Popen(['sudo', '/sbin/wpa_cli'], stdout=PIPE, stdin=PIPE, stderr=PIPE)
    p.communicate(input='enable_network 0'.encode())
    p = Popen(['sudo', '/sbin/wpa_cli'], stdout=PIPE, stdin=PIPE, stderr=PIPE)
    p.communicate(input='save_config'.encode())

    f = open('/etc/wpa_supplicant/wpa_supplicant.conf', 'r')
    wpa_supplicant = f.read()

    country_regex = "^country=[A-Z]{2}$"
    country_code_absent = re.match(country_regex, wpa_supplicant, re.MULTILINE) is None

    if country_code_absent:
        with open('/etc/wpa_supplicant/wpa_supplicant.conf', 'w') as modified: modified.write("country=BE\n" + wpa_supplicant)

    os.system('reboot')