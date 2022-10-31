#!/bin/bash

# default to true if not passed
ENABLE_I2C=${ENABLE_I2C:-'true'}
ENABLE_1_WIRE=${ENABLE_1_WIRE:-'true'}
ENABLE_CAMERA=${ENABLE_1_WIRE:-'true'}
ENABLE_SERIAL=${ENABLE_1_WIRE:-'true'}
ENABLE_CO2_SENSORS=${ENABLE_1_WIRE:-'true'}
AUTO_REBOOT=${AUTO_REBOOT:-'true'}

REBOOT_REQUIRED=0

if [ -f /boot/config.txt ]; then

  # Enable I2C
  if [[ $ENABLE_I2C == "true" ]] && [ $(grep -ic "^dtparam=i2c_arm=on" /boot/config.txt) -eq 0 ]; then
    echo "dtparam=i2c_arm=on" >> /boot/config.txt
    echo "Enabled I2C in boot config"
    REBOOT_REQUIRED=1
  fi

  if [[ $ENABLE_I2C == "true" ]] && [ -f /etc/modules ]; then
    if [ $(grep -ic "i2c-dev" /etc/modules) -eq 0 ]; then
      echo "i2c-dev" >> /etc/modules
      echo "Enable I2C modules"
      REBOOT_REQUIRED=1
    fi
  fi

  # Enable 1-Wire
  if [[ $ENABLE_1_WIRE == "true" ]] && [ $(grep -ic "^dtoverlay=w1-gpio" /boot/config.txt) -eq 0 ]; then
    echo "dtoverlay=w1-gpio" >> /boot/config.txt
    echo "Enabled 1 Wire in boot config"
    REBOOT_REQUIRED=1
  fi

  # Enable camera
  if [[ $ENABLE_CAMERA == "true" ]] && [ $(grep -ic "^gpu_mem=" /boot/config.txt) -eq 0 ]; then
    echo "gpu_mem=128" >> /boot/config.txt
    echo "Enabled Camera in boot config (1)"
    REBOOT_REQUIRED=1
  fi

  if [[ $ENABLE_CAMERA == "true" ]] && [ $(grep -ic "^start_x=1" /boot/config.txt) -eq 0 ]; then
    echo "start_x=1" >> /boot/config.txt
    echo "Enabled Camera in boot config (2)"
    REBOOT_REQUIRED=1
  fi

  # Bullseye legacy camera support
  if [[ $ENABLE_CAMERA == "true" ]] && [ ! $(grep -ic "^dtoverlay=vc4-kms-v3d" /boot/config.txt) -eq 0 ]; then
    # can't inline sed due to docker mount
    cp /boot/config.txt /config.tmp
    sed -i "/config.tmp" -e "s@^[ ]*dtoverlay=vc4-kms-v3d@#dtoverlay=vc4-kms-v3d@g"
    cat /config.tmp > /boot/config.txt
    rm /config.tmp
    echo "Enabled Bullseye legacy Camera mode in boot config (1)"
    REBOOT_REQUIRED=1
  fi

  if [[ $ENABLE_CAMERA == "true" ]] && [ ! $(grep -ic "^camera_auto_detect=.*" /boot/config.txt) -eq 0 ]; then
    # can't inline sed due to docker mount
    cp /boot/config.txt /config.tmp
    sed -i "/config.tmp" -e "s@^[ ]*camera_auto_detect=.*@@g"
    cat /config.tmp > /boot/config.txt
    rm /config.tmp
    echo "Enabled Bullseye legacy Camera mode in boot config (2)"
    REBOOT_REQUIRED=1
  fi

  if [[ $ENABLE_CAMERA == "true" ]] && [ $(grep -ic "^dtoverlay=vc4-fkms-v3d" /boot/config.txt) -eq 0 ]; then
    # can't inline sed due to docker mount
    cp /boot/config.txt /config.tmp
    sed -i "/config.tmp" -e "s@^\[pi4\]@\[pi4\]\ndtoverlay=vc4-fkms-v3d@"
    cat /config.tmp > /boot/config.txt
    rm /config.tmp
    echo "Enabled Bullseye legacy Camera mode in boot config (3)"
    REBOOT_REQUIRED=1
  fi

  # Enable serial
  if [[ $ENABLE_SERIAL == "true" ]] && [ $(grep -ic "^enable_uart=1" /boot/config.txt) -eq 0 ]; then
    echo "enable_uart=1" >> /boot/config.txt
    echo "Enabled Serial in boot config"
    REBOOT_REQUIRED=1
  fi

fi

# Disable serial debug to enable CO2 sensors
if [ -f /boot/cmdline.txt ]; then

  if [[ $ENABLE_CO2_SENSORS == "true" ]] && [ $(grep -ic "console=ttyAMA0,[0-9]\+ " /boot/cmdline.txt) -eq 1 ]; then
    # can't inline sed due to docker mount
    cp /boot/cmdline.txt /boot-cmdline.tmp
    sed -i "/boot-cmdline.tmp" -e "s@console=ttyAMA0,[0-9]\+ @@"
    cat /boot-cmdline.tmp > /boot/cmdline.txt
    rm /boot-cmdline.tmp
    echo "Enabled CO2 sensors in boot config (1)"
    REBOOT_REQUIRED=1
  fi

  if [[ $ENABLE_CO2_SENSORS == "true" ]] && [ $(grep -ic "console=serial0,[0-9]\+ " /boot/cmdline.txt) -eq 1 ]; then
    # can't inline sed due to docker mount
    cp /boot/cmdline.txt /boot-cmdline.tmp
    sed -i "/boot-cmdline.tmp" -e "s@console=serial0,[0-9]\+ @@"
    cat /boot-cmdline.tmp > /boot/cmdline.txt
    rm /boot-cmdline.tmp
    echo "Enabled CO2 sensors in boot config (2)"
    REBOOT_REQUIRED=1
  fi

fi

# Setup logging symlinks
if [ ! -h log/terrariumpi.log ]; then
  ln -s /dev/shm/terrariumpi.log log/terrariumpi.log
fi
if [ ! -h log/terrariumpi.access.log ]; then
  ln -s /dev/shm/terrariumpi.access.log log/terrariumpi.access.log
fi

# Add some pi camera symbolic links
ln -s /opt/vc/bin/raspi* /usr/bin/ 2>/dev/null

if [[ $REBOOT_REQUIRED == 1 ]]; then
  if [[ $AUTO_REBOOT == true ]]; then
    echo "Some settings have been updated that require reboot, your Raspberry Pi will reboot in 60 seconds..."
    sleep 60
    echo b >/proc/sysrq-trigger
  else
    echo "Some settings have been updated that require reboot, please reboot your Raspberry Pi now."
    exit 100
  fi
fi

# Clear after restart
if [ -f /var/run/pigpio.pid ]; then
  rm /var/run/pigpio.pid
fi
# run localhost socket only
pigpiod -l

# Remove the restart file from last unhealty status
if [ -f .restart ]; then
  rm .restart
fi

# Clear after restart
if [ -f motd.sh ]; then
  rm motd.sh
fi

# We need to update the libraries with the mounted /opt/vc/lib/ :(
ldconfig

# No reboot required, Pi must already be fully configured, start TP
exec /opt/venv/bin/python /TerrariumPI/terrariumPI.py
