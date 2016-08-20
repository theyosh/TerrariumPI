#!/bin/bash

# Clean up first
aptitude -y remove wolfram-engine sonic-pi oracle-java8-jdk desktop-base gnome-desktop3-data libgnome-desktop-3-10 epiphany-browser-data epiphany-browser nuscratch scratch wiringpi
apt-get -y remove "^libreoffice.*"
apt-get -y autoremove

# Basic config:
raspi-config

# Install required packages to get the terrarium software running
aptitude -y update
aptitude -y safe-upgrade
aptitude -y install libftdi1 screen python-imaging python-dateutil python-ow python-rpi.gpio python-psutil git subversion watchdog

# Manually install python pip, else you will get Python 2.6... :(
wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py
rm get-pip.py

# Install multiple python modules
pip install gevent untangle uptime bottle bottle_websocket

# Install https://pypi.python.org/pypi/pylibftdi
pip install pylibftdi
# Make sure that the normal Pi user can read and write to the usb driver
echo 'SUBSYSTEMS=="usb", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6001", GROUP="users", MODE="0660"' > /etc/udev/rules.d/99-libftdi.rules
echo 'SUBSYSTEMS=="usb", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6014", GROUP="users", MODE="0660"' >> /etc/udev/rules.d/99-libftdi.rules

# Install 1 Wire stuff
aptitude -y install i2c-tools owfs ow-shell
sed -i.bak 's/^server: FAKE = DS18S20,DS2405/#server: FAKE = DS18S20,DS2405/' /etc/owfs.conf
echo "server: device=/dev/i2c-1" >> /etc/owfs.conf

sed -i.bak 's/^blacklist i2c-bcm2708/#blacklist i2c-bcm2708/' /etc/modprobe.d/raspi-blacklist.conf
echo "i2c-dev" >> /etc/modules
modprobe i2c-bcm2708
modprobe i2c-dev

# Remove unneeded OWS services
update-rc.d -f owftpd remove
update-rc.d -f owfhttpd remove

# Set the timezone
dpkg-reconfigure tzdata

echo "Instaltion is done. Please reboot once to get the I2C working correctly"
