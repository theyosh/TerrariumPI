Changelog
=========


3.1.0 (2017-11-14)
------------

**New**
- Add logfile compressio. [TheYOSH]
- Add audio preview player. [TheYOSH]
- Add audio usage page. [TheYOSH]
- Add better configuration upgrading and logging. [TheYOSH]
- Add disk usage stats and graphs. [TheYOSH]
- Add automatic database upgrades during startup. [TheYOSH]
- Add disk stats part1. [TheYOSH]
- Add soundcard selection which adds the option to use USB soundscards.
  [TheYOSH]
- Added player and dimmer switch warning to power switch settings page
  and playlist page. [TheYOSH]
- Add information text and changed showing help information. [TheYOSH]
- Add player disabled message. [TheYOSH]
- Add PWM Dimmer check and disable audio when a PWM dimmer is used.
  [TheYOSH]
- Add web based audio player. Add playlist options repeat and shuffle.
  [TheYOSH]
- Add support for repeat and shuffle playlists. [TheYOSH]
- Add extra check if switch history data is available. Fix [#41](https://github.com/theyosh/TerrariumPI/issues/41).
  [TheYOSH]
- Add Leaflet.loading as submodule. [TheYOSH]
- Add Leaflet fullscreen as submodule. [TheYOSH]
- Add check for non existing sensor ids. [#38](https://github.com/theyosh/TerrariumPI/issues/38). [TheYOSH]
- Add extra information when rebooting. [TheYOSH]

**Fixes**
- Fix updating weather data when offline. [TheYOSH]
- Fix logging. [TheYOSH]
- Small fixes. [TheYOSH]
- Small fixes. [TheYOSH]
- Fix logging for saving new doors. [TheYOSH]
- Fix logging for saving new switches. [TheYOSH]
- Fix audio playlists reloading. [TheYOSH]
- Fix notification message color. [TheYOSH]
- Fix switch toggleing. [TheYOSH]
- Fix HTML in dutch translation. [TheYOSH]
- Fix dimmer detection. [TheYOSH]
- Fix repeat and shuffle switches when a new playlist is added.
  [TheYOSH]
- Fix open door indicator. [TheYOSH]
- Attempt to fix issue [#44](https://github.com/theyosh/TerrariumPI/issues/44). [TheYOSH]
- Final fix German language. Thanks @vanessa2013. [TheYOSH]
- Fix German translation. [TheYOSH]
- Fix water price calculation. [TheYOSH]
- Fix [#40](https://github.com/theyosh/TerrariumPI/issues/40). Keeping your iguana nicely warm. [TheYOSH]
- Fix [#36](https://github.com/theyosh/TerrariumPI/issues/36). [TheYOSH]

**Updates**
- Update changelog. [TheYOSH]
- Update Dutch translation. [TheYOSH]
- Update logging. [TheYOSH]
- Update logging. [TheYOSH]
- Update disk and memory graphs. [TheYOSH]
- Update language configuration variable. [TheYOSH]
- Update translations. [TheYOSH]
- Update logging. [TheYOSH]
- Update changelog. [TheYOSH]
- Update module fancybox. [TheYOSH]
- Update version number. [TheYOSH]
- Update readme documentation. [TheYOSH]
- Update translations. [TheYOSH]
- Major update. Transform all BCM pin numbering to GPIO in config. Code
  will transform to BCM numbering when needed. Makes it easier to add
  GPIO based hardware. [TheYOSH]
- Update price formatting power and water usage on the dasboard.
  [TheYOSH]
- Update German translation. [TheYOSH]
- Audio update to get Pi silent during startup :( [TheYOSH]
- Better submodules update support. [TheYOSH]
- Update with remote master. [TheYOSH]

**Other**
- Clean up weather code. [TheYOSH]
- Remove debug. [TheYOSH]
- Log volume changes. [TheYOSH]
- Better DHT sensor warnings. [TheYOSH]
- Max timeout DHT senors is 10 seconds. [TheYOSH]
- Code cleanup. [TheYOSH]
- Cleanup Audio player code. [TheYOSH]
- Remove debug. [TheYOSH]
- Merge branch 'master' into feature/audio_modules. [TheYOSH]
- Final tuning audio. [TheYOSH]
- Merge branch 'master' into feature/audio_modules. [TheYOSH]
- Remove debug. [TheYOSH]
- Temp stash. [TheYOSH]
- First attempt to add an audio system with audio files and playlists.
  [#42](https://github.com/theyosh/TerrariumPI/issues/42). [TheYOSH]


3.0.0 (2017-10-29)
------------------

**New**
- Add sqlite3 dependency for manual database manupilation. [TheYOSH]
- Added webcam update timeout. Webcams are now only updated once a
  minute. Should reduce the load and makes the enginge a bit faster.
  [TheYOSH]
- Add extra dimming timing for small changes. [TheYOSH]
- Add PI power user to total power usage. [TheYOSH]
- Added missing translation fields. [TheYOSH]
- Add dimmer settings processing and saving to config file. [TheYOSH]
- Add dimmer support part 1. [TheYOSH]

**Fixes**
- Fix empty graphs. [TheYOSH]
- Fix timer issues [#34](https://github.com/theyosh/TerrariumPI/issues/34). [TheYOSH]
- Fix graphing empty graphs and smaller dimmer knob. [TheYOSH]
- Fixed total duration calculation in total power usage. [TheYOSH]
- Fix switch loading without dimmer settings. [TheYOSH]
- Fix switch toggle to support dimmers. [TheYOSH]
- Fix switch toggle to support dimmers. [TheYOSH]
- Fix devision by zero. [TheYOSH]
- Fix SQL duplicate key error. [TheYOSH]
- Fix timer issues [#34](https://github.com/theyosh/TerrariumPI/issues/34). [TheYOSH]
- Fixed missing translation in home dashboard. [#33](https://github.com/theyosh/TerrariumPI/issues/33). [TheYOSH]

**Updates**
- Update changelog. [TheYOSH]
- Update version number. [TheYOSH]
- Update engine loop to make sure at least one run per minute is
  possible. Should prevent spicky graphs. [TheYOSH]
- Update environment dashboard modus names [#34](https://github.com/theyosh/TerrariumPI/issues/34). [TheYOSH]
- Update translations. [TheYOSH]
- Update readme. [TheYOSH]
- Update readme. [TheYOSH]
- Update power duration calculation. [TheYOSH]
- Updated installation so it works faster and handles upgrades better.
  [TheYOSH]
- Updated data logging and graphing. Reduced load on the client side.
  [TheYOSH]
- Updated dimmer settings in switch settings page. [TheYOSH]
- Updated supported hardware page. [TheYOSH]
- Update environment dashboard modus names [#34](https://github.com/theyosh/TerrariumPI/issues/34). [TheYOSH]
- Update gentelella. [TheYOSH]

**Other**
- Merge pull request [#35](https://github.com/theyosh/TerrariumPI/issues/35) from theyosh/feature/power_dimmer. [TheYOSH]

  Feature/power dimmer
- Collector code clean up and better data storage and retrieval.
  [TheYOSH]
- Merge branch 'master' into feature/power_dimmer. [TheYOSH]
- Trying to add more stability for dimming hardware. [TheYOSH]
- Remove unused settings for non dimmer switches. [TheYOSH]
- Make PI user restart PiGPIOd process. [TheYOSH]
- Enable pigpiod service at reboot. [TheYOSH]
- Better on and off detection for dimmers. [TheYOSH]
- Merge branch 'master' into feature/power_dimmer. [TheYOSH]


2.8.2 (2017-10-21)
------------------

**New**
- Add sync command. [TheYOSH]

**Fixes**
- Fix wrong timers and updated German language. fix [#33](https://github.com/theyosh/TerrariumPI/issues/33). [TheYOSH]
- Fixed weather icons. [TheYOSH]
- Small HTML fixes. [TheYOSH]
- Fix HTML code in Dutch translation. Was broke in usage page. [TheYOSH]

**Updates**
- Update changelog. [TheYOSH]
- Update version number. [TheYOSH]
- Update README.md. [TheYOSH]
- Update README.md. [TheYOSH]
- Update install and update documentation. [TheYOSH]

**Other**
- Merge branch 'master' of https://github.com/theyosh/TerrariumPI.
  [TheYOSH]
- Refactor weather code to use inheritance. [TheYOSH]
- Merge branch 'master' of https://github.com/theyosh/TerrariumPI.
  [TheYOSH]
- Allow negative temperature settings. [TheYOSH]


2.8.1 (2017-09-30)
------------------

**New**
- Added a link in the Usage link to https://pinout.xyz to help end users
  that are not familiar with different pin numbering, updated and fixed
  some of the italian translation    modified:
  locales/it_IT/LC_MESSAGES/terrariumpi.mo    modified:
  locales/it_IT/LC_MESSAGES/terrariumpi.po    modified:
  locales/terrariumpi.pot. [Lorenzo Faleschini]

**Updates**
- Update changelog. [TheYOSH]
- Update version number. [TheYOSH]
- Update fancybox. [TheYOSH]
- Update switch logging. [TheYOSH]
- Update to switch logging for short duration switching. [TheYOSH]
- Update translations including Italian for better supporting urls in
  text. [TheYOSH]
- Changed "normal" pin numbering with more correct "physiscal" pin
  numbering and updated italian translation. [Lorenzo Faleschini]

  modified:   locales/it_IT/LC_MESSAGES/terrariumpi.mo
  	modified:   locales/it_IT/LC_MESSAGES/terrariumpi.po
  	modified:   locales/terrariumpi.pot
- Update version number in configfile. [TheYOSH]
- Update version number in readme. [TheYOSH]

**Other**
- Finished Dutch translation. [TheYOSH]
- Forced decimal number input by using input patterns. [TheYOSH]
- Merge pull request [#26](https://github.com/theyosh/TerrariumPI/issues/26) from penzoiders/master. [TheYOSH]

  updated translation and original strings to help user with GPIO pinout numbering


2.8 (2017-09-26)
----------------

**New**
- Add update section for updating software from Git. Updated
  installation steps. [TheYOSH]
- Add translation screenshots. [TheYOSH]
- Add German translation first start. [TheYOSH]
- Added logout notification. Refs[#22](https://github.com/theyosh/TerrariumPI/issues/22). [TheYOSH]
- Add logout option. This will change the authentication headers so that
  you are not able to make changes anymore. Ref[#22](https://github.com/theyosh/TerrariumPI/issues/22). [TheYOSH]
- Added localized number and currency formatting. [TheYOSH]
- Added Italian localization, full translation    new file:
  locales/it_IT/LC_MESSAGES/it.mo     new file:
  locales/it_IT/LC_MESSAGES/it.po. [Lorenzo Faleschini]

**Fixes**
- Update switch logging to add the old switch state in front of the new
  state. Should fix broken switch graphs. [TheYOSH]
- Fix translating sensor types. [TheYOSH]

**Updates**
- Update changelog. [TheYOSH]
- Update install script to handle updates better. Forced GPIO pin number
  to float when reading data. [#25](https://github.com/theyosh/TerrariumPI/issues/25). [TheYOSH]
- Update readme file. [TheYOSH]
- Update changelog generator. [TheYOSH]
- Update copyright year. [TheYOSH]
- Updated weather icons. [#23](https://github.com/theyosh/TerrariumPI/issues/23). [TheYOSH]
- Update translations. [TheYOSH]
- Update leaflet to version 1.2.0. [TheYOSH]
- Updated AJAX loader indicator and whitespace. [TheYOSH]
- Small JS updates. [TheYOSH]
- Small js update. [TheYOSH]
- Updated online and door indicators. [TheYOSH]
- Update loading available languages. [TheYOSH]

**Other**
- First final version Germand translation. Close [#23](https://github.com/theyosh/TerrariumPI/issues/23). [TheYOSH]
- Merge branch 'master' of https://github.com/theyosh/TerrariumPI.
  [TheYOSH]
- New screenshots. [TheYOSH]
- Set default language to en_US. [TheYOSH]
- Renamed translation files. [TheYOSH]
- Merge pull request [#21](https://github.com/theyosh/TerrariumPI/issues/21) from penzoiders/master. [TheYOSH]

  Added Italian localization, full translation (first release)


2.7.1 (2017-09-09)
------------------

**New**
- Added description back to working. Fix [#18](https://github.com/theyosh/TerrariumPI/issues/18). [TheYOSH]
- Add a new switch type GPIO-invert. Use it when normal GPIO is working
  in oppisite way. Fix [#20](https://github.com/theyosh/TerrariumPI/issues/20). [TheYOSH]

**Fixes**
- Fix webcam rotation. Settings was not saved at all :( . Fix [#19](https://github.com/theyosh/TerrariumPI/issues/19).
  [TheYOSH]
- Fixed saving new password. Added error feedback when saving is not
  successfull. And better password update check. Fix [#17](https://github.com/theyosh/TerrariumPI/issues/17). [TheYOSH]

**Updates**
- Update changelog. [TheYOSH]
- Update version number. [TheYOSH]
- Update translations files. [TheYOSH]


2.7 (2017-09-04)
----------------

**Fixes**
- Better warning message when sensor measured values are outside given
  ranges. Fix [#16](https://github.com/theyosh/TerrariumPI/issues/16). [TheYOSH]
- Fix switch callback functions. Refs [#15](https://github.com/theyosh/TerrariumPI/issues/15). [TheYOSH]
- Fix adding new temperature sensors. Refs [#15](https://github.com/theyosh/TerrariumPI/issues/15). [TheYOSH]
- Fixed bug found in [#13](https://github.com/theyosh/TerrariumPI/issues/13). Only calculate hours when lights are enabled.
  [TheYOSH]

**Updates**
- Update changelog. [TheYOSH]
- Update readme. [TheYOSH]
- Update gentelella. [TheYOSH]
- Update hardware text. [TheYOSH]
- Update translation. Dutch at 75% [TheYOSH]

**Other**
- Support OpenWeatherMap.org. [TheYOSH]
- Disable extra door and switch logging. [TheYOSH]
- Support up to 8 ports on USB relay switch. [TheYOSH]


2.6 (2017-08-06)
----------------

**New**
- Add profile page reloading after changing profile image. [TheYOSH]
- Add Animal Profile option. [TheYOSH]
- Add robots.txt. [TheYOSH]

**Fixes**
- Small fix. [TheYOSH]
- Fix missing variable in template. [TheYOSH]
- Fix 404 error in template rendering. [TheYOSH]

**Updates**
- Update changelog. [TheYOSH]
- Update changelog. [TheYOSH]
- Update changelog. [TheYOSH]
- Update translations. [TheYOSH]

**Other**
- Merge pull request [#12](https://github.com/theyosh/TerrariumPI/issues/12) from theyosh/feature/profile. [TheYOSH]

  Feature/profile
- Changed profile image uploading. [TheYOSH]
- Moved profile page to main menu. [TheYOSH]
- Remove debug. [TheYOSH]


2.5 (2017-07-28)
----------------

**New**
- Add fancybox. [TheYOSH]
- Added documentation v0.1. [TheYOSH]
- Add IPv6 support. [TheYOSH]

**Fixes**
- Fixed weather usage documentation. [TheYOSH]
- Fix issue [#9](https://github.com/theyosh/TerrariumPI/issues/9). Typo in function call. And extra fix for indicator on
  the weather page. Close [#9](https://github.com/theyosh/TerrariumPI/issues/9). [TheYOSH]

**Updates**
- Update changelog. [TheYOSH]
- Update changelog. [TheYOSH]
- Update documentation part2. [TheYOSH]
- Update readme. [TheYOSH]
- Update screenshots 4. [TheYOSH]
- Update screenshots 3. [TheYOSH]
- Update screenshots 2. [TheYOSH]
- Update screenshots. [TheYOSH]
- Update version number. [TheYOSH]
- Activate config upgrade. [TheYOSH]
- Updated software to run fully in Celsius or Fahrenheit. The option is
  now under system settings and is valid for all temperature
  measurements. [#10](https://github.com/theyosh/TerrariumPI/issues/10). [TheYOSH]

**Other**
- Merge pull request [#11](https://github.com/theyosh/TerrariumPI/issues/11) from theyosh/documentation. [TheYOSH]

  Documentation
- Remove fancybox. [TheYOSH]
- Merge master. [TheYOSH]
- Remove debug. [TheYOSH]
- Documentation part 2. [TheYOSH]
- Merge branch 'master' of https://github.com/theyosh/TerrariumPI.
  [TheYOSH]


2.4.3 (2017-07-21)
------------------

**New**
- Add caching headers for API calls - Now in UTC. [TheYOSH]
- Add caching headers for API calls. [TheYOSH]

**Fixes**
- Merge pull request [#8](https://github.com/theyosh/TerrariumPI/issues/8) from theyosh/fix_environment. [TheYOSH]

  Fix environment
- Fix timer times in environment settings page. [TheYOSH]
- Temperature indicator fix. [TheYOSH]
- Fixed weather sun rise and set times. [TheYOSH]
- Fix update checker. [TheYOSH]
- Fix wrong sensor reads. [TheYOSH]
- Fix gauges. [TheYOSH]
- Fix HTML5 language. [TheYOSH]
- Fix missing weather icon for thunderstorm. [TheYOSH]

**Updates**
- Update changelog. [TheYOSH]
- Update version. [TheYOSH]
- Updated environment engine to support weather and timer mode with or
  without sensors for fine tuning. [TheYOSH]
- Updated weather code. [TheYOSH]
- Updated webcam code. [TheYOSH]
- Updated field descriptions. [TheYOSH]
- Updated switch loading so updating will not switch of existing
  switches. [TheYOSH]

**Other**
- Remove debug. [TheYOSH]
- Remove JS debug. [TheYOSH]
- Remove sunset and sunsrising shifting. [TheYOSH]
- More proper English. [TheYOSH]
- Refactor code to use proper English terms. Will require the renew the
  environment settings. [TheYOSH]


2.4.2 (2017-07-16)
------------------

**New**
- Add version checker. [TheYOSH]
- Add hardware documentation. [TheYOSH]
- Add switch GPIO errors to logfile. [TheYOSH]

**Fixes**
- Fix webcam warmup time variable. [TheYOSH]
- Helpsections are by default closed now. Fixed multiple clicks loaded.
  [TheYOSH]
- Fixed adding sensors and switches to the system. [TheYOSH]
- Fix door status overview page. [TheYOSH]

**Updates**
- Update changelog. [TheYOSH]
- Update version number. [TheYOSH]
- Update language. [TheYOSH]
- Update information page. [TheYOSH]
- Updated required fields. [TheYOSH]
- Update weather logging. [TheYOSH]
- Update OWFS port setting. Now OWFS can be disabled by setting the OWFS
  port to 0. [TheYOSH]

**Other**
- Removed software page. [TheYOSH]
- Remove empty lines. [TheYOSH]


2.4.1 (2017-07-15)
------------------

**New**
- Add js script for translations. [TheYOSH]
- Added git checkout for Gentelella bootstrap 3 template if missing.
  [TheYOSH]
- Add better empty switches/sensors loading. [TheYOSH]
- Added heater and cooler timers fields. [TheYOSH]
- Added style code to hide rows when loading. [TheYOSH]
- Add some debugging. [TheYOSH]
- Add chaching header. Disabled webserver debug output. [TheYOSH]

**Fixes**
- Fix translations. [TheYOSH]
- Fix dashboard environment. [TheYOSH]
- Fix environment. [TheYOSH]
- Fix spelling typos. [TheYOSH]

**Updates**
- Update changelog. [TheYOSH]
- Update US language. [TheYOSH]
- Updated system form fields. [TheYOSH]
- Update translations form fields. [TheYOSH]

**Other**
- Bla. [TheYOSH]
- Rewritten environment code. Reduces a lot of code. [TheYOSH]
- Small changes. [TheYOSH]
- Remove w1 support for switches. [TheYOSH]
- Debug cleanup. [TheYOSH]
- Smaller image. [TheYOSH]


2.4 (2017-07-14)
----------------

**New**
- Added exception handling for wrong GPIO pin number. [TheYOSH]
- Add GPIO relay support. Closes [#3](https://github.com/theyosh/TerrariumPI/issues/3). [TheYOSH]
- Added sprayer modus. Is always sensor for now. [TheYOSH]
- Added cooling system to the environment engine. [TheYOSH]
- Added missing door module. [TheYOSH]
- Add power switch title when hover over it. [TheYOSH]
- Added support for Raspberry PI 1Wire interface sensors. For now only
  temperature sensors are supported. [#2](https://github.com/theyosh/TerrariumPI/issues/2). [TheYOSH]
- Add support for GPIO (DHT11, DHT22 and AM2302) sensors. [TheYOSH]
- Added support for Weater underground API data. [TheYOSH]
- Added form fields explanations (2) [TheYOSH]
- Added help pages for dashboard and weather page (2) [TheYOSH]
- Added help pages for dashboard and weather page. [TheYOSH]
- Added form fields explanations. [TheYOSH]
- Added extra help to weather settings page. [TheYOSH]
- Added door history to dashboard. [TheYOSH]
- Added extra switch and door logging for better graphs. [TheYOSH]
- Added changelog. [TheYOSH]
- Add door open duration and fixed data processing or door and swiches.
  [TheYOSH]
- Add missing title to the door status. [TheYOSH]
- Added missing module for handling errors from the raspberry pi camera.
  [TheYOSH]
- Added error logging to sensor object. [TheYOSH]
- Add door indicator logging and graphing. [TheYOSH]

**Fixes**
- Fixes for UX. [TheYOSH]
- Fix removing switches. [TheYOSH]
- Fix content height. [TheYOSH]
- Fix content heights (3) [TheYOSH]
- Fix content heights (2) [TheYOSH]
- Fix content heights. [TheYOSH]
- Fix for loading environment settings page. [TheYOSH]
- Fix environent on dashboard. [TheYOSH]
- Fix. [TheYOSH]
- Fix form processing. [TheYOSH]
- Fix switch on detection. [TheYOSH]
- Fix power switch logging. [TheYOSH]
- Fix cleaning all sensors. [TheYOSH]
- Update changelog. Fixes [#2](https://github.com/theyosh/TerrariumPI/issues/2). [TheYOSH]
- Fix environment measurement. [TheYOSH]
- Fix 1 wire sensor detection. [#2](https://github.com/theyosh/TerrariumPI/issues/2). [TheYOSH]
- Fix SSL issue with weather data. [TheYOSH]
- Fixes for other graphs and fixed processing sensor update form. Ref
  [#2](https://github.com/theyosh/TerrariumPI/issues/2). [TheYOSH]
- Fix initial loading of total values for power and water. [TheYOSH]
- Fix loading graphs when there is no data. [TheYOSH]
- Fix wunderground weather data forecast. Missing data reset. [TheYOSH]
- Fixed dashboard environment warning icons spacing. [TheYOSH]
- Fixed Changelog output. [TheYOSH]
- Fix humidity icon in sensor list. [TheYOSH]
- Fix door graphs (2) [TheYOSH]
- Fix door graphs. [TheYOSH]
- Fix Gauge.js graphs (2) [TheYOSH]
- Fix Gauge.js graphs. [TheYOSH]
- Fixed door check in spray system. [TheYOSH]
- Fix door history. [TheYOSH]

**Updates**
- Update changelog. [TheYOSH]
- Update readme. [TheYOSH]
- Update readme for GPIO relay board. [TheYOSH]
- Revert UX updates. [TheYOSH]
- Update readme file. [TheYOSH]
- Small UX updates. [TheYOSH]
- Updated cooler dashboard. Switched min and max value. [TheYOSH]
- Update weather icons. [TheYOSH]
- More small updates. [TheYOSH]
- Small updates. [TheYOSH]
- Update webcam system. [TheYOSH]
- Small updates. [TheYOSH]
- Updated door system code. [TheYOSH]
- Updated config settings. [TheYOSH]
- Updated readme file for more information about sensor support. [#2](https://github.com/theyosh/TerrariumPI/issues/2).
  [TheYOSH]
- Update install location Adafruit libraries. [TheYOSH]
- Update startup script. [TheYOSH]
- Updated notification timestamp data fields. [TheYOSH]
- Update changelog. [TheYOSH]

  Better format
- Small updates. [TheYOSH]
- Updated English language. [TheYOSH]
- Updated code to support multiple door sensors. [TheYOSH]
- Updated translations. [TheYOSH]
- Updated UX. [TheYOSH]
- Update to latest gauge.js. Version 1.3.4. [TheYOSH]
- Update Leaflet.loading to version 0.1.24. [TheYOSH]
- Upgrade Leaflet.fullscreen to version 1.0.2. [TheYOSH]
- Update leaflet to version 1.1.0. [TheYOSH]
- Update Gentelella. [TheYOSH]
- Update missing translations. [TheYOSH]

**Other**
- Merge branch 'master' of https://github.com/theyosh/TerrariumPI.
  [TheYOSH]
- Merge pull request [#7](https://github.com/theyosh/TerrariumPI/issues/7) from theyosh/cooler. [TheYOSH]

  Merge Cooler system
- Merge branch 'master' of https://github.com/theyosh/TerrariumPI.
  [TheYOSH]
- Merge branch 'master' of https://github.com/theyosh/TerrariumPI.
  [TheYOSH]
- Change default logging to info. [TheYOSH]
- In preperation for [#3](https://github.com/theyosh/TerrariumPI/issues/3) the power switch system has been rewritten to
  add and delete power switches. [TheYOSH]
- Merge pull request [#4](https://github.com/theyosh/TerrariumPI/issues/4) from theyosh/gpio_sensors. [TheYOSH]

  Merge gpio sensors branch to master
- Changed term 1wire to OWFS to support Raspberry PI 1 Wire overlay. [#2](https://github.com/theyosh/TerrariumPI/issues/2).
  [TheYOSH]
- Cleanup spaces. [TheYOSH]
- Removed debugging. [TheYOSH]
- Support for not using some parts of the environment system. [TheYOSH]
- Removed the doorpin config from general settings page. [TheYOSH]
- Typo. [TheYOSH]
- Moved door status to own page. [TheYOSH]
- Use system default pip. [TheYOSH]
