# wpa_cli set_network 0 ssid "Fortress of Solitude 2.4GHz"
from subprocess import Popen, PIPE, STDOUT
import subprocess, re
import os

f = open('/etc/wpa_supplicant/wpa_supplicant.conf', 'r')
wpa_supplicant = f.read()
print(wpa_supplicant)

country_regex = "^country=[A-Z]{2}$"
country_code_absent = re.match(country_regex, wpa_supplicant, re.MULTILINE) is None

print(country_code_absent)

if country_code_absent:
    with open('/etc/wpa_supplicant/wpa_supplicant.conf', 'w') as modified: modified.write("country=BE\n" + wpa_supplicant)

p = Popen(['sudo', '/sbin/wpa_cli'], stdout=PIPE, stdin=PIPE, stderr=PIPE)
stdout_data = p.communicate(input='set_network 0 ssid "Fortress of Solitude 5GHz"'.encode())[0]
print(stdout_data)
p = Popen(['sudo', '/sbin/wpa_cli'], stdout=PIPE, stdin=PIPE, stderr=PIPE)
stdout_data = p.communicate(input='set_network 0 psk "fjxlg518"'.encode())[0]
print(stdout_data)
p = Popen(['sudo', '/sbin/wpa_cli'], stdout=PIPE, stdin=PIPE, stderr=PIPE)
stdout_data = p.communicate(input='enable_network 0'.encode())[0]
print(stdout_data)
p = Popen(['sudo', '/sbin/wpa_cli'], stdout=PIPE, stdin=PIPE, stderr=PIPE)
stdout_data = p.communicate(input='save_config'.encode())[0]
print(stdout_data)
os.system('reboot')