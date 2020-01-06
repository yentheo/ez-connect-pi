> sudo apt-get install libbluetooth-dev
> sudo pip3 install pybluez
> sudo pip3 install wifi

Edit files:
/etc/systemd/system/dbus-org.bluez.service

change line
ExecStart=/usr/lib/bluetooth/bluetoothd
to
ExecStart=/usr/lib/bluetooth/bluetoothd -C

add line
ExecStartPost=/usr/bin/sdptool add SP

> sudo systemctl daemon-reload
> sudo systemctl restart bluetooth.service