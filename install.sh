#!/bin/bash
BASEDIR=$(dirname $(readlink -nf $0))

WHOAMI=`whoami`
if [ "${WHOAMI}" != "root" ]; then
  echo "Start TerrariumPI installation as user root"
  exit 0
fi

# Clean up first
aptitude -y remove wolfram-engine sonic-pi oracle-java8-jdk desktop-base gnome-desktop3-data libgnome-desktop-3-10 epiphany-browser-data epiphany-browser nuscratch scratch wiringpi
apt-get -y remove "^libreoffice.*"
apt-get -y autoremove

# Install required packages to get the terrarium software running
aptitude -y update
aptitude -y safe-upgrade
aptitude -y install libftdi1 screen python-imaging python-dateutil python-ow python-rpi.gpio python-psutil git subversion watchdog build-essential python-dev python-picamera python-opencv python-pip python-pigpio i2c-tools owfs ow-shell sqlite3

# Basic config:
raspi-config

# Set the timezone
dpkg-reconfigure tzdata

if [ `ls -l gentelella | grep -v ^t | wc -l` -eq 0 ]; then
  # Manual get Gentelella bootstrap 3 template
  git clone https://github.com/puikinsh/gentelella.git gentelella
fi

cd gentelella
git pull
cd "${BASEDIR}/.."

# Install multiple python modules
pip install --upgrade gevent untangle uptime bottle bottle_websocket pylibftdi

# Install https://pypi.python.org/pypi/pylibftdi
# Docu https://pylibftdi.readthedocs.io/
# Make sure that the normal Pi user can read and write to the usb driver
echo 'SUBSYSTEMS=="usb", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6001", GROUP="dialout", MODE="0660"' > /etc/udev/rules.d/99-libftdi.rules
echo 'SUBSYSTEMS=="usb", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6014", GROUP="dialout", MODE="0660"' >> /etc/udev/rules.d/99-libftdi.rules

# Install 1 Wire stuff
sed -i.bak 's/^server: FAKE = DS18S20,DS2405/#server: FAKE = DS18S20,DS2405/' /etc/owfs.conf

if [ `grep -ic "server: device=/dev/i2c-1" /etc/owfs.conf` -eq 0 ]; then
  echo "server: device=/dev/i2c-1" >> /etc/owfs.conf
fi

sed -i.bak 's/^blacklist i2c-bcm2708/#blacklist i2c-bcm2708/' /etc/modprobe.d/raspi-blacklist.conf
if [ `grep -ic "i2c-dev" /etc/modules` -eq 0 ]; then
  echo "i2c-dev" >> /etc/modules
fi

modprobe i2c-bcm2708
modprobe i2c-dev

# Install Adafruit DHT Python library
if [ ! -d Adafruit_Python_DHT ]
then
  git clone https://github.com/adafruit/Adafruit_Python_DHT.git
fi
cd Adafruit_Python_DHT
git pull
sudo python setup.py install
cd "${BASEDIR}/.."

# Remove unneeded OWS services
update-rc.d -f owftpd remove
update-rc.d -f owfhttpd remove

if [ `grep -ic "start.sh" /etc/rc.local` -eq 0 ]; then
  sed -i.bak "s@^exit 0@# Starting TerrariumPI server\n${BASEDIR}/start.sh\n\nexit 0@" /etc/rc.local
fi

# Make sure GPIO group is available
groupadd gpio 2> /dev/null
usermod -a -G gpio pi 2> /dev/null

# Make sure pigpiod is started at boot, and that user PI can restart it with sudo command
echo "pi ALL=(ALL) NOPASSWD: /usr/sbin/service pigpiod restart" > /etc/sudoers.d/terrariumpi
systemctl enable pigpiod

# We are done!
sync
echo "Instaltion is done. Please reboot once to get the I2C and Adafruit DHT libary working correctly"
