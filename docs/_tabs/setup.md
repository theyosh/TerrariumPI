---
title: Setup
icon: fas fa-cogs
order: 5

image:
  src: /assets/img/Setup.webp
  alt: Setup header image
---

## Login
![New relay form](/assets/img/Login.webp){: style="max-height: 100px" .right}
After the installation, you need to setup TerrariumPI. In order to do that, login with a browser at http://[raspberry_pi]:8090 and click on the `Login` link on the left side menu. The default login should be **admin** / **password** ([FAQ]({{ 'faq/login/' | relative_url}}))

## Help
On every form popup you have a small question mark <i class="far fa-question-circle" aria-hidden="true"></i> next to the form title. Click on it to get more information about the form fields.


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
:  Enter a new password for authentication. [Encrypted]({{ 'features/' | relative_url}}#admin-password)

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
: The username to login to your Meross cloud account. [Encrypted]({{ 'features/' | relative_url}}#other-sensitive-data)

Meross password
: The password to login to your Meross cloud account. [Encrypted]({{ 'features/' | relative_url}}#other-sensitive-data)

## Weather
![Weather source form](/assets/img/Weather_Settings.webp)
_Popup form adding/updating the weather source_

With the weather data you can schedule your light system based on the **sun rise** and **sun set**. This can either be at your home location, or any other location. The sun rise and set times will be shifted to your home location times. So when it is day at 08:00 at the given location, TerrariumPI will thread that as 08:00 local time. This way, you can have seasons with shorter and longer days, based on day of the year.

Other weather data is just for show. Does not have a function.

### Setup
In order to use the weather system, you need to create a free account at [OpenWeatherMap](https://home.openweathermap.org/users/sign_up).

The url format needs to be `https://api.openweathermap.org/data/2.5/weather?q=[City],[Country]&appid=[API_KEY]`. Do not add the `&metric=` part in the url.
## Sensors
![Sensor settings form](/assets/img/Sensor_Settings.webp)
_Popup form adding/updating the sensors_

### Calibration

## Relays
![Relay form](/assets/img/Add_Relay_Form.webp)
_Popup form for adding and updating relays - Calibration is only available for dimmers_

### Calibration

## Doors / buttons
![Button form](/assets/img/Button_Settings.webp)
_Popup form for adding and updating buttons - Calibration is only available for light sensors_

### Calibration

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