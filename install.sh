#!/bin/bash
BASEDIR=$(dirname $(readlink -nf $0))
SCRIPT_USER=`who -m | awk '{print $1}'`

WHOAMI=`whoami`
if [ "${WHOAMI}" != "root" ]; then
  echo "Start TerrariumPI installation as user root"
  echo "sudo ./install.sh"
  exit 0
fi

echo "TerrariumPI is going to be installed to run with user '${SCRIPT_USER}'."
PS3='Is this correct?: '
options=("yes" "no")
select opt in "${options[@]}"
do
    case $opt in
        "yes")
            echo "Installing..."
            break
            ;;
        "no")
           echo "Run the installer from the prefered user to run the software."
           exit 0
            break
            ;;
        *) echo invalid option;;
    esac
done


# Clean up first
aptitude -y remove wolfram-engine sonic-pi oracle-java8-jdk desktop-base gnome-desktop3-data libgnome-desktop-3-10 epiphany-browser-data epiphany-browser nuscratch scratch wiringpi
apt-get -y remove "^libreoffice.*"
apt-get -y autoremove

# Install required packages to get the terrarium software running
aptitude -y update
aptitude -y safe-upgrade
aptitude -y install libftdi1 screen python-imaging python-dateutil python-ow python-rpi.gpio python-psutil git subversion watchdog build-essential python-dev python-picamera python-opencv python-pip python-pigpio python-requests i2c-tools owfs ow-shell sqlite3 vlc-nox python-mediainfodll libasound2-dev

# Basic config:
#raspi-config
# Enable 1Wire en I2C during boot
if [ `grep -ic "#dtparam=i2c_arm=on" /boot/config.txt` -eq 1 ]; then
  sed -i.bak 's/^#dtparam=i2c_arm=on/dtparam=i2c_arm=on/' /boot/config.txt
fi
if [ `grep -ic "dtparam=i2c_arm=on" /boot/config.txt` -eq 0 ]; then
  echo "dtparam=i2c_arm=on" >> /boot/config.txt
fi

if [ `grep -ic "dtoverlay=w1-gpio" /boot/config.txt` -eq 0 ]; then
  echo "dtoverlay=w1-gpio" >> /boot/config.txt
fi

# Enable camera
if [ `grep -ic "gpu_mem=" /boot/config.txt` -eq 0 ]; then
  echo "gpu_mem=128" >> /boot/config.txt
fi

# Set the timezone
dpkg-reconfigure tzdata

# Update submodules if downloaded through tar or zip
cd "${BASEDIR}/"
git submodule init
git submodule update
cd "${BASEDIR}/.."

# Install multiple python modules
pip install --upgrade gevent
pip install --upgrade untangle
pip install --upgrade uptime
pip install --upgrade bottle
pip install --upgrade bottle_websocket
pip install --upgrade pylibftdi
pip install --upgrade pyalsaaudio
pip install --upgrade pyusb
pip install --upgrade pysispm

# Install https://pypi.python.org/pypi/pylibftdi
# Docu https://pylibftdi.readthedocs.io/
# Make sure that the normal Pi user can read and write to the usb driver
groupadd dialout 2> /dev/null
usermod -a -G dialout ${SCRIPT_USER} 2> /dev/null
echo 'SUBSYSTEMS=="usb", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6001", GROUP="dialout", MODE="0660"' > /etc/udev/rules.d/99-libftdi.rules
echo 'SUBSYSTEMS=="usb", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6014", GROUP="dialout", MODE="0660"' >> /etc/udev/rules.d/99-libftdi.rules


# https://pypi.python.org/pypi/pysispm
groupadd sispmctl 2> /dev/null
usermod -a -G sispmctl ${SCRIPT_USER} 2> /dev/null
echo 'SUBSYSTEM=="usb", ATTR{idVendor}=="04b4", ATTR{idProduct}=="fd10", GROUP="sispmctl", MODE="660"' > /etc/udev/rules.d/60-sispmctl.rules
echo 'SUBSYSTEM=="usb", ATTR{idVendor}=="04b4", ATTR{idProduct}=="fd11", GROUP="sispmctl", MODE="660"' >> /etc/udev/rules.d/60-sispmctl.rules
echo 'SUBSYSTEM=="usb", ATTR{idVendor}=="04b4", ATTR{idProduct}=="fd12", GROUP="sispmctl", MODE="660"' >> /etc/udev/rules.d/60-sispmctl.rules
echo 'SUBSYSTEM=="usb", ATTR{idVendor}=="04b4", ATTR{idProduct}=="fd13", GROUP="sispmctl", MODE="660"' >> /etc/udev/rules.d/60-sispmctl.rules

# Reload udev controll
udevadm control --reload-rules


# Install 1 Wire I2C stuff
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
cd "${BASEDIR}"

chown ${SCRIPT_USER}. .
chown ${SCRIPT_USER}. * -Rf

# Remove unneeded OWS services
update-rc.d -f owftpd remove
update-rc.d -f owfhttpd remove

if [ `grep -ic "start.sh" /etc/rc.local` -eq 0 ]; then
  sed -i.bak "s@^exit 0@# Starting TerrariumPI server\n${BASEDIR}/start.sh\n\nexit 0@" /etc/rc.local
fi

# Make sure GPIO group is available
groupadd gpio 2> /dev/null
usermod -a -G gpio ${SCRIPT_USER} 2> /dev/null

# Make sure pigpiod is started at boot, and that user PI can restart it with sudo command
echo "${SCRIPT_USER} ALL=(ALL) NOPASSWD: /usr/sbin/service pigpiod restart" > /etc/sudoers.d/terrariumpi
systemctl enable pigpiod

# We are done!
sync
echo "Instaltion is done. Please reboot once to get the 1Wire, I2C and Adafruit DHT libary working correctly"
