Changelog
=========


2.5(2017-07-28)
------------------

**New**
- Add fancybox. [TheYOSH]
- Added documentation v0.1. [TheYOSH]
- Add IPv6 support. [TheYOSH]

**Fixes**
- Fixed weather usage documentation. [TheYOSH]
- Fix issue #9. Typo in function call. And extra fix for indicator on
  the weather page. Close #9. [TheYOSH]

**Updates**
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
  measurements. #10. [TheYOSH]

**Other**
- Merge pull request #11 from theyosh/documentation. [TheYOSH]

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
- Merge pull request #8 from theyosh/fix_environment. [TheYOSH]

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
- Add GPIO relay support. Closes #3. [TheYOSH]
- Added sprayer modus. Is always sensor for now. [TheYOSH]
- Added cooling system to the environment engine. [TheYOSH]
- Added missing door module. [TheYOSH]
- Add power switch title when hover over it. [TheYOSH]
- Added support for Raspberry PI 1Wire interface sensors. For now only
  temperature sensors are supported. #2. [TheYOSH]
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
- Update changelog. Fixes #2. [TheYOSH]
- Fix environment measurement. [TheYOSH]
- Fix 1 wire sensor detection. #2. [TheYOSH]
- Fix SSL issue with weather data. [TheYOSH]
- Fixes for other graphs and fixed processing sensor update form. Ref
  #2. [TheYOSH]
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
- Updated readme file for more information about sensor support. #2.
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
- Merge pull request #7 from theyosh/cooler. [TheYOSH]

  Merge Cooler system
- Merge branch 'master' of https://github.com/theyosh/TerrariumPI.
  [TheYOSH]
- Merge branch 'master' of https://github.com/theyosh/TerrariumPI.
  [TheYOSH]
- Change default logging to info. [TheYOSH]
- In preperation for #3 the power switch system has been rewritten to
  add and delete power switches. [TheYOSH]
- Merge pull request #4 from theyosh/gpio_sensors. [TheYOSH]

  Merge gpio sensors branch to master
- Changed term 1wire to OWFS to support Raspberry PI 1 Wire overlay. #2.
  [TheYOSH]
- Cleanup spaces. [TheYOSH]
- Removed debugging. [TheYOSH]
- Support for not using some parts of the environment system. [TheYOSH]
- Removed the doorpin config from general settings page. [TheYOSH]
- Typo. [TheYOSH]
- Moved door status to own page. [TheYOSH]
- Use system default pip. [TheYOSH]
