#!/bin/bash
# https://wiki.bash-hackers.org/syntax/pattern#extended_pattern_language
shopt -s extglob

BASEDIR=$(dirname $(readlink -nf "$0"))
VERSION=$(grep ^__version__ "${BASEDIR}/terrariumPI.py" | cut -d' ' -f 3)
VERSION="${VERSION//\'/}"
INSTALLER_TITLE="TerrariumPI v. ${VERSION} (Python 3)"
PI_ZERO=$(grep -iEc "model\s+: .*Pi Zero" /proc/cpuinfo)
BUSTER_OS=$(grep -ic "^VERSION_CODENAME=buster" /etc/os-release)

WHOAMI=$(whoami)
if [ "${WHOAMI}" != "root" ]; then
  echo "Start TerrariumPI installation as user root"
  echo "sudo ./install.sh"
  exit 0
fi

if [ "${PI_ZERO}" -eq 1 ]; then
  # Pi Zero needs root user to run
  SCRIPT_USER="root"
else
  SCRIPT_USER=$(stat -c "%U" "${BASEDIR}")
  if [ "" == "${SCRIPT_USER}" ]; then
    SCRIPT_USER="pi"
  fi
fi

SCRIPT_GROUP="$(id -gn ${SCRIPT_USER})"

CLEANUP_PACKAGES="wolfram sonic-pi openbox nodered chromium-browser desktop-base gnome-desktop3-data libgnome-desktop epiphany-browser-data epiphany-browser nuscratch scratch wiringpi libreoffice"
PYTHON_LIBS="python3-pip python3-dev python3-venv"
OPENCV_PACKAGES="libopenexr23 libilmbase23 liblapack3 libatlas3-base"
# For Bullseye we need libopenexr25 and libilmbase25
if [ "${BUSTER_OS}" -eq 0 ]; then
  OPENCV_PACKAGES="libopenexr25 libilmbase25 liblapack3 libatlas3-base"
fi
APT_PACKAGES="bc screen git watchdog i2c-tools pigpio sqlite3 ffmpeg sispmctl ntp libxslt1.1 libglib2.0-dev ${OPENCV_PACKAGES} ${PYTHON_LIBS}"

PIP_MODULES=""
while IFS= read -r line; do
  [[ $line =~ ^#.* ]] && continue
  PIP_MODULES="${PIP_MODULES} ${line}"
done < requirements.txt

if [ "${PI_ZERO}" -eq 1 ]; then
  # Pi Zero needs some fixed python modules
  PIP_MODULES="${PIP_MODULES//gevent==+([^ ])/gevent==21.8.0}"
  PIP_MODULES="${PIP_MODULES//bcrypt==+([^ ])/bcrypt==3.2.2}"

  if [ "${BUSTER_OS}" -eq 1 ]; then
    PIP_MODULES="${PIP_MODULES//opencv-python-headless==+([^ ])/opencv-python-headless==4.5.4.60}"
    PIP_MODULES="${PIP_MODULES//cryptography==+([^ ])/cryptography==37.0.4}"
  else
    PIP_MODULES="${PIP_MODULES//opencv-python-headless==+([^ ])/opencv-python-headless==4.5.3.56}"
  fi

  PIP_MODULES="${PIP_MODULES//numpy==+([^ ])/numpy==1.21.4}"
  PIP_MODULES="${PIP_MODULES} lxml==4.6.4"
fi

# Debian buster does not like numpy or cryptography .... :(
if [ "${BUSTER_OS}" -eq 1 ]; then
  PIP_MODULES="${PIP_MODULES//numpy==+([^ ])/numpy==1.21.4}"
fi

#set -ex

# Install dialog for further installation
if ! hash whiptail 2>/dev/null; then
  aptitude -y install whiptail
fi

clear

# OS version check

# if [ ${BUSTER_OS} -eq 0 ]; then
#   whiptail --backtitle "${INSTALLER_TITLE}" --title " TerrariumPI Installer " --yesno "TerrariumPI is not Raspbian Bullseye OS compatible. You can install it, but the Raspberry PI cameras are not working.\nDownload the old Legacy OS Raspbian Buster\n\nDo you want to continue?" 0 60

#   case $? in
#     1|255) whiptail --backtitle "${INSTALLER_TITLE}"  --title " TerrariumPI Installer " --msgbox "TerrariumPI installation is aborted" 0 60
#       echo "TerrariumPI ${VERSION} is supported on Buster OS (Legacy OS)"
#       echo "Download from: https://www.raspberrypi.com/software/operating-systems/#raspberry-pi-os-legacy"
#       exit 0
#     ;;
#   esac
# fi

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
debconf-apt-progress -- apt-get -y install ${APT_PACKAGES}

# Set the timezone
dpkg-reconfigure tzdata

# Basic config:
# Enable 1Wire en I2C during boot
if [ -f /boot/config.txt ]; then

  # Enable I2C
  if [ $(grep -ic "^dtparam=i2c_arm=on" /boot/config.txt) -eq 0 ]; then
    echo "dtparam=i2c_arm=on" >> /boot/config.txt
  fi

  if [ -f /etc/modules ]; then
    if [ $(grep -ic "i2c-dev" /etc/modules) -eq 0 ]; then
      echo "i2c-dev" >> /etc/modules
    fi
  fi

  # Enable 1-Wire
  if [ $(grep -ic "^dtoverlay=w1-gpio" /boot/config.txt) -eq 0 ]; then
    echo "dtoverlay=w1-gpio" >> /boot/config.txt
  fi

  # Enable camera
  if [ $(grep -ic "^gpu_mem=" /boot/config.txt) -eq 0 ]; then
    echo "gpu_mem=128" >> /boot/config.txt
  fi

  if [ $(grep -ic "^start_x=1" /boot/config.txt) -eq 0 ]; then
    echo "start_x=1" >> /boot/config.txt
  fi

  # Bullseye legacy camera
  sed -i "/boot/config.txt" -e "s@^[ ]*dtoverlay=vc4-kms-v3d@#dtoverlay=vc4-kms-v3d@"
  sed -i "/boot/config.txt" -e "s@^[ ]*camera_auto_detect=.*@@"

  if [ $(grep -ic "^dtoverlay=vc4-fkms-v3d" /boot/config.txt) -eq 0 ]; then
    sed -i "/boot/config.txt" -e "s@^\[pi4\]@\[pi4\]\ndtoverlay=vc4-fkms-v3d@"
  fi

  # Enable serial
  if [ $(grep -ic "^enable_uart=1" /boot/config.txt) -eq 0 ]; then
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
usermod -a -G dialout,sispmctl,gpio "${SCRIPT_USER}" 2> /dev/null

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

# Increase swap file size
if [ -f /etc/dphys-swapfile ]; then
  sed -i 's/^CONF_SWAPSIZE=100/CONF_SWAPSIZE=512/' /etc/dphys-swapfile
fi

# Make sure pigpiod is started at boot, and that user PI can restart it with sudo command
echo "${SCRIPT_USER} ALL=(ALL) NOPASSWD: /usr/sbin/service pigpiod restart" > /etc/sudoers.d/020_terrariumpi
# Make rebooting from webinterface possible
echo "${SCRIPT_USER} ALL=(ALL) NOPASSWD: /sbin/reboot" >> /etc/sudoers.d/020_terrariumpi
echo "${SCRIPT_USER} ALL=(ALL) NOPASSWD: /sbin/shutdown" >> /etc/sudoers.d/020_terrariumpi
# http://denkovi.com/denkovi-relay-command-line-tool
echo "${SCRIPT_USER} ALL=(ALL) NOPASSWD: /usr/bin/java -jar 3rdparty/DenkoviRelayCommandLineTool/DenkoviRelayCommandLineTool.jar *" >> /etc/sudoers.d/020_terrariumpi

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
Install required software\n\nInstalling sub modules ...
XXX
EOF
git submodule init 2> /dev/null

PROGRESS=$((PROGRESS + 1))
cat <<EOF
XXX
$PROGRESS
Install required software\n\nUpdating sub modules ...
XXX
EOF
git submodule update 2> /dev/null

PROGRESS=$((PROGRESS + 1))
cat <<EOF
XXX
$PROGRESS
Install required software\n\nSetting up Python 3 environment ...
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
MODULE_OFFSET=${PROGRESS}
MODULE_MAX=86
for PIP_MODULE in ${PIP_MODULES}
do
  PROGRESS=$(printf '%.*f\n' 0 $(echo "scale=2; ( ${MODULE_COUNTER} * ((${MODULE_MAX} - ${MODULE_OFFSET}) / ${NUMBER_OF_MODULES}) ) + ${MODULE_OFFSET}" | bc -l))
  ATTEMPT=1
  MAX_ATTEMPTS=5
  IFS='/' read -ra MODULE_NAME <<< "${PIP_MODULE}"
  MODULE_NAME=${MODULE_NAME[-1]}
  IFS='==' read -ra MODULE_NAME <<< "${MODULE_NAME}"
  MODULE_NAME=${MODULE_NAME[0]}

  while [ $ATTEMPT -le $MAX_ATTEMPTS ]
  do

    cat <<EOF
XXX
$PROGRESS
Install required software

Installing python${PYTHON} module ${MODULE_COUNTER} out of ${NUMBER_OF_MODULES}: ${MODULE_NAME} (attempt ${ATTEMPT}) ...
XXX
EOF
    pip install --upgrade "${PIP_MODULE}" 2> /dev/null

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

PROGRESS=$((MODULE_MAX + 3))
cat <<EOF
XXX
$PROGRESS
Finishing installation

Setting file rights ...
XXX
EOF

# Change the rights to the Pi user
cd "${BASEDIR}/"

# Updates for docker support
# Create data directory
mkdir -p data

# Custom logging
if [ -f logging.custom.conf ]; then
  mv logging.custom.conf log
fi

# Calendar
if [ -f calendar.ics ]; then
  mv calendar.ics data
fi

# Database
if [ -f terrariumpi.db ]; then
  mv terrariumpi.db* data
fi

# Set file owner rights
chown "${SCRIPT_USER}". .
chown "${SCRIPT_USER}". * -Rf

sync


PROGRESS=$((PROGRESS + 2))
cat <<EOF
XXX
$PROGRESS
Finishing installation

Enable system startup services ...
XXX
EOF

sed -e "s@^User=.*@User=${SCRIPT_USER}@" -e "s@^Group=.*@Group=${SCRIPT_GROUP}@" -e "s@^WorkingDirectory=.*@WorkingDirectory=${BASEDIR}@" -e "s@^ExecStart=.*@ExecStart=${BASEDIR}/venv/bin/python ${BASEDIR}/terrariumPI.py@" "${BASEDIR}/contrib/terrariumpi.service.example" > /etc/systemd/system/terrariumpi.service
sed -ie "s@.*RemoveIPC=.*@RemoveIPC=false@" /etc/systemd/logind.conf
systemctl daemon-reload
systemctl enable terrariumpi


PROGRESS=$((PROGRESS + 2))
cat <<EOF
XXX
$PROGRESS
Finishing installation

Enable bluetooth for ${SCRIPT_USER} user ...
XXX
EOF

# To run this as non-root run the following, https://github.com/marcelrv/miflora, https://github.com/IanHarvey/bluepy/issues/218
for BLUETOOTH_HELPER in $(ls venv/lib/python*/*-packages/bluepy/bluepy-helper); do
  setcap 'cap_net_raw,cap_net_admin+eip' "${BLUETOOTH_HELPER}"
done


PROGRESS=$((PROGRESS + 2))
cat <<EOF
XXX
$PROGRESS
Finishing installation

Enable Message Of The Day ...
XXX
EOF

# Enable MOTD
if [ ! -h /etc/update-motd.d/05-terrariumpi ]; then
  ln -s "${BASEDIR}/motd.sh" /etc/update-motd.d/05-terrariumpi
fi

PROGRESS=$((PROGRESS + 2))
cat <<EOF
XXX
$PROGRESS
Finishing installation

Setup logging ...
XXX
EOF

# Setup logging symlinks
if [ ! -h log/terrariumpi.log ]; then
  su -c 'ln -s /dev/shm/terrariumpi.log log/terrariumpi.log' -s /bin/bash "${SCRIPT_USER}"
fi
if [ ! -h log/terrariumpi.access.log ]; then
  su -c 'ln -s /dev/shm/terrariumpi.access.log log/terrariumpi.access.log' -s /bin/bash "${SCRIPT_USER}"
fi

PROGRESS=100
cat <<EOF
XXX
$PROGRESS
Install required software\n\nDone! ...
XXX
EOF

# We are done!
sync
sleep 1
) | whiptail --backtitle "${INSTALLER_TITLE}" --title " TerrariumPI Installer " --gauge "Install required software\n\nInstalling python modules ..." 0 78 0


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
