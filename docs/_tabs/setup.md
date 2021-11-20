---
title: Setup
icon: fas fa-cogs
order: 5

image:
  path: /assets/img/Setup.webp
  src: /assets/img/Setup.webp
  alt: Setup header image
---

## Login
![New relay form](/assets/img/Login.webp){: style="max-height: 100px" .right}
After the installation, you need to setup TerrariumPI. In order to do that, login with a browser at http://[raspberry_pi]:8090 and click on the `Login` link on the left side menu. The default login should be **admin** / **password** ([FAQ]({% link _faq/login.md %}))

## Help
On every form popup you have a small question mark <i class="far fa-question-circle" aria-hidden="true"></i> next to the form title. Click on it to get more information about the form fields.

## Required fields
All fields with a red start (<span style="color:red;font-weight:bold">*</span>) are required to fill out. Some fields can be come required based on selected options.

## Settings
![Settings form](/assets/img/Settings.webp)
_Settings form with four parts_

The settings is split up in multiple parts. Each group contains settings that are related to each other.

### System
In the system group you setup the minimal settings to get TerrariumPI running.

Pi power usage
: Enter the amount of total power in watts used by the Raspberry PI including attached USB devices.

IP number
: Enter the IP to listen for connections. Default 0.0.0.0

Port number
: Enter the port number to listen for connections. Default 8090

Authentication mode
: There are 3 authentication options.
- Full authentication: For all actions you need to be logged in.
- Only for changes: Only adding and updating needs authentication.
- No authentication: No authentication at all. **Be very carefull with this!**

User name
:  Enter the user name for authentication. Default admin

New password
:  Enter a new password for authentication. [Encrypted]({% link _tabs/features.md %}#admin-password)

Confirm new password
: Confirm the new password for authentication.

Excluded ids
: List of IDs that are excluded. If you mis a sensor or relay, remove it from this list, and it will be used again.


### Locale
In the locale group you can setup your locales that are custom to.

Language
:  Select the interface language. This will also change number and currency formatting.

Temperature type
:  Select the temperature indicator. Only affects the current values.

Distance type
:  Select the distance indicator. Only affects the current values.

Liquid volume type
:  Select the water volume indicator. Only affects the current values.

Wind speed type
:  Select the wind speed indicator. Only affects the current values.

Power price
:  Enter the price per kWh.

Water price
:  Enter the price per L/Gallon.


### Gui
In the Gui group you can tune the web interface.

Title
: Enter a custom title. If it contains the letters PI, it will turn red on the MOTD

Profile image
: Upload a small image. That is used in the left menu.

Graph smoothing
: If the graph is spikey, you can enter a value which is the amount of measurements that are averaged.

Auto dark mode
: Tun dark mode on based on weather sun rise and set

Show min and max values in gauge graphs
: Add the minimum and maximum value that is measured in the last 24 hours on the gauge graph.

Hide enclosures on dashboard
: Only show the average graphs on the dashboard.

All gauges on a single page
: Add an extra menu option to show all the sensors on a single page.

### Cloud
In the cloud group you can enter credentials for different cloud integrations

#### Meross
With the Meross cloud you can use all the relays and sensors that are connected to your account.

Meross username
: The username to login to your Meross cloud account. [Encrypted]({% link _tabs/features.md %}#other-sensitive-data)

Meross password
: The password to login to your Meross cloud account. [Encrypted]({% link _tabs/features.md %}#other-sensitive-data)

## Weather
![Weather source form](/assets/img/Weather_Settings.webp)
_Popup form adding/updating the weather source_

With the weather data you can schedule your light system based on the **sun rise** and **sun set**. This can either be at your home location, or any other location. The sun rise and set times will be shifted to your home location times. So when it is day at 08:00 at the given location, TerrariumPI will thread that as 08:00 local time. This way, you can have seasons with shorter and longer days, based on day of the year.

Other weather data is just for show. Does not have a function.

### Setup
In order to use the weather system, you need to create a free account at [OpenWeatherMap](https://home.openweathermap.org/users/sign_up).

The url format needs to be `https://api.openweathermap.org/data/2.5/weather?q=[City],[Country]&appid=[API_KEY]`. Do not add the `&metric=` part in the url.

## Relays
![Relay form](/assets/img/Add_Relay_Form.webp)
_Popup form for adding and updating relays - Calibration is only available for dimmers_
Adding and changing relays is done with the above relay form.

Hardware
: The hardware type of the relay. [A full list of supported relays]({% link _tabs/hardware.md %}#relays)

Address
: Enter the address of the relay. This is specific for each [relay]({% link _tabs/hardware.md %}#relays).

Name
: The name of the relay. Use an easy to remember name.

Wattage
: The ammount of power that is used when on or at full power (dimmer)

Water flow
: The ammount of water that is used when on or at full power (dimmer) in Liter/Gallon per minute

Current
: The current state of the relay. Value 0 is off, 100 is full on, or a value between 0 - 100 (dimmer)

### Calibration
This is only available for dimmers.

Dimmer frequency in Hz
: The frequency of wicht the dimmer is working on. The default depends on the selected dimmer type.

Max power in %
: The max power the dimmer is allowed to use. Default 100

Dimmer offset in %
: An offset value that is reduced from the actual value. Default 0
## Sensors
![Sensor settings form](/assets/img/Sensor_Settings.webp)
_Popup form adding/updating the sensors_
Adding and changing sensors is done with the above sensor form.

Hardware
: The hardware type of the sensor. [A full list of supported sensors]({% link _tabs/hardware.md %}#sensors)

Type
: Select what kind of sensor it is.

Address
: Enter the address of the sensor. This is specific for each [sensor]({% link _tabs/hardware.md %}#sensors).

Name
: The name of the sensor. Use an easy to remember name.

Alarm min
: The lower alarm value. When the sensor gets below this value, the **low** alarm will be triggered

Alarm max
: The high alarm value. When the sensor gets higher then this value, the **hight** alarm will be triggered

Limit min
: The minimun value that is valid for this sensor. Values measured below this value will be ignored.

Limit max
: The maximum value that is valid for this sensor. Values measured higher then this value will be ignored.

Max diff
: The maximum difference between two measurements that is valid. Enter **0** to disable.

Exclude average
: Exclude this sensor from the average calculation and graphs on the dashboard.

### Calibration
Offset
: Enter a value to correct the output reading. This can be a positive or negative value.


## Doors / buttons
![Button form](/assets/img/Button_Settings.webp)
_Popup form for adding and updating buttons - Calibration is only available for light sensors_
Adding and changing buttons is done with the above button form.

Hardware
: The hardware type of the button. [A full list of supported buttons]({% link _tabs/hardware.md %}#buttons)

Address
: Enter the address of the button. This is specific for each [button]({% link _tabs/hardware.md %}#buttons).

Name
: The name of the button. Use an easy to remember name.

Current
: The current state of the button. Value 1 is active, value 0 is not active

### Calibration
This is only available for light sensors.

Capacitor value in µF
: Enter the value of the capacitor



## Webcams
![Webcam form](/assets/img/Webcam_Settings.webp)
_Popup form for adding and updating webcams_

## Audio
![Playlist form](/assets/img/Playlist_Settings.webp)
_Popup form for adding and updating playlists_

## Enclosures
![Enclosure form](/assets/img/Enclosure_Settings.webp)
_Popup form for adding and updating enclosures_

## Areas
![Area form](/assets/img/Area_Settings.webp)
_Popup form for adding and updating areas_