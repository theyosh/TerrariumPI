#!/bin/bash
SCRIPT_USER=`who -m | awk '{print $1}'`
SCRIPT_USER_ID=`id -u ${SCRIPT_USER}`
if [ "" == "${SCRIPT_USER}" ]; then
  SCRIPT_USER="pi"
fi
PYTHON=2
if [ "${1}" == "3" ]; then
  PYTHON=3
fi

BASEDIR=$(dirname $(readlink -nf $0))
VERSION=`grep ^version "${BASEDIR}/defaults.cfg" | cut -d' ' -f 3`
LOGFILE="${BASEDIR}/log/terrariumpi.log"
ACCESSLOGFILE="${BASEDIR}/log/terrariumpi.access.log"
TMPFS="/run/user/${SCRIPT_USER_ID}"
INSTALLER_TITLE="TerrariumPI v. ${VERSION} (Python${PYTHON})"

CLEANUP_PACKAGES="wolfram sonic-pi openbox nodered java openjdk chromium-browser desktop-base gnome-desktop3-data libgnome-desktop epiphany-browser-data epiphany-browser nuscratch scratch wiringpi libreoffice"

PIP_MODULES="setuptools python-dateutil rpi.gpio psutil picamera pigpio requests gpiozero untangle uptime bottle bottle_websocket pylibftdi pyalsaaudio pyserial python-twitter python-pushover requests[socks] Adafruit-SHT31 bluepy pywemo pyownet emails mh-z19 icalendar melopero-amg8833 PCA9685-driver pyfiglet RPi.bme280"
if [ $PYTHON -eq 2 ]; then
  PIP_MODULES="${PIP_MODULES} iCalEvents==0.1.21 gevent==1.4.0 luma.core==1.12.0 luma.oled"
fi
if [ $PYTHON -eq 3 ]; then
  PIP_MODULES="${PIP_MODULES} gevent opencv-python-headless meross-iot==0.2.2.3 iCalEvents adafruit-circuitpython-sht31d mitemp_bt asyncio luma.oled poetry"
fi

if [ `grep -ic " buster " /etc/apt/sources.list` -eq 2 ]; then
  # Does not work on Buster, so we use the deb package version.... lets hope that it will stay working
  PIP_MODULES="${PIP_MODULES/opencv-python-headless/}"
fi

WHOAMI=`whoami`
if [ "${WHOAMI}" != "root" ]; then
  echo "Start TerrariumPI installation as user root"
  echo "sudo ./install.sh"
  exit 0
fi

#set -e

# Install dialog for further installation
if ! hash whiptail 2>/dev/null; then
  aptitude -y install whiptail
fi

clear

whiptail --backtitle "${INSTALLER_TITLE}" --title " TerrariumPI Installer " --yesno "TerrariumPI is going to be installed to run with user '${SCRIPT_USER}'. If this is not the right user stop the installation now!\n\nDo you want to continue?" 0 60

case $? in
  1|255) whiptail --backtitle "${INSTALLER_TITLE}"  --title " TerrariumPI Installer " --msgbox "TerrariumPI installation is aborted" 0 60
         exit 0
  ;;
esac

# Clean up first
whiptail --backtitle "${INSTALLER_TITLE}" --title " TerrariumPI Installer " --yesno "TerrariumPI is going to remove not needed programs in order to free up disk space and make future updates faster. All desktop software will be removed.\n\nDo you want to remove not needed programs?" 0 0

case $? in
  0) whiptail --backtitle "${INSTALLER_TITLE}"  --title " TerrariumPI Installer " --infobox "TerrariumPI is removing not needed programs" 0 0

    CLEANUP=""
    for PACKAGE in ${CLEANUP_PACKAGES}
    do
      CLEANUP="${CLEANUP} \"*${PACKAGE}*\""
    done

    debconf-apt-progress -- apt-get -y remove ${CLEANUP} && apt-get -y autoremove
#    debconf-apt-progress -- apt-get -y autoremove
  ;;
esac

# Remove previous python 2.X packages to make sure pip installed libraries are used
debconf-apt-progress -- apt-get -y remove owhttpd owftpd

# OWServer geeft problemen met install??? Of omdat config al aangepast is... maar als deez uit is, wil de apt install niet verder... Dus killen en manueel starten. dan verder install

# Install required packages to get the terrarium software running
PYTHON_LIBS="python-pip python-dev python-mediainfodll python-smbus python-pil python-opencv python-numpy python-lxml"
if [ $PYTHON -eq 3 ]; then
  PYTHON_LIBS="python3-pip python3-dev python3-mediainfodll python3-smbus python3-pil python3-opencv python3-numpy python3-lxml python3-venv"
fi

debconf-apt-progress -- apt-get -y autoremove
debconf-apt-progress -- apt-get -y update
debconf-apt-progress -- apt-get -y full-upgrade


APT_PACKAGES="libftdi1 screen git subversion watchdog build-essential i2c-tools pigpio owserver sqlite3 vlc-bin ffmpeg libfreetype6-dev libjpeg-dev \
  libasound2-dev sispmctl lshw libffi-dev ntp libglib2.0-dev rng-tools libcblas3 libatlas3-base libgstreamer0.10-0 libgstreamer1.0-0 libilmbase12 \
  libopenexr22 libgtk-3-0 libxml2-dev libxslt1-dev python-twisted python-zope.interface libgpiod2 $PYTHON_LIBS"

# libjasper1 -> Is alleen op Raspbarry ARM....

if [ `grep -ic " buster " /etc/apt/sources.list` -eq 2 ]; then
  # Remove not existing packages in Debian buster
  APT_PACKAGES="${APT_PACKAGES/libcblas3/}"
  APT_PACKAGES="${APT_PACKAGES/libilmbase12/}"
  APT_PACKAGES="${APT_PACKAGES/libopenexr22/}"
fi

debconf-apt-progress -- apt-get -y install $APT_PACKAGES

# Set the timezone
dpkg-reconfigure tzdata

# Basic config:
# Enable 1Wire en I2C during boot
if [ -f /boot/config.txt ]; then

  # Enable I2C
  if [ `grep -ic "^dtparam=i2c_arm=on" /boot/config.txt` -eq 0 ]; then
    echo "dtparam=i2c_arm=on" >> /boot/config.txt
  fi

  # Enable 1-Wire
  if [ `grep -ic "^dtoverlay=w1-gpio" /boot/config.txt` -eq 0 ]; then
    echo "dtoverlay=w1-gpio" >> /boot/config.txt
  fi

  # Enable camera
  if [ `grep -ic "^gpu_mem=" /boot/config.txt` -eq 0 ]; then
    echo "gpu_mem=128" >> /boot/config.txt
  fi

  if [ `grep -ic "^start_x=1" /boot/config.txt` -eq 0 ]; then
    echo "start_x=1" >> /boot/config.txt
  fi

  # Enable serial
  if [ `grep -ic "^enable_uart=1" /boot/config.txt` -eq 0 ]; then
    echo "enable_uart=1" >> /boot/config.txt
  fi

fi

if [ -f /boot/cmdline.txt ]; then
  sed -i "/boot/cmdline.txt" -e "s@console=ttyAMA0,[0-9]\+ @@"
  sed -i "/boot/cmdline.txt" -e "s@console=serial0,[0-9]\+ @@"
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
echo 'SUBSYSTEM=="usb", ATTR{idVendor}=="04b4", ATTR{idProduct}=="fd15", GROUP="sispmctl", MODE="660"' >> /etc/udev/rules.d/60-sispmctl.rules

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

# Increase swap file size
if [ -f /etc/dphys-swapfile ]; then
  sed -i.bak 's/^CONF_SWAPSIZE=100/CONF_SWAPSIZE=512/' /etc/dphys-swapfile
fi


# Make sure pigpiod is started at boot, and that user PI can restart it with sudo command
echo "${SCRIPT_USER} ALL=(ALL) NOPASSWD: /usr/sbin/service pigpiod restart" > /etc/sudoers.d/terrariumpi
# Make rebooting from webinterface possible
echo "${SCRIPT_USER} ALL=(ALL) NOPASSWD: /sbin/reboot" >> /etc/sudoers.d/terrariumpi
echo "${SCRIPT_USER} ALL=(ALL) NOPASSWD: /sbin/shutdown" >> /etc/sudoers.d/terrariumpi
# https://github.com/UedaTakeyuki/mh-z19/blob/master/pypi/mh_z19/__init__.py#L18
echo "${SCRIPT_USER} ALL=(ALL) NOPASSWD: /bin/systemctl stop serial-getty@ttyS0.service" >> /etc/sudoers.d/terrariumpi
echo "${SCRIPT_USER} ALL=(ALL) NOPASSWD: /bin/systemctl start serial-getty@ttyS0.service" >> /etc/sudoers.d/terrariumpi
echo "${SCRIPT_USER} ALL=(ALL) NOPASSWD: /bin/systemctl stop serial-getty@ttyAMA0.service" >> /etc/sudoers.d/terrariumpi
echo "${SCRIPT_USER} ALL=(ALL) NOPASSWD: /bin/systemctl start serial-getty@ttyAMA0.service" >> /etc/sudoers.d/terrariumpi
# http://denkovi.com/denkovi-relay-command-line-tool
echo "${SCRIPT_USER} ALL=(ALL) NOPASSWD: /usr/bin/java -jar DenkoviRelayCommandLineTool/DenkoviRelayCommandLineTool.jar *" >> /etc/sudoers.d/terrariumpi
# mh-z19 sensor
echo "${SCRIPT_USER} ALL=(ALL) NOPASSWD: /usr/bin/python -m mh_z19 --all" >> /etc/sudoers.d/terrariumpi
echo "${SCRIPT_USER} ALL=(ALL) NOPASSWD: /usr/bin/python2 -m mh_z19 --all" >> /etc/sudoers.d/terrariumpi
echo "${SCRIPT_USER} ALL=(ALL) NOPASSWD: /usr/bin/python3 -m mh_z19 --all" >> /etc/sudoers.d/terrariumpi

systemctl enable pigpiod

# Remove unneeded OWS services
update-rc.d -f owftpd remove
update-rc.d -f owfhttpd remove

PROGRESS=20
# Update submodules if downloaded through tar or zip
(
cd "${BASEDIR}/"
cat <<EOF
XXX
$PROGRESS
Install required software\n\nInstalling base software ...
XXX
EOF


PROGRESS=$((PROGRESS + 2))
cat <<EOF
XXX
$PROGRESS
Install required software\n\nInstalling base software ...
XXX
EOF
git submodule init > /dev/null


PROGRESS=$((PROGRESS + 2))
cat <<EOF
XXX
$PROGRESS
Install required software\n\nInstalling base software ...
XXX
EOF
git submodule update > /dev/null
cd "${BASEDIR}/.."

PROGRESS=$((PROGRESS + 2))
cat <<EOF
XXX
$PROGRESS
Install required software\n\nInstalling base software ...
XXX
EOF
cd "${BASEDIR}/gentelella"
git checkout 1.4.0 > /dev/null 2> /dev/null
cd "${BASEDIR}/.."

NUMBER_OF_MODULES=($PIP_MODULES)
NUMBER_OF_MODULES=${#NUMBER_OF_MODULES[@]}
MODULE_COUNTER=1
for PIP_MODULE in ${PIP_MODULES}
do
  PROGRESS=$((PROGRESS + 2))
  ATTEMPT=1
  MAX_ATTEMPTS=5
  while [ $ATTEMPT -le $MAX_ATTEMPTS ]
  do

    cat <<EOF
XXX
$PROGRESS
Install required software (some modules will take 5-10 min.)

Installing python${PYTHON} module ${MODULE_COUNTER} out of ${NUMBER_OF_MODULES}: ${PIP_MODULE} (attempt ${ATTEMPT}) ...
XXX
EOF
    if [ $PYTHON -eq 2 ]; then
      pip2 install -q --upgrade ${PIP_MODULE} > /dev/null 2>/dev/null

    elif [ $PYTHON -eq 3 ]; then
      pip3 install -q --upgrade ${PIP_MODULE} > /dev/null 2>/dev/null

    fi

    if [ $? -eq 0 ]; then
      # PIP install succeeded normally
      ATTEMPT=$((ATTEMPT + 99))
    else
      # PIP install failure... retry..
      ATTEMPT=$((ATTEMPT + 1))
    fi

  done

  MODULE_COUNTER=$((MODULE_COUNTER + 1))

done

PROGRESS=92
# Update submodules if downloaded through tar or zip
cd "${BASEDIR}/"

if [ $PYTHON -eq 3 ]; then
  # Remove pip numpy install that comes with an upgrade of another module. Does not work
  # Removing this will fallback to OS default
  pip3 uninstall -y -q numpy
fi

cd "${BASEDIR}/Bright-Pi"
if [ $PYTHON -eq 2 ]; then
  sudo python2 setup.py install
elif [ $PYTHON -eq 3 ]; then
  sudo python3 setup.py install
fi


cat <<EOF
XXX
$PROGRESS
Install required software (some modules will take 5-10 min.)

Installing python${PYTHON} module: Bright-Pi ...
XXX
EOF


PROGRESS=94
# Update submodules if downloaded through tar or zip
cd "${BASEDIR}/Adafruit_Python_DHT"
if [ $PYTHON -eq 2 ]; then
  sudo pip2 uninstall -y -q Adafruit_DHT 2> /dev/null
  sudo python2 setup.py install
elif [ $PYTHON -eq 3 ]; then
  sudo pip3 uninstall -y -q Adafruit_DHT 2> /dev/null
  sudo python3 setup.py install
fi


cat <<EOF
XXX
$PROGRESS
Install required software (some modules will take 5-10 min.)

Installing python${PYTHON} module: Adafruit_Python_DHT ...
XXX
EOF


PROGRESS=96
# Update submodules if downloaded through tar or zip
if [ $PYTHON -eq 3 ]; then
  cd "${BASEDIR}/python-kasa"
  poetry build
  sudo pip3 install -U dist/python_kasa-*.whl
fi


cat <<EOF
XXX
$PROGRESS
Install required software (some modules will take 5-10 min.)

Installing python${PYTHON} module: TP Link Kasa ...
XXX
EOF


PROGRESS=98
# Update submodules if downloaded through tar or zip
cd "${BASEDIR}/8relay-rpi/python/8relay"
if [ $PYTHON -eq 2 ]; then
  sudo python2 setup.py install
elif [ $PYTHON -eq 3 ]; then
  sudo python3 setup.py install
fi

cat <<EOF
XXX
$PROGRESS
Install required software (some modules will take 5-10 min.)

Installing python${PYTHON} module: TP Link Kasa ...
XXX
EOF


PROGRESS=99
cat <<EOF
XXX
$PROGRESS
Setting file rights ...
XXX
EOF
# Update submodules if downloaded through tar or zip
cd "${BASEDIR}/"
chown ${SCRIPT_USER}. .
chown ${SCRIPT_USER}. * -Rf

PROGRESS=100
cat <<EOF
XXX
$PROGRESS
Install required software\n\nDone! ...
XXX
EOF

sleep 1
) | whiptail --backtitle "${INSTALLER_TITLE}" --title " TerrariumPI Installer " --gauge "Install required software\n\nInstalling python module ${PIP_MODULE} ..." 0 78 0


# To run this as non-root run the following, https://github.com/marcelrv/miflora, https://github.com/IanHarvey/bluepy/issues/218
for BLUETOOTH_HELPER in `ls /usr/local/lib/python*/dist-packages/bluepy/bluepy-helper`; do
  setcap 'cap_net_raw,cap_net_admin+eip' "${BLUETOOTH_HELPER}"
done

# Move log file to temprorary mount
if grep -qs "${TMPFS} " /proc/mounts; then
  # TMPFS user dir is available....
  if ! [ -h "${LOGFILE}" ]; then
    # There is not a symlink to tmpfs partition
    if [ -f "${LOGFILE}" ]; then
      # There is an existing logfile already. Move it
      mv ${LOGFILE} ${TMPFS}
    fi
    su -c "ln -s ${TMPFS}/terrariumpi.log ${LOGFILE}" -s /bin/bash ${SCRIPT_USER}
  fi

  if ! [ -h "${ACCESSLOGFILE}" ]; then
    # There is not a symlink to tmpfs partition
    if [ -f "${ACCESSLOGFILE}" ]; then
      # There is an existing logfile already. Move it
      mv ${ACCESSLOGFILE} ${TMPFS}
    fi
    su -c "ln -s ${TMPFS}/terrariumpi.access.log ${ACCESSLOGFILE}" -s /bin/bash ${SCRIPT_USER}
  fi
fi

# Make TerrariumPI start during boot
if [ `grep -ic "start.sh" /etc/rc.local` -eq 0 ]; then
  sed -i.bak "s@^exit 0@# Starting TerrariumPI server\n${BASEDIR}/start.sh ${PYTHON}\n\nexit 0@" /etc/rc.local
fi

# Add a nice MOTD when you login
if [ -f /etc/motd ]; then
  mv /etc/motd /etc/motd.old
fi

if [ ! -h /etc/update-motd.d/05-terrariumpi ]; then
  ln -s /home/pi/TerrariumPI/motd.sh /etc/update-motd.d/05-terrariumpi
fi

# We are done!
sync

whiptail --backtitle "${INSTALLER_TITLE}" --title " TerrariumPI Installer " --yesno "TerrariumPI is installed/upgraded. To make sure that all is working please reboot.\n\nDo you want to reboot now?" 0 60

case $? in
  0)
  for SECONDS in {5..1}
  do
    echo "TerrariumPI installation is rebooting the Raspberry PI in ${SECONDS} seconds..."
    sleep 1
  done
  sync
  reboot
  ;;
esac

