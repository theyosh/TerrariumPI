# TerrariumPI 2.8.1
Software for cheap home automation of your reptile terrarium or any other enclosed environment. With this software you are able to control an enclosed environment so that the temperature and humidity is of a constant value. This is done by using temperature and humidity sensors and realy switches to activate external devices.

It has support for lights, sprayer, heater and cooler equipment. The amount of devices that can be controlled depends on the used relay boards.

Think off:
- Terrarium
- Aquarium
- Growhouse

And all this is controlled with a nice webinterface based on [Gentelella a Bootstrap 3 template](https://github.com/puikinsh/gentelella/).
## Features
- Controlling electronic devices like lights, sprayers, heating and cooling equipment
- Reading out temperature and humidity sensors
- Open door detection (sprayer will not spray when a door is open)
- Support for native Raspberry Pi cam out of the box
- Support for USB and remote webcams
- Total power and water usage for costs calculation
- Lights control based on sun rise and sun set or timers
- Rain control based on measured humidity
- Heater control based on temperature sensors or timers
- Cooling control based on temperature sensors or timers
- Weather forecast from external source
- Temperatures in Celsius or Fahrenheit
- Alarm detections

It is currently controling my reptile terrarium for more then three years! And my Madagascar Day Gecko is very happy with it!

## Translations
The software has support for the following languages:
- English
- Dutch
- German
- Italian

Your language not in the list? [Create your own language translation](https://github.com/theyosh/TerrariumPI/wiki/Translations)

## Installation
The installation expects a Pi with working network and ssh. It is tested with [Raspbian Stretch Lite](https://www.raspberrypi.org/downloads/raspbian/). For now the Full version is not working somehow.... So use the lite image!
1. Get a working Raspberry Pi and login as user 'pi'  
  `ssh pi@[raspberry_ip]`
2. Clone this repository and submodules!  
  `git clone --recursive https://github.com/theyosh/TerrariumPI.git`
3. Enter the new TerrariumPI folder  
  `cd TerrariumPI`
4. Run the installer script and wait  
  `sudo ./install.sh`
5. Reboot Raspberry PI to get all the needed modules loaded  
  `sudo reboot`
6. Go to the webinterface at http://[raspberry_ip]:8090

If you want to use the Raspberry PI 1 wire interface, you have to manually enable it through the raspi-config and reboot once more.

Make sure that your Pi is secured when you put it to the Internet. Would be a shame if TerrariumPI gets next fictum of '[A smart fish tank left a casino vulnerable to hackers](http://money.cnn.com/2017/07/19/technology/fish-tank-hack-darktrace/index.html)' :P

## Updating
This updating is based on that the software is installed with the steps in the Installation above.
1. Get a working Raspberry Pi and login as user 'pi'  
  `ssh pi@[raspberry_ip]`
2. Enter the TerrariumPI folder  
  `cd TerrariumPI`
3. Update the new code with git  
  `git pull`
4. Restart TerrariumPI according to: https://github.com/theyosh/TerrariumPI/wiki/FAQ#how-to-restart-terrariumpi

Now clear your browser cache and reload the webinterface. A brand new version should be running.

## Hardware
This software requires some extra hardware in order to run and work. The bare minimun is
- Power relay board
  - USB versions (Serial and Bitbang)
  - GPIO versions
- Temperature/humdity sensors DHT11, DHT22, AM2303, DS1820, HIH4000, etc through
  - OWFS
  - GPIO
  - 1 Wire interface

If there is some other hardware which is not working with TerrariumPI, open an issue on [Github](https://github.com/theyosh/TerrariumPI/issues) and we will try to support it.

## Screenshots
(made on a very big screen :P )
### Dashboard
![TerrariumPI 2.5 Dashboard screenshot](screenshots/Dashboard.png)
### Sensors
![TerrariumPI 2.5 Sensors settings screenshot](screenshots/Temperature_sensors_list.png)
### Adding sensors
![TerrariumPI 2.5 Sensors settings screenshot adding a new sensor](screenshots/Sensor_settings_add_sensor.png)
### Power switches
![TerrariumPI 2.5 Power switches settings screenshot](screenshots/Switch_settings.png)
### Environment setup
![TerrariumPI 2.5 Environment setup screenshot](screenshots/Environment_setup.png)
### System settings
![TerrariumPI 2.5 System setup screenshot](screenshots/System_setup.png)

More screenshots can be found [here](https://github.com/theyosh/TerrariumPI/tree/master/screenshots)

## About
A live version is running at: https://terrarium.theyosh.nl/index.html. Go to 'Help' menu for more information about used hardware, software and how to setup.
