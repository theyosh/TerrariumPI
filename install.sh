#!/bin/bash
# https://wiki.bash-hackers.org/syntax/pattern#extended_pattern_language
shopt -s extglob

#set -x

BASEDIR=$(dirname $(readlink -nf "$0"))
VERSION=$(grep ^__version__ "${BASEDIR}/terrariumPI.py" | cut -d' ' -f 3)
VERSION="${VERSION//\"/}"
OS=$(grep -ioP '^VERSION_CODENAME=(\K.*)' /etc/os-release)
PYTHON=$(python3 -V)
PI_HARDWARE=$(grep -ioP '^Model\s*: (\K.*)' /proc/cpuinfo)
PI_ZERO=0
if [[ $PI_HARDWARE == *"Pi Zero"* ]]; then
  PI_ZERO=1
fi

INSTALLER_TITLE="TerrariumPI ${VERSION}, ${PYTHON}, OS ${OS}, ${PI_HARDWARE}"

WHOAMI=$(whoami)
if [ "${WHOAMI}" != "root" ]; then
  echo "Start TerrariumPI installation with sudo command"
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

PIP_MODULES=""
while IFS= read -r line; do
  [[ $line =~ ^#.* ]] && continue
  PIP_MODULES="${PIP_MODULES} ${line}"
done < requirements.txt

if [ "${OS}" == "buster" ]; then
  # Python 3.7 (EOL)
  PIP_MODULES="${PIP_MODULES//pip==+([^ ])/pip==24.0}"
  PIP_MODULES="${PIP_MODULES//setuptools==+([^ ])/setuptools==68.0.0}"
  PIP_MODULES="${PIP_MODULES//wheel==+([^ ])/wheel==0.42.0}"

  PIP_MODULES="${PIP_MODULES//yoyo-migrations==+([^ ])/yoyo-migrations===8.2.0}"
  PIP_MODULES="${PIP_MODULES//python-dotenv==+([^ ])/python-dotenv==0.21.1}"

  PIP_MODULES="${PIP_MODULES//gevent==+([^ ])/gevent==22.10.2}"
  PIP_MODULES="${PIP_MODULES//bcrypt==+([^ ])/bcrypt==4.1.3}"

  PIP_MODULES="${PIP_MODULES//Pillow==+([^ ])/Pillow==9.5.0}"
  PIP_MODULES="${PIP_MODULES//numpy==+([^ ])/numpy==1.21.4}"
  PIP_MODULES="${PIP_MODULES//opencv-python-headless==+([^ ])/opencv-python-headless==4.6.0.66}"

  PIP_MODULES="${PIP_MODULES//gpiozero==+([^ ])/gpiozero==1.6.2}"
  PIP_MODULES="${PIP_MODULES//requests==+([^ ])/requests==2.31.0}"

  PIP_MODULES="${PIP_MODULES//python-kasa==+([^ ])/python-kasa==0.5.1}"
  PIP_MODULES="${PIP_MODULES//meross-iot==+([^ ])/meross-iot==0.4.7.5}"
  PIP_MODULES="${PIP_MODULES//pywemo==+([^ ])/pywemo==0.9.2}"

  PIP_MODULES="${PIP_MODULES//Adafruit-Blinka==+([^ ])/Adafruit-Blinka==8.43.0}"

  PIP_MODULES="${PIP_MODULES//icalevents==+([^ ])/icalevents==0.1.25}"
  PIP_MODULES="${PIP_MODULES//psutil==+([^ ])/psutil==6.0.0}"
  PIP_MODULES="${PIP_MODULES//packaging==+([^ ])/packaging==24.0}"

  PIP_MODULES="${PIP_MODULES//pyfiglet==+([^ ])/pyfiglet==0.8.post1}"

  PIP_MODULES="${PIP_MODULES//luma.oled==+([^ ])/luma.oled==3.13.0}"

  PIP_MODULES="${PIP_MODULES//python-telegram-bot\[socks,http2\]==+([^ ])/python-telegram-bot\[socks,http2\]==20.3}"

  PIP_MODULES="${PIP_MODULES//icalendar==+([^ ])/icalendar==5.0.13}"
  PIP_MODULES="${PIP_MODULES//adafruit-circuitpython-typing==+([^ ])/adafruit-circuitpython-typing==1.10.1}"
  PIP_MODULES="${PIP_MODULES//pydantic==+([^ ])/pydantic==1.10.9}"

  OPENCV_PACKAGES="libopenexr23 libilmbase23 liblapack3 libatlas3-base"

elif [ "${OS}" == "bullseye" ]; then
  # Python 3.9
  OPENCV_PACKAGES="libopenexr25 libilmbase25 liblapack3 libatlas3-base"

elif [ "${OS}" == "bookworm" ]; then
  # Python 3.11
  # We use the python3-opencv from the OS, as piwheels does not provide a compiled package (rpicam-apps-lite does not work on RPI 5)
  OPENCV_PACKAGES="libopenexr-3-1-30 liblapack3 libatlas3-base python3-opencv libglib2.0-dev libbluetooth-dev rpicam-apps"

  # Python package version difference per OS
  # On bookworm we use the OS package versions
  PIP_MODULES="${PIP_MODULES//opencv-python-headless==+([^ ])/}"
  # Need a upgraded bluepy library
  PIP_MODULES="${PIP_MODULES//git+https:\/\/github.com\/IanHarvey\/bluepy/git+https:\/\/github.com\/Mausy5043\/bluepy3}"

fi

# if [ "${PI_ZERO}" -eq 1 ]; then
#   # Pi Zero needs some fixed python modules
#   PIP_MODULES="${PIP_MODULES//gevent==+([^ ])/gevent==21.8.0}"
#   PIP_MODULES="${PIP_MODULES//bcrypt==+([^ ])/bcrypt==3.2.2}"
#   PIP_MODULES="${PIP_MODULES//numpy==+([^ ])/numpy==1.21.4}"
#   PIP_MODULES="${PIP_MODULES} lxml==4.6.4"

#   if [ "${OS}" == "buster" ]; then
#     PIP_MODULES="${PIP_MODULES//opencv-python-headless==+([^ ])/opencv-python-headless==4.5.4.60}"
#     PIP_MODULES="${PIP_MODULES//cryptography==+([^ ])/cryptography==37.0.4}"
#   elif [ "${OS}" == "bullseye" ]; then
#     PIP_MODULES="${PIP_MODULES//opencv-python-headless==+([^ ])/opencv-python-headless==4.5.3.56}"
#   fi
# fi

APT_PACKAGES="bc screen git watchdog i2c-tools pigpio sqlite3 ffmpeg libasound2-dev sispmctl ntp libssl1.1 libxslt1.1 libxslt1-dev libxml2-dev libglib2.0-dev libopenblas-dev ${OPENCV_PACKAGES} ${PYTHON_LIBS}"

# Install dialog for further installation
if ! hash whiptail 2>/dev/null; then
  aptitude -y install whiptail
fi

clear

# OS version check
# if [ "${OS}" == "bookworm" ]; then
#   whiptail --backtitle "${INSTALLER_TITLE}" --title " TerrariumPI Installer " --yesno "TerrariumPI is not Raspbian Bookworm OS compatible. Use at own risk.\n\nDo you want to continue?" 0 60

#   case $? in
#     1|255) whiptail --backtitle "${INSTALLER_TITLE}"  --title " TerrariumPI Installer " --msgbox "TerrariumPI installation is aborted" 0 60
#       echo "TerrariumPI ${VERSION} is supported on Buster/Bullseye OS (Legacy OS)"
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

# Set the timezone
dpkg-reconfigure tzdata

# Clean up first
whiptail --backtitle "${INSTALLER_TITLE}" --title " TerrariumPI Installer " --yesno "TerrariumPI is going to remove not needed programs in order to free up disk space and make future updates faster. All desktop software will be removed.\n\nDo you want to remove not needed programs?" 0 0

CLEANUP=0
case $? in
  0)
    CLEANUP=1
  ;;
esac

whiptail --backtitle "${INSTALLER_TITLE}"  --title " TerrariumPI Installer " --msgbox "TerrariumPI will now start the installation... Have a coffee" 0 60

if [ "${CLEANUP}" -eq 1 ]; then
  debconf-apt-progress -- apt-get -y remove *${CLEANUP_PACKAGES// /* *}*
fi

# Install required packages to get the terrarium software running
debconf-apt-progress -- apt-get -y autoremove
debconf-apt-progress -- apt-get -y update
debconf-apt-progress -- apt-get -y full-upgrade
debconf-apt-progress -- apt-get -y install ${APT_PACKAGES}

# Basic config:
# Enable 1Wire en I2C during boot
if [ -f /etc/modules ]; then
  if [ $(grep -ic "i2c-dev" /etc/modules) -eq 0 ]; then
    echo "i2c-dev" >> /etc/modules
  fi
fi

BOOTCONFIG="/boot/config.txt"
if [ "${OS}" == "bookworm" ]; then
  BOOTCONFIG="/boot/firmware/config.txt"
fi

if [ -f "${BOOTCONFIG}" ]; then

  # Enable I2C
  if [ $(grep -ic "^dtparam=i2c_arm=on" "${BOOTCONFIG}") -eq 0 ]; then
    echo "dtparam=i2c_arm=on" >> "${BOOTCONFIG}"
  fi

  # Enable 1-Wire
  if [ $(grep -ic "^dtoverlay=w1-gpio" "${BOOTCONFIG}") -eq 0 ]; then
    echo "dtoverlay=w1-gpio" >> "${BOOTCONFIG}"
  fi

  # Enable serial
  if [ $(grep -ic "^enable_uart=1" "${BOOTCONFIG}") -eq 0 ]; then
    echo "enable_uart=1" >> "${BOOTCONFIG}"
  fi

  if [ "${OS}" != "bookworm" ]; then

    # Enable camera
    if [ $(grep -ic "^gpu_mem=" "${BOOTCONFIG}") -eq 0 ]; then
        echo "gpu_mem=128" >> "${BOOTCONFIG}"
    fi

    if [ $(grep -ic "^start_x=1" "${BOOTCONFIG}") -eq 0 ]; then
        echo "start_x=1" >> "${BOOTCONFIG}"
    fi

    # Bullseye legacy camera
    sed -i "${BOOTCONFIG}" -e "s@^[ ]*dtoverlay=vc4-kms-v3d@#dtoverlay=vc4-kms-v3d@"
    sed -i "${BOOTCONFIG}" -e "s@^[ ]*camera_auto_detect=.*@@"

    if [ $(grep -ic "^dtoverlay=vc4-fkms-v3d" "${BOOTCONFIG}") -eq 0 ]; then
      sed -i "${BOOTCONFIG}" -e "s@^\[pi4\]@\[pi4\]\ndtoverlay=vc4-fkms-v3d@"
    fi
  fi

fi

# Disable serial debug to enable CO2 sensors
CMDLINE="/boot/cmdline.txt"
if [ "${OS}" == "bookworm" ]; then
  CMDLINE="/boot/firmware/cmdline.txt"
fi

if [ -f "${CMDLINE}" ]; then
  sed -i "${CMDLINE}" -e "s@console=ttyAMA0,[0-9]\+ @@"
  sed -i "${CMDLINE}" -e "s@console=serial0,[0-9]\+ @@"
fi

# Create needed groups
groupadd -f dialout 2> /dev/null
groupadd -f sispmctl 2> /dev/null
groupadd -f gpio 2> /dev/null
# Add user to all groupds
usermod -a -G dialout,sispmctl,gpio,bluetooth "${SCRIPT_USER}" 2> /dev/null

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
git submodule update 2> /dev/null && rm -rf 3rdparty/4relay-rpi && rm -rf 3rdparty/4relind-rpi && rm -rf 3rdparty/8relind-rpi && rm -rf 3rdparty/Bright-Pi
patch -N -s -r /dev/null 3rdparty/python3-voltcraft-sem6000/sem6000/repeat_on_failure_decorator.py < contrib/python3-voltcraft-sem6000.patch.diff >/dev/null

PROGRESS=$((PROGRESS + 1))
cat <<EOF
XXX
$PROGRESS
Install required software\n\nSetting up Python environment ...
XXX
EOF

# Create Python environment
cd "${BASEDIR}/"
if [ -f venv/pyvenv.cfg ]; then
    sed -i "venv/pyvenv.cfg" -e "s@^include-system-site-packages.*@include-system-site-packages = false@"
fi
python3 -m venv venv
source venv/bin/activate

# Install python modules inside the virtual env of Python
NUMBER_OF_MODULES=($PIP_MODULES)
NUMBER_OF_MODULES=${#NUMBER_OF_MODULES[@]}
MODULE_COUNTER=1
MODULE_OFFSET=${PROGRESS}
MODULE_MAX=92
for PIP_MODULE in ${PIP_MODULES}
do
  PROGRESS=$(printf "%'.*f\n" 0 $(echo "scale=2; ( ${MODULE_COUNTER} * ((${MODULE_MAX} - ${MODULE_OFFSET}) / ${NUMBER_OF_MODULES}) ) + ${MODULE_OFFSET}" | bc -l))
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

Installing python module ${MODULE_COUNTER} out of ${NUMBER_OF_MODULES}: ${MODULE_NAME} (attempt ${ATTEMPT}) ...
XXX
EOF
    pip install --upgrade "${PIP_MODULE}" --extra-index-url https://www.piwheels.org/simple 2> /dev/null

    if [ $? -eq 0 ]; then
      # PIP install succeeded normally

      if [ "${MODULE_NAME}" == "bluepy3" ]; then
        # Need to compile a binary: https://github.com/Mausy5043/bluepy3?tab=readme-ov-file#installation
        python -c "import bluepy3.btle"
      fi

      ATTEMPT=$((ATTEMPT + 99))
    else
      # PIP install failure... retry..
      ATTEMPT=$((ATTEMPT + 1))
    fi

  done

  MODULE_COUNTER=$((MODULE_COUNTER + 1))

done

if [ "${OS}" == "bookworm" ]; then
  sed -i "venv/pyvenv.cfg" -e "s@^include-system-site-packages.*@include-system-site-packages = true@"
fi

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
chown "${SCRIPT_USER}": .
chown "${SCRIPT_USER}": * -Rf

sync


PROGRESS=$((PROGRESS + 1))
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
systemctl enable terrariumpi 2> /dev/null


PROGRESS=$((PROGRESS + 1))
cat <<EOF
XXX
$PROGRESS
Finishing installation

Enable bluetooth for ${SCRIPT_USER} user ...
XXX
EOF

# To run this as non-root run the following,
# https://github.com/marcelrv/miflora,
# https://github.com/IanHarvey/bluepy/issues/218,
# https://github.com/Mausy5043/bluepy3?tab=readme-ov-file#installation
find . -name "bluepy*-helper" -exec setcap 'cap_net_raw,cap_net_admin+eip' {} \;

PROGRESS=$((PROGRESS + 1))
cat <<EOF
XXX
$PROGRESS
Finishing installation

Enable Message Of The Day ...
XXX
EOF

# Enable MOTD
ln -s "${BASEDIR}/motd.sh" /etc/update-motd.d/05-terrariumpi 2>/dev/null

PROGRESS=$((PROGRESS + 1))
cat <<EOF
XXX
$PROGRESS
Finishing installation

Setup logging ...
XXX
EOF

# Setup logging symlinks
if [ ! -h log/terrariumpi.log ]; then
  su -c 'ln -s /dev/shm/terrariumpi.log log/terrariumpi.log' -s /bin/bash "${SCRIPT_USER}" 2>/dev/null
fi
if [ ! -h log/terrariumpi.access.log ]; then
  su -c 'ln -s /dev/shm/terrariumpi.access.log log/terrariumpi.access.log' -s /bin/bash "${SCRIPT_USER}" 2>/dev/null
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
  echo "TerrariumPI installation is rebooting the Raspberry PI now!"
  reboot
  ;;
esac
