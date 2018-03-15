# TerrariumPI 3.4.1
Software for cheap home automation of your reptile terrarium or any other enclosed environment. With this software you are able to control for example a terrarium so that the temperature and humidity is of a constant value. Controlling the temperature can be done with heat lights, external heating or cooling system. As long as there is one temperature sensor available the software is able to keep a constant temperature.

For humidity control there is support for a spraying system. The sprayer can be configured to spray for an X amount of seconds and there is a minumal period between two spray actions. Use at least one humitidy sensors to get a constant humidity value.

The software is that flexible that there is no limit in amount of sensors, relay boards or door sensors. The usage can be endless. All power switches have support for timers to trigger based on a time pattern.

Think off:
- Terrarium (wet of dry)
- Aquarium
- Tanks with animals or plants
- Growhouse

And all this is controlled with a nice webinterface based on [Gentelella a Bootstrap 3 template](https://github.com/puikinsh/gentelella/).

## Table of Contents
1. [Features](#features)
2. [Translations](#translations)
3. [Installation](#installation)
4. [Updating](#updating)
5. [Hardware](#hardware)
   1. [GPIO numbering](#gpio-numbering)
   2. [New hardware](#new-hardware)
6. [Remote data](#remote-data)
7. [Screenshots](#screenshots)
8. [About](#about)

## Features
- Controlling electronic devices like lights, sprayers, heating, cooling and water pump equipment
- Support for dimming electronic devices
  - Manual dimming through web interface
  - Predefined on and off dimming durations
  - Predefined on and off dimming percentages
  - Predefined dimming steps for environment system (heater and cooler)
- Support for timmers in powerswitches and environment #72
  - Predefined start and stop times based on timer or weather
  - Predefined on and off durations in minutes
- Support for Energenie USB and LAN powerswitches [EG-PM(s)2](http://energenie.com/item.aspx?id=7556)
- Support for multiple temperature and humidity sensors
- Support for ultrasonic sound range sensors
- Support for native Raspberry Pi cam out of the box
- Support for USB and remote webcams
- Support for analog devices through a MCP3008
  - Support for PH probe SKU SEN0161
- Open door detection (sprayer will not spray when a door is open)
- Total power and water usage for costs calculation
- Lights control based on sun rise and sun set or timers
- Rain control based on humidity sensors and timers
- Heater control based on temperature sensors or timers
  - Variable day and night difference for min and max temperature
- Cooling control based on temperature sensors or timers
- Watertank level control based on ultrasonic sound range sensors
- Weather forecast from external source for lighting schema
  - Supports https://yr.no
  - Supports https://wunderground.com
  - Supports https://openweathermap.org
- Temperatures in Celsius or Fahrenheit
- Distances in centimetres or inches
- Alarm detections
- Audio support through interal audio jack or USB soundcards #42
  - Create playlists (loop and repeat)
  - Volume controle in the webinterface
  - Uploading audio files through webinterface
  - Audio meta data support (mediainfo)
- Remote temperature and humidity sensors through HTTP(S) JSON API's. JSON Data format can be found on [Remote data wiki](https://github.com/theyosh/TerrariumPI/wiki/Remote-data).

It is currently controling my reptile terrarium for more then three years! And my Madagascar Day Gecko is very happy with it!

## Translations
The software has support for the following languages:
- English
- Dutch
- German
- Italian
- France

Your language not in the list or not up to date? [Create your own language translation](https://github.com/theyosh/TerrariumPI/wiki/Translations)

## Installation
The installation expects a Pi with working network and ssh. It is tested with [Raspbian Stretch Lite](https://www.raspberrypi.org/downloads/raspbian/). For now the Full version is not working somehow.... So use the lite image!
1. Get a working Raspberry Pi and login as user 'pi'  
  `ssh pi@[raspberry_ip]`
2. Install git  
  `sudo apt -y install git`
3. Clone this repository and submodules!  
  `git clone --recursive https://github.com/theyosh/TerrariumPI.git`
4. Enter the new TerrariumPI folder  
  `cd TerrariumPI`
5. Run the installer script and wait  
  `sudo ./install.sh`
6. Reboot Raspberry PI to get all the needed modules loaded  
  `sudo reboot`
7. Go to the webinterface at http://[raspberry_ip]:8090

All needed options and modules are setup by the installer script. This means that I2C and 1Wire overlay are enabled by default.

Make sure that your Pi is secured when you put it to the Internet. Would be a shame if TerrariumPI gets next fictum of '[A smart fish tank left a casino vulnerable to hackers](http://money.cnn.com/2017/07/19/technology/fish-tank-hack-darktrace/index.html)' :P

## Updating
This updating is based on that the software is installed with the steps in the Installation above. When updating between release versions it will take more time due to database updates and cleanups. This can be seen in the logfile.
1. Get a working Raspberry Pi and login as user 'pi'  
  `ssh pi@[raspberry_ip]`
2. Enter the TerrariumPI folder  
  `cd TerrariumPI`
3. Update the new code with git  
  `git pull`
4. Re-run the installation script in order to update software dependencies  
  `sudo ./install.sh`
4. Restart TerrariumPI according to: https://github.com/theyosh/TerrariumPI/wiki/FAQ#how-to-restart-terrariumpi

Now clear your browser cache and reload the webinterface. A brand new version should be running.

## Hardware
This software requires a Raspberry Pi and some extra hardware in order to run and work. The bare minimun and tested hardware is
- Raspberry PI
  - Pi 2
  - Pi 3
  - Zero
- Power relay board
  - USB versions (Serial and Bitbang)
  - GPIO versions
  - PWM Dimmer versions
- Temperature/humdity/ultrasonic/PH sensors DHT11, DHT22, AM2303, DS1820, HIH4000, HC-SR04, SEN0161, etc through
  - OWFS
  - GPIO
  - 1 Wire interface
  - MCP3008 ([RasPiO Analog Zero](https://github.com/raspitv/analogzero))
  
### GPIO numbering
All hardware that connects to the GPIO pins use **Physical GPIO numbering** (1 - 40). The software will translate it to BCM if needed for a supported device or sensor. [More information about GPIO pin numbering](https://pinout.xyz/)

For the analog devices use numbers of the channel on the analog device which is from 0 to 7 (8 channels). Also the software expect the analog MCP3008 on GPIO ports 19,21,23,24 physical (default). [More information about GPIO pin numbering](https://pinout.xyz/)

### New hardware
If there is some other hardware which is not working with TerrariumPI, open an issue on [Github](https://github.com/theyosh/TerrariumPI/issues) and we will try to support it. Raspberry Pi Zero is not tested.

## Remote data
It is possible to use external sensor data that is available through HTTP(S) in JSON format. This way you can combine multiple Raspberry Pi's with TerrariumPI running to one single system. By using multiple Rapsberry PI's you can cover a bigger area. But there are limitations.

Currently it is READONLY. So you can read out remote sensors and switches but you cannot control the remote switches. But this way you can combine the power swiches total costs and power usage.

more information is here: [Remote data wiki](https://github.com/theyosh/TerrariumPI/wiki/Remote-data)

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
