import re, subprocess

def bluetooth_mac_address():
    output = subprocess.check_output(['hciconfig']).decode('utf-8')
    bluetooth_mac_address_regex = "^\tBD Address: ((?:[A-F0-9]{2}:){5}[A-F0-9]{2}).*$"

    match = re.search(bluetooth_mac_address_regex, output, re.MULTILINE)
    if match is not None:
        return match.group(1)
    else:
        return None