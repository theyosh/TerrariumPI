#!/bin/bash

WHOAMI=`whoami`
if [ "${WHOAMI}" != "root" ]; then
  echo "Start TerrariumPI installation as user root"
  echo "sudo ./install.sh"
  exit 0
fi

BASEDIR=$(dirname $(readlink -nf $0))
SCRIPT_USER=`stat -c "%U" "${BASEDIR}"`
if [ "" == "${SCRIPT_USER}" ]; then
  SCRIPT_USER="pi"
fi

SCRIPT_GROUP=`id -gn ${SCRIPT_USER}`

VERSION=`grep ^__version__ "${BASEDIR}/terrariumPI.py" | cut -d' ' -f 3`
VERSION="${VERSION//\'/}"
INSTALLER_TITLE="TerrariumPI v. ${VERSION} (Python 3)"

CLEANUP_PACKAGES="wolfram sonic-pi openbox nodered java openjdk chromium-browser desktop-base gnome-desktop3-data libgnome-desktop epiphany-browser-data epiphany-browser nuscratch scratch wiringpi libreoffice"
PYTHON_LIBS="python3-pip python3-dev python3-venv"
OPENCV_PACKAGES="libopenexr23 libilmbase23 liblapack3 libatlas3-base"
APT_PACKAGES="screen git watchdog i2c-tools pigpio owserver sqlite3 ffmpeg sispmctl ntp libxslt1.1 ${OPENCV_PACKAGES} ${PYTHON_LIBS}"

PIP_MODULES=""
while IFS= read -r line; do
  [[ $line =~ ^#.* ]] && continue
  PIP_MODULES="${PIP_MODULES} ${line}"
done < requirements.txt

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

    debconf-apt-progress -- apt-get -y remove ${CLEANUP}
  ;;
esac

# Install required packages to get the terrarium software running

debconf-apt-progress -- apt-get -y autoremove
debconf-apt-progress -- apt-get -y update
debconf-apt-progress -- apt-get -y full-upgrade

#NOT_NEEDED="libftdi1-dev build-essential subversion libfreetype6-dev libjpeg-dev libasound2-dev libffi-dev libglib2.0-dev rng-tools libcblas3 libatlas3-base libgstreamer0.10-0 libgstreamer1.0-0 libilmbase12 libopenexr22 libgtk-3-0 libxml2-dev libxslt1-dev libgpiod2"

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

  if [ -f /etc/modules ]; then
    if [ `grep -ic "i2c-dev" /etc/modules` -eq 0 ]; then
      echo "i2c-dev" >> /etc/modules
    fi
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

# Disable serial debug to enable CO2 sensors
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
# if [ -f /etc/owfs.conf ]; then
#   sed -i.bak 's/^server: FAKE = DS18S20,DS2405/#server: FAKE = DS18S20,DS2405/' /etc/owfs.conf

#   if [ `grep -ic "server: device=/dev/i2c-1" /etc/owfs.conf` -eq 0 ]; then
#     echo "server: device=/dev/i2c-1" >> /etc/owfs.conf
#   fi
# fi

# if [ -f /etc/modprobe.d/raspi-blacklist.conf ]; then
#   sed -i.bak 's/^blacklist i2c-bcm2708/#blacklist i2c-bcm2708/' /etc/modprobe.d/raspi-blacklist.conf
# fi

# Increase swap file size
if [ -f /etc/dphys-swapfile ]; then
  sed -i 's/^CONF_SWAPSIZE=100/CONF_SWAPSIZE=512/' /etc/dphys-swapfile
fi

# Make sure pigpiod is started at boot, and that user PI can restart it with sudo command
echo "${SCRIPT_USER} ALL=(ALL) NOPASSWD: /usr/sbin/service pigpiod restart" > /etc/sudoers.d/terrariumpi
# Make rebooting from webinterface possible
echo "${SCRIPT_USER} ALL=(ALL) NOPASSWD: /sbin/reboot" >> /etc/sudoers.d/terrariumpi
echo "${SCRIPT_USER} ALL=(ALL) NOPASSWD: /sbin/shutdown" >> /etc/sudoers.d/terrariumpi
# http://denkovi.com/denkovi-relay-command-line-tool
echo "${SCRIPT_USER} ALL=(ALL) NOPASSWD: /usr/bin/java -jar 3rdparty/DenkoviRelayCommandLineTool/DenkoviRelayCommandLineTool.jar *" >> /etc/sudoers.d/terrariumpi

systemctl enable pigpiod 2>/dev/null

PROGRESS=0
# Update submodules if downloaded through tar or zip
(
cd "${BASEDIR}/"
cat <<EOF
XXX
$PROGRESS
Install required software\n\nInstalling base software ...
XXX
EOF


PROGRESS=$((PROGRESS + 1))
cat <<EOF
XXX
$PROGRESS
Install required software\n\nInstalling base software ...
XXX
EOF
git submodule init 2> /dev/null


PROGRESS=$((PROGRESS + 1))
cat <<EOF
XXX
$PROGRESS
Install required software\n\nInstalling base software ...
XXX
EOF
git submodule update 2> /dev/null

PROGRESS=$((PROGRESS + 1))
cat <<EOF
XXX
$PROGRESS
Install required software\n\nInstalling base software ...
XXX
EOF

# Create Python environment
cd "${BASEDIR}/"
python3 -m venv venv
source venv/bin/activate

# Install python modules inside the virtual env of Python
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
Install required software

Installing python${PYTHON} module ${MODULE_COUNTER} out of ${NUMBER_OF_MODULES}: ${PIP_MODULE} (attempt ${ATTEMPT}) ...
XXX
EOF
    pip install --upgrade ${PIP_MODULE}
    # > /dev/null 2>/dev/null

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

PROGRESS=99
cat <<EOF
XXX
$PROGRESS
Setting file rights ...
XXX
EOF

sed -e "s@^User=.*@User=${SCRIPT_USER}@" -e "s@^Group=.*@Group=${SCRIPT_GROUP}@" -e "s@^WorkingDirectory=.*@WorkingDirectory=${BASEDIR}@" -e "s@^ExecStart=.*@ExecStart=/home/pi/TerrariumPI/venv/bin/python /home/pi/TerrariumPI/terrariumPI.py@" "${BASEDIR}/contrib/terrariumpi.service.example" > /etc/systemd/system/terrariumpi.service
systemctl daemon-reload
systemctl enable terrariumpi

# Change the rights to the Pi user
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
for BLUETOOTH_HELPER in `ls venv/lib/python*/*-packages/bluepy/bluepy-helper`; do
  setcap 'cap_net_raw,cap_net_admin+eip' "${BLUETOOTH_HELPER}"
done

# Enable MOTD
if [ ! -h /etc/update-motd.d/05-terrariumpi ]; then
  ln -s "${BASEDIR}/motd.sh" /etc/update-motd.d/05-terrariumpi
fi

# Setup logging symlinks
su -c 'ln -s /dev/shm/terrariumpi.log "log/terrariumpi.log"' -s /bin/bash ${SCRIPT_USER}
su -c 'ln -s /dev/shm/terrariumpi.access.log "log/terrariumpi.access.log"' -s /bin/bash ${SCRIPT_USER}

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
