#!/bin/bash
BASEDIR=$(dirname $(readlink -nf $0))
SCRIPT_USER=`who -m | awk '{print $1}'`
VERSION=`grep ^version defaults.cfg | cut -d' ' -f 3`

WHOAMI=`whoami`
if [ "${WHOAMI}" != "root" ]; then
  echo "Start TerrariumPI installation as user root"
  echo "sudo ./install.sh"
  exit 0
fi

# Stop at all errors
set -e

# Install dialog for further installation
if ! hash dialog 2>/dev/null; then
  aptitude -y install dialog
fi

dialog --aspect 40 --backtitle "TerrariumPI v. ${VERSION}" --title " TerrariumPI Installer " --yesno "TerrariumPI is going to be installed to run with user '${SCRIPT_USER}'.\n\nDo you want to continue?" 0 0

case $? in
  1|255) dialog --aspect 40 --backtitle "TerrariumPI v. ${VERSION}"  --title " TerrariumPI Installer " --infobox "TerrariumPI installation is aborted" 0 0
         sleep 2
         exit 0
  ;;
esac

# Clean up first
echo "10\n" | dialog --aspect 40 --backtitle "TerrariumPI v. ${VERSION}" --title " TerrariumPI Installer " --gauge "Cleaning unwanted programs..." 0 0

apt-get -q -y remove wolfram-engine sonic-pi oracle-java8-jdk desktop-base gnome-desktop3-data libgnome-desktop-3-10 epiphany-browser-data epiphany-browser nuscratch scratch wiringpi > /dev/null

echo "40\n" | dialog --aspect 40 --backtitle "TerrariumPI v. ${VERSION}" --title " TerrariumPI Installer " --gauge "Cleaning unwanted programs..." 0 0

apt-get -q -y remove "^libreoffice.*" > /dev/null

echo "70\n" | dialog --aspect 40 --backtitle "TerrariumPI v. ${VERSION}" --title " TerrariumPI Installer " --gauge "Cleaning unwanted programs..." 0 0

apt-get -q -y autoremove > /dev/null

echo "100\n" | dialog --aspect 40 --backtitle "TerrariumPI v. ${VERSION}" --title " TerrariumPI Installer " --gauge "Cleaning unwanted programs..." 0 0

# Install required packages to get the terrarium software running
echo "10\n" | dialog --aspect 40 --backtitle "TerrariumPI v. ${VERSION}" --title " TerrariumPI Installer " --gauge "Install required software..." 0 0
apt-get -q -y update > /dev/null
echo "20\n" | dialog --aspect 40 --backtitle "TerrariumPI v. ${VERSION}" --title " TerrariumPI Installer " --gauge "Install required software..." 0 0
apt-get -q -y full-upgrade > /dev/null
echo "40\n" | dialog --aspect 40 --backtitle "TerrariumPI v. ${VERSION}" --title " TerrariumPI Installer " --gauge "Install required software..." 0 0
apt-get -q -y install libftdi1 screen python-imaging python-dateutil python-ow python-rpi.gpio python-psutil git subversion watchdog build-essential python-dev python-picamera python-opencv python-pip python-pigpio python-requests i2c-tools owfs ow-shell sqlite3 vlc-nox python-mediainfodll libasound2-dev sispmctl python-gpiozero lshw > /dev/null

echo "60\n" | dialog --aspect 40 --backtitle "TerrariumPI v. ${VERSION}" --title " TerrariumPI Installer " --gauge "Install required software..." 0 0

# Update submodules if downloaded through tar or zip
cd "${BASEDIR}/"
git submodule init > /dev/null
git submodule update > /dev/null
cd "${BASEDIR}/.."

echo "70\n" | dialog --aspect 40 --backtitle "TerrariumPI v. ${VERSION}" --title " TerrariumPI Installer " --gauge "Install required software..." 0 0

PROGRESS=70
PIP_MODULES="gevent untangle uptime bottle bottle_websocket pylibftdi pyalsaaudio"
for PIP_MODULE in ${PIP_MODULES}
do
  PROGRESS=$((PROGRESS + 2))
  echo "${PROGRESS}\n" | dialog --aspect 40 --backtitle "TerrariumPI v. ${VERSION}" --title " TerrariumPI Installer " --gauge "Install required software..." 0 0
  pip install -q --upgrade ${PIP_MODULE}
done

# Install Adafruit DHT Python library
PROGRESS=$((PROGRESS + 2))
echo "${PROGRESS}\n" | dialog --aspect 40 --backtitle "TerrariumPI v. ${VERSION}" --title " TerrariumPI Installer " --gauge "Install required software..." 0 0
if [ ! -d Adafruit_Python_DHT ]
then
  git clone https://github.com/adafruit/Adafruit_Python_DHT.git >/dev/null
fi

PROGRESS=$((PROGRESS + 2))
echo "${PROGRESS}\n" | dialog --aspect 40 --backtitle "TerrariumPI v. ${VERSION}" --title " TerrariumPI Installer " --gauge "Install required software..." 0 0
cd Adafruit_Python_DHT
git pull  > /dev/null

PROGRESS=$((PROGRESS + 2))
echo "${PROGRESS}\n" | dialog --aspect 40 --backtitle "TerrariumPI v. ${VERSION}" --title " TerrariumPI Installer " --gauge "Install required software..." 0 0
python setup.py -q install 2> /dev/null
cd "${BASEDIR}"

chown ${SCRIPT_USER}. .
chown ${SCRIPT_USER}. * -Rf

echo "100\n" | dialog --aspect 40 --backtitle "TerrariumPI v. ${VERSION}" --title " TerrariumPI Installer " --gauge "Install required software..." 0 0


# Basic config:
# Enable 1Wire en I2C during boot
if [ -f /boot/config.txt ]; then

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

fi

# Create needed groups
groupadd -f dialout 2> /dev/null
groupadd -f sispmctl 2> /dev/null
groupadd -f gpio 2> /dev/null
# Add user to all groupds
usermod -a -G dialout,sispmctl,gpio ${SCRIPT_USER} 2> /dev/null


# Docu https://pylibftdi.readthedocs.io/
# Make sure that the normal Pi user can read and write to the usb driver
echo 'SUBSYSTEMS=="usb", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6001", GROUP="dialout", MODE="0660"' > /etc/udev/rules.d/99-libftdi.rules
echo 'SUBSYSTEMS=="usb", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6014", GROUP="dialout", MODE="0660"' >> /etc/udev/rules.d/99-libftdi.rules

# https://pypi.python.org/pypi/pysispm
echo 'SUBSYSTEM=="usb", ATTR{idVendor}=="04b4", ATTR{idProduct}=="fd10", GROUP="sispmctl", MODE="660"' > /etc/udev/rules.d/60-sispmctl.rules
echo 'SUBSYSTEM=="usb", ATTR{idVendor}=="04b4", ATTR{idProduct}=="fd11", GROUP="sispmctl", MODE="660"' >> /etc/udev/rules.d/60-sispmctl.rules
echo 'SUBSYSTEM=="usb", ATTR{idVendor}=="04b4", ATTR{idProduct}=="fd12", GROUP="sispmctl", MODE="660"' >> /etc/udev/rules.d/60-sispmctl.rules
echo 'SUBSYSTEM=="usb", ATTR{idVendor}=="04b4", ATTR{idProduct}=="fd13", GROUP="sispmctl", MODE="660"' >> /etc/udev/rules.d/60-sispmctl.rules

# Reload udev controll
udevadm control --reload-rules

# Install 1 Wire I2C stuff
if [ -f /etc/owfs.conf ]; then
  sed -i.bak 's/^server: FAKE = DS18S20,DS2405/#server: FAKE = DS18S20,DS2405/' /etc/owfs.conf

  if [ `grep -ic "server: device=/dev/i2c-1" /etc/owfs.conf` -eq 0 ]; then
    echo "server: device=/dev/i2c-1" >> /etc/owfs.conf
  fi
fi

if [ -f /etc/modprobe.d/raspi-blacklist.conf ]; then
  sed -i.bak 's/^blacklist i2c-bcm2708/#blacklist i2c-bcm2708/' /etc/modprobe.d/raspi-blacklist.conf
fi

if [ -f /etc/modules ]; then
  if [ `grep -ic "i2c-dev" /etc/modules` -eq 0 ]; then
    echo "i2c-dev" >> /etc/modules
  fi
fi

# Make sure pigpiod is started at boot, and that user PI can restart it with sudo command
echo "${SCRIPT_USER} ALL=(ALL) NOPASSWD: /usr/sbin/service pigpiod restart" > /etc/sudoers.d/terrariumpi
systemctl enable pigpiod

# Remove unneeded OWS services
update-rc.d -f owftpd remove
update-rc.d -f owfhttpd remove

# Set the timezone
dpkg-reconfigure tzdata

# Make TerrariumPI start during boot
if [ `grep -ic "start.sh" /etc/rc.local` -eq 0 ]; then
  sed -i.bak "s@^exit 0@# Starting TerrariumPI server\n${BASEDIR}/start.sh\n\nexit 0@" /etc/rc.local
fi

# We are done!
sync

dialog --aspect 40 --backtitle "TerrariumPI v. ${VERSION}" --title " TerrariumPI Installer " --yesno "TerrariumPI is installed/upgraded. To make sure that all is working please reboot.\n\nDo you want to reboot now?" 0 0

case $? in
  0)
  for SECONDS in {5..1}
  do
    dialog --aspect 40 --backtitle "TerrariumPI v. ${VERSION}"  --title " TerrariumPI Installer " --infobox "TerrariumPI installation is rebooting the Raspberry PI in ${SECONDS} seconds..." 0 0
         sleep 1
  done
  sync
  reboot
  ;;
esac
