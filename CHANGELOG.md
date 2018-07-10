Changelog
=========


3.8.1 (2018-07-10)
------------------

**New**
------
- Add sorting on different pages. [theyosh]

**Fixes**
------
- Fix typo. [theyosh]
- Fix starting up with no data in the database. [#168](https://github.com/theyosh/TerrariumPI/issues/168). [theyosh]
- Fixed caching issue when chaning settings. [#167](https://github.com/theyosh/TerrariumPI/issues/167). [theyosh]
- Fix Telegram Bot going to soon. [theyosh]

**Updates**
------
- Update version. [theyosh]
- Update README.md. [TheYOSH]
- Update data gaphing and finetuning SQL. [theyosh]
- Update installer for OLED displays. [theyosh]

**Other**
------
- Do not change dimmer up or down when running. On and off is still
  possible. [theyosh]
- Finetuning Notifications. Renamed LCD to Display for general name and
  support OLED screens. [#164](https://github.com/theyosh/TerrariumPI/issues/164). [theyosh]


3.8.0 (2018-07-01)
------------------

**New**
------
- Added support for LCD screens through notification system. [#164](https://github.com/theyosh/TerrariumPI/issues/164) [#101](https://github.com/theyosh/TerrariumPI/issues/101).
  [theyosh]
- Add proxy support for Telegram. [#161](https://github.com/theyosh/TerrariumPI/issues/161). [theyosh]

**Fixes**
------
- Fixing hanging Telegram Bot. [theyosh]
- Rewriting getting remote data. Trying to fix proxy issues with
  Telegram. [#161](https://github.com/theyosh/TerrariumPI/issues/161). [theyosh]
- Fix missing dimmer step setting. [theyosh]
- Fix database recovery. [theyosh]
- Fix environment status for manual power switch toggling. [theyosh]
- Better fix for tooltips in graphs. [theyosh]
- Fix tooltip HTML code. [theyosh]
- Fix telegram bot socks setting [#161](https://github.com/theyosh/TerrariumPI/issues/161). [theyosh]
- Fix total power usage (2) [theyosh]
- Fix total power usage. [theyosh]
- Fixing telegram bot to be more resistant to errors. [theyosh]

**Updates**
------
- Update changelog. [theyosh]
- Update changelog. [theyosh]
- Update README.md. [TheYOSH]
- Update translations. [theyosh]
- Small update to installer and reload message settings after saving.
  [#101](https://github.com/theyosh/TerrariumPI/issues/101) [#161](https://github.com/theyosh/TerrariumPI/issues/161). [theyosh]
- Small update to installer and reload message settings after saving.
  [#101](https://github.com/theyosh/TerrariumPI/issues/101) [#161](https://github.com/theyosh/TerrariumPI/issues/161). [theyosh]
- Update Telegram box proxy settings. [theyosh]
- Better and safer upgrade. [theyosh]
- Update version number. [theyosh]
- Updated data collector:   - Removed duplicate data records for power
  switches and doors   - Added and changed indexes for faster quering
  - Put more logic in queries and less in code. [theyosh]

  This will improve the overall query time with 50%. And improve the average query times with 400%!!

**Other**
------
- Merge pull request [#165](https://github.com/theyosh/TerrariumPI/issues/165) from theyosh/development. [TheYOSH]

  Release 3.8.0
- Finetuning. [theyosh]
- Smoothen the dimmer. [theyosh]
- Auto decode HTML content. [theyosh]
- Restart Telegram Bot after changing settings if needed. [theyosh]
- Stop after 2 errors. [theyosh]
- Code cleanup. [theyosh]
- Move timestamp to LCD code. [theyosh]
- Merge branch 'development' of ssh://github.com/theyosh/TerrariumPI
  into development. [theyosh]
- Remove debig. [theyosh]
- Final collector code. And good looking graphs. [theyosh]
- Merge branch 'master' into development. [theyosh]
- Merge pull request [#162](https://github.com/theyosh/TerrariumPI/issues/162) from theyosh/development. [TheYOSH]

  Add proxy support for Telegram. [#161](https://github.com/theyosh/TerrariumPI/issues/161)
- Stash. [theyosh]
- Another attempt to get the powerswitches and door nicer graphs.
  [theyosh]
- Change quotes. [theyosh]


3.7.0 (2018-06-20)
------------------

**New**
------
- Add some extra checks. [theyosh]
- Add link to Telegram bot. [#101](https://github.com/theyosh/TerrariumPI/issues/101). [theyosh]
- Add logging explanations. [theyosh]
- Add notification message rate limits. [#101](https://github.com/theyosh/TerrariumPI/issues/101). [theyosh]
- Add NTP to the installation. [theyosh]
- Add better error logging for notifications. Fixed message parsing for
  variables. [theyosh]
- Add notifications page. [theyosh]

**Fixes**
------
- Fix not recogniced images. [#101](https://github.com/theyosh/TerrariumPI/issues/101). [theyosh]
- Fix profile image path. [#101](https://github.com/theyosh/TerrariumPI/issues/101). [theyosh]
- Fix 1 minute timer actions. [theyosh]
- Fix config upgrade. [#155](https://github.com/theyosh/TerrariumPI/issues/155). [theyosh]

**Updates**
------
- Update CHANGELOG. [theyosh]
- Update version number. [theyosh]
- Update twitter image based on profile image. [#101](https://github.com/theyosh/TerrariumPI/issues/101). [theyosh]
- Update notification translations. [#101](https://github.com/theyosh/TerrariumPI/issues/101). [theyosh]
- Update README.md. [TheYOSH]

  Add notification information
- Update notification system. [#101](https://github.com/theyosh/TerrariumPI/issues/101). [theyosh]
- Updated some logging and installer messages. [theyosh]
- Next rounds of updates for notifications. [#101](https://github.com/theyosh/TerrariumPI/issues/101). [theyosh]
- Update terrariumUtils.py. [TheYOSH]

  Fix bug [#155](https://github.com/theyosh/TerrariumPI/issues/155)

**Other**
------
- Merge pull request [#160](https://github.com/theyosh/TerrariumPI/issues/160) from theyosh/development. [TheYOSH]

  New release
- Some cosmetic touchups... [#101](https://github.com/theyosh/TerrariumPI/issues/101). [theyosh]
- Remove debug. [theyosh]
- Typo. [theyosh]
- Rewritten TelegramBot. [#101](https://github.com/theyosh/TerrariumPI/issues/101). [theyosh]
- Support for HTML multipart email messages with profile image. [#101](https://github.com/theyosh/TerrariumPI/issues/101).
  [theyosh]
- More notifications finetuning. Adding traffic light support for system
  messages. [#101](https://github.com/theyosh/TerrariumPI/issues/101). [theyosh]
- Merge branch 'development' of ssh://github.com/theyosh/TerrariumPI
  into development. [theyosh]
- Enable powerswitches and sensors to send notifications. [#101](https://github.com/theyosh/TerrariumPI/issues/101).
  [theyosh]
- Finetuning notifications. [theyosh]
- Better log formatting. [theyosh]
- Move mail checks and options. [theyosh]
- Better environment logic for messaging. [theyosh]
- Secure the notification config data with authentication due to private
  tokens. [theyosh]
- Merge branch 'master' into notifications. [theyosh]
- Stash first part notifications. [#101](https://github.com/theyosh/TerrariumPI/issues/101). [theyosh]
- Fine tune chirp sensor. [theyosh]


3.6.0 (2018-05-31)
------------------

**New**
------
- Add support for Chirp moisture/temperature/brightness sensors.
  https://wemakethings.net/chirp/ [#133](https://github.com/theyosh/TerrariumPI/issues/133). [theyosh]
- Add new package dependency. [#149](https://github.com/theyosh/TerrariumPI/issues/149). [theyosh]
- Add webcam config upgrade. [theyosh]
- Add archive timer for webcams. [theyosh]
- Add Telegram bot contribution. Thanks to [@BashSer.](https://github.com/BashSer.) [theyosh]

**Fixes**
------
- Fix HTTP vs HTTPS urls and give visual feedback when wrong url is
  used. [#154](https://github.com/theyosh/TerrariumPI/issues/154). [theyosh]
- Fix dashboard. [theyosh]
- Fix data and config values for environment. [theyosh]
- Fix file uploading. [theyosh]
- Quick fix sprayer info. [TheYOSH]
- Fix logrotating on tmpfs. [#148](https://github.com/theyosh/TerrariumPI/issues/148). [theyosh]
- Fix graph legend backgrond. [theyosh]

**Updates**
------
- Update changelog. [theyosh]
- Update environment page. [theyosh]
- Update environment page. [theyosh]
- Update README.md. [TheYOSH]
- Update languages. [theyosh]
- Better update migration. [theyosh]
- Update translations. [theyosh]
- Update README.md. [TheYOSH]
- Update environment system. [#150](https://github.com/theyosh/TerrariumPI/issues/150). [theyosh]
- Update I2C timing to double the max timeouts. [theyosh]
- Update environment. [#150](https://github.com/theyosh/TerrariumPI/issues/150). [theyosh]
- Update environment engine. Complete rewrite of code. Now you can
  select power switches for low alarm and high alarm. [#150](https://github.com/theyosh/TerrariumPI/issues/150). [theyosh]
- Updated 100% italian translation + corrections, compiled MO file.
  [Lorenzo Faleschini]

**Other**
------
- Merge for release. [theyosh]
- Small environment adjustments. [theyosh]
- Merge branch 'development' of ssh://github.com/theyosh/TerrariumPI
  into development. [theyosh]
- Better light and door dependency description. [theyosh]
- Make log symlink as running user. [theyosh]
- Second part of new environment. [#150](https://github.com/theyosh/TerrariumPI/issues/150). [theyosh]
- Better Chirp support. [theyosh]
- Change accesslogfile. [#148](https://github.com/theyosh/TerrariumPI/issues/148). [theyosh]
- Changed moisture logic. [#133](https://github.com/theyosh/TerrariumPI/issues/133). [theyosh]
- Finetune webcam archive. [theyosh]
- Merge pull request [#147](https://github.com/theyosh/TerrariumPI/issues/147) from penzoiders/master. [TheYOSH]

  updated 100% italian translation + corrections, compiled MO file


3.5.0 (2018-05-05)
------------------

**New**
------
- Add moisture environment. [#133](https://github.com/theyosh/TerrariumPI/issues/133). [theyosh]
- Add Ph environment part. [#135](https://github.com/theyosh/TerrariumPI/issues/135). [theyosh]
- Add moisture environment system. [#133](https://github.com/theyosh/TerrariumPI/issues/133). [theyosh]
- Add extra check if sensors are operational when used in environment
  system. This will add an error indicator per environmentpart on the
  dashboard and an error badge on each graph that has a not working
  sensor. A sensor is not working when there are no updates for 10
  minutes. When there are zero working sensors in the environmentpart,
  it will we forced to be put to off. [#142](https://github.com/theyosh/TerrariumPI/issues/142). [theyosh]
- Add horizontal graph legends option. [#143](https://github.com/theyosh/TerrariumPI/issues/143). [theyosh]
- Add remote PH sensor support. [theyosh]
- Add EC (Electrical conductivity) expressed in mS (microSiemens)
  [nke69]
- Add EC (Electrical conductivity) expressed in mS (microSiemens)
  [nke69]
- Add power management options to YT-XX sensors through extra use of
  GPIO port for power. [theyosh]
- Add moisture support for YT-XX sensors through digital port. Either
  sensing dry or wet. [#133](https://github.com/theyosh/TerrariumPI/issues/133). [theyosh]
- Add extra debug logging check. [theyosh]
- Add extra float check. [theyosh]
- Add option for selecting source for day and night temperature shift.
  [#139](https://github.com/theyosh/TerrariumPI/issues/139). [TheYOSH]
- Add files via upload. [TheYOSH]

**Fixes**
------
- Fixed moisture sensor. [#133](https://github.com/theyosh/TerrariumPI/issues/133). [theyosh]
- Finally found the memory leak!! Fixed!! [theyosh]
- Fix memory leaks and moisture limits changes. [theyosh]
- Fix Si7021 sensor. [#129](https://github.com/theyosh/TerrariumPI/issues/129). [theyosh]
- Fix pH environmentpart [#145](https://github.com/theyosh/TerrariumPI/issues/145). [theyosh]
- Fix dashboard loading. [theyosh]
- Fix IP number in startup script. [theyosh]
- Fix terrariumHCSR04Sensor. [theyosh]
- Fix power management. [#133](https://github.com/theyosh/TerrariumPI/issues/133). [theyosh]
- Fix I2C settings per sensor. [#129](https://github.com/theyosh/TerrariumPI/issues/129). [theyosh]
- Fix stupid Apple rendering bug! Fix [#134](https://github.com/theyosh/TerrariumPI/issues/134). [TheYOSH]
- Fix image motion detection with image rotations. [#137](https://github.com/theyosh/TerrariumPI/issues/137). [TheYOSH]
- Do not overwrite image resolutions after rotations. [TheYOSH]

**Updates**
------
- Update changelog. [theyosh]
- Update translations. [theyosh]
- Update version number. [theyosh]
- Update README.md. [TheYOSH]
- Update library fancybox. [TheYOSH]
- Update dashboard page. [theyosh]
- Update submodules. [theyosh]
- Update translations. [theyosh]
- Update icons. [theyosh]
- Update dashboard to show all averagetypes. [theyosh]
- Updated I2C sensor support. Rewritten existing code. And added
  (untested) support for si7021 and hdu21d. [#129](https://github.com/theyosh/TerrariumPI/issues/129). [theyosh]
- Update installer. Add option to skip cleanup of existing unneeded
  programs. [TheYOSH]
- Update German translations. [#115](https://github.com/theyosh/TerrariumPI/issues/115). Close [#138](https://github.com/theyosh/TerrariumPI/issues/138). [TheYOSH]
- Updated the installer with graphical dialog. [TheYOSH]
- Update webcam archiving. Add better exception handling. [TheYOSH]
- Small webcam update. [TheYOSH]
- Update README.md. [TheYOSH]
- Update README.md. [TheYOSH]
- Update translation files. [nke69]

  Update translation files for 3.4.2

**Other**
------
- Code cleanup. [theyosh]
- Increase humidity time read out. [#129](https://github.com/theyosh/TerrariumPI/issues/129). [theyosh]
- Save motion images to new folder structure in Y/M/D format. [theyosh]
- Speedup dashboard loading. [theyosh]
- Code cleanup. [theyosh]
- Merge branch 'master' of ssh://github.com/theyosh/TerrariumPI.
  [theyosh]
- Refactoring terrariumpi sensors code. [theyosh]
- Objects new style. [theyosh]
- New style python objects. [theyosh]
- Merge pull request [#144](https://github.com/theyosh/TerrariumPI/issues/144) from nke69/master. [TheYOSH]

  Add EC (Electrical conductivity) expressed in mS (microSiemens)
- Add EC (Electrical conductivity) expressed in mS (microSiemens)
  [nke69]
- Add EC (Electrical conductivity) expressed in mS (microSiemens)
  [nke69]
- First attempt adding support for BME280/BMP280 chips.This code is
  UNTESTED [#129](https://github.com/theyosh/TerrariumPI/issues/129). [theyosh]
- Merge branch 'master' of ssh://github.com/theyosh/TerrariumPI.
  [TheYOSH]
- Merge pull request [#136](https://github.com/theyosh/TerrariumPI/issues/136) from nke69/master. [TheYOSH]

  Update translation files


3.4.2 (2018-04-09)
------------------

**New**
------
- Add webcam archiving based on motion detection. [TheYOSH]
- Add webcam archiving. Testing n ow. [TheYOSH]
- Add extra checks. [TheYOSH]
- Add sensor cleanup. [TheYOSH]
- Add support for SHT2X sensors. [#84](https://github.com/theyosh/TerrariumPI/issues/84). [TheYOSH]
- Add external calendar support. [#124](https://github.com/theyosh/TerrariumPI/issues/124). [TheYOSH]
- Add external calendar support. [#124](https://github.com/theyosh/TerrariumPI/issues/124). [TheYOSH]
- Add empty folder for external json data. [TheYOSH]
- Add empty folder for external json data. [TheYOSH]
- Add remote doors support. Will update once every 30 seconds. [#124](https://github.com/theyosh/TerrariumPI/issues/124).
  [TheYOSH]
- Add files via upload. [nke69]

  Added "PH" value to display ph value in the graphics.
  Continued from https://github.com/theyosh/TerrariumPI/issues/87
- Add "PH" value. [nke69]

  Add "PH" value to collect information into the database.
  Continued from https://github.com/theyosh/TerrariumPI/issues/87

**Fixes**
------
- Fix reading negative temperature values for 1-wire devices. [TheYOSH]
- Fix weather settings link. [TheYOSH]

**Updates**
------
- Update README.md. [TheYOSH]
- Update README.md. [TheYOSH]
- Update changelog. [TheYOSH]
- Update translation files. [TheYOSH]
- Update version number. [TheYOSH]
- Update submodules. [TheYOSH]
- Update translations. [TheYOSH]

**Other**
------
- Merge branch 'master' of ssh://github.com/theyosh/TerrariumPI.
  [TheYOSH]
- Different motion detection. Should work better with low light (2)
  [TheYOSH]
- Different motion detection. Should work better with low light.
  [TheYOSH]
- Remove debug output. [TheYOSH]
- Better sensor checking. [TheYOSH]
- Bla. [TheYOSH]
- Better handling of offline remote data. [TheYOSH]
- Change PH to pH. [TheYOSH]
- Some finetuning. [#125](https://github.com/theyosh/TerrariumPI/issues/125). [TheYOSH]
- Merge pull request [#125](https://github.com/theyosh/TerrariumPI/issues/125) from nke69/master. [TheYOSH]

  Adding "PH" value in database
- Display PH Graphs. [nke69]

  Added the value "PH" for displaying graphs.
  Continued from https://github.com/theyosh/TerrariumPI/issues/87


3.4.1 (2018-03-19)
------------------

**New**
------
- Add pushnotification through external script. Thanks [@kahuwi14](https://github.com/kahuwi14) [#101](https://github.com/theyosh/TerrariumPI/issues/101).
  [TheYOSH]
- Add day/night temperature difference in heater environment system.
  [#106](https://github.com/theyosh/TerrariumPI/issues/106). [TheYOSH]
- Add smart dimming in heater and cooler environment system. [#106](https://github.com/theyosh/TerrariumPI/issues/106).
  [TheYOSH]
- Add NGINX vHost config for running on port 80. [#113](https://github.com/theyosh/TerrariumPI/issues/113). [TheYOSH]
- Added missing translation. [TheYOSH]
- Add logfile status indicator in the footer. [TheYOSH]
- Add program lshw depedency. [TheYOSH]
- Add visual feedback when there are no sensors / switches / etc
  available. [TheYOSH]
- Add device information in the footer of the webinterface. [TheYOSH]

**Fixes**
------
- Test for fixing DHT issues. [#118](https://github.com/theyosh/TerrariumPI/issues/118) [#120](https://github.com/theyosh/TerrariumPI/issues/120). [TheYOSH]
- Fix adding new webcams. [TheYOSH]
- Fix adding new webcams. [TheYOSH]

**Updates**
------
- Update CHANGELOG.md. [TheYOSH]
- Update changelog. [TheYOSH]
- Update notification script. [#101](https://github.com/theyosh/TerrariumPI/issues/101). [TheYOSH]
- Update changelog. [TheYOSH]
- Update README.md. [TheYOSH]
- Update README.md. [TheYOSH]
- Update changelog. [TheYOSH]
- Updated translation generator. [TheYOSH]
- Update notify contrib code by [@kahuwi14.](https://github.com/kahuwi14.) [TheYOSH]
- Update translations. [TheYOSH]
- Update translations. [TheYOSH]
- Update environment dashboard (2) [TheYOSH]
- Update environment dashboard. [TheYOSH]
- Update system settings page. [TheYOSH]
- Update initial loading. [TheYOSH]
- Update German language. Thanks [@Barbara1984.](https://github.com/Barbara1984.) Close [#111](https://github.com/theyosh/TerrariumPI/issues/111). [TheYOSH]
- Update translation to reflect correct fr, minor bug with translation.
  [nke69]
- Update German translation. Thanks to [@Barbara1984](https://github.com/Barbara1984) [#105](https://github.com/theyosh/TerrariumPI/issues/105). [TheYOSH]

**Other**
------
- Merge branch 'development' [TheYOSH]
- Revert back code for DHT sensors. Add extra timeout per DHT readout.
  Will slow down the process, but will also give the DHT sensors more
  time to produce data. [#120](https://github.com/theyosh/TerrariumPI/issues/120). [TheYOSH]
- Merge with master. [TheYOSH]
- Better pin cleanup. [TheYOSH]
- Better settings checking. [#116](https://github.com/theyosh/TerrariumPI/issues/116). [TheYOSH]
- Better PiGPIOd connections(3) [TheYOSH]
- Better PiGPIOd connections(2) [TheYOSH]
- Better PiGPIOd connections. [TheYOSH]
- Cleanup of GPIO pins. [TheYOSH]
- Only allow up and down dimming with dimmer power switches. Respect the
  max on and off dimmer percentage when going up or down. [#106](https://github.com/theyosh/TerrariumPI/issues/106).
  [TheYOSH]
- Better memory usage reporting in status view. Close [#117](https://github.com/theyosh/TerrariumPI/issues/117). [TheYOSH]
- Cleanup dashboard. [TheYOSH]
- Changed weather forecast to just weather. [TheYOSH]
- Merge pull request [#119](https://github.com/theyosh/TerrariumPI/issues/119) from nke69/master. [TheYOSH]

  Update translation to reflect correct fr, minor bug with translation.


3.4.0 (2018-02-25)
------------------

**New**
------
- Add debug for testing. [TheYOSH]
- Add PH indicator. [#108](https://github.com/theyosh/TerrariumPI/issues/108). [TheYOSH]
- Add traduction and minor bug. [nke69]

  Add description for new changes [#87](https://github.com/theyosh/TerrariumPI/issues/87) and minor bug in traduction
- Add watertank actions based on sensors or timer data. Enable automatic
  switchig on water pumps. [#87](https://github.com/theyosh/TerrariumPI/issues/87). [TheYOSH]
- Add water tank sensor photos. [TheYOSH]
- Add watertank environment part. It does only measurement. No actions
  yet. [#87](https://github.com/theyosh/TerrariumPI/issues/87). [TheYOSH]
- Add HC-SR04-Ultrasonic-Sensor support part1.1 [#87](https://github.com/theyosh/TerrariumPI/issues/87). [TheYOSH]
- Add HC-SR04-Ultrasonic-Sensor support part1 [#87](https://github.com/theyosh/TerrariumPI/issues/87). [TheYOSH]
- Add option to add full authentication. [#102](https://github.com/theyosh/TerrariumPI/issues/102). [TheYOSH]
- Add extra check for remote Energenie power switches. [TheYOSH]
- Add auto updater to start script. Add reboot question in installer
  script. [TheYOSH]
- Add support for Energenie LAN power switches. [#95](https://github.com/theyosh/TerrariumPI/issues/95). [TheYOSH]
- Add support for Energenie USB powerswitches. [#95](https://github.com/theyosh/TerrariumPI/issues/95). [TheYOSH]
- Add files via upload. [nke69]
- Add log page. [TheYOSH]
- Add files via upload. [nke69]
- Add resolution settings to webcams. [#91](https://github.com/theyosh/TerrariumPI/issues/91). [TheYOSH]

**Fixes**
------
- Fixed gpiozero library installation. [TheYOSH]
- Fix array selecting. [TheYOSH]
- Another fix for PH devices [#108](https://github.com/theyosh/TerrariumPI/issues/108). [TheYOSH]
- Fix missing GPIO to BCM conversion. [#108](https://github.com/theyosh/TerrariumPI/issues/108). [TheYOSH]
- Fix on/off detection with zeor power switches. [TheYOSH]
- Fix dashboard js bug. [TheYOSH]
- Finetune distance sensor code and fix OWFS sensor scanning. [TheYOSH]
- Updates for measurements in centimetre or inches [#87](https://github.com/theyosh/TerrariumPI/issues/87). Various small
  fixes and code cleanup regarding [#87](https://github.com/theyosh/TerrariumPI/issues/87). [TheYOSH]
- Fix gauge graphs. Fix sensor indicators. [TheYOSH]
- Fix lights bug when combination off weather and no min and max hours.
  [TheYOSH]
- Fix bug in clearing power switches and sensors. Do NOT make code at 3
  in the night :). Fix [#104](https://github.com/theyosh/TerrariumPI/issues/104). [TheYOSH]
- Fix US date parsing. [#97](https://github.com/theyosh/TerrariumPI/issues/97). [TheYOSH]
- Fix adding new switches. [#97](https://github.com/theyosh/TerrariumPI/issues/97). [TheYOSH]
- Changed installation script to support other user then pi to run the
  software [#96](https://github.com/theyosh/TerrariumPI/issues/96). Changed pip installer so it could fix [#81](https://github.com/theyosh/TerrariumPI/issues/81). And added
  support for remote usb power switches [#95](https://github.com/theyosh/TerrariumPI/issues/95). [TheYOSH]
- Fix stupid copy paste code actions. [#94](https://github.com/theyosh/TerrariumPI/issues/94). [TheYOSH]
- Fix form validation. Close [#93](https://github.com/theyosh/TerrariumPI/issues/93). [TheYOSH]

**Updates**
------
- Update changelog. [TheYOSH]
- Update defaults.cfg. [TheYOSH]
- Update README.md. [TheYOSH]
- Update README.md. [TheYOSH]
- Update README.md. [TheYOSH]
- Update changelog. [TheYOSH]
- Update documentation and use liters for watertank dashboard. [TheYOSH]
- Update UI icons. [TheYOSH]
- Update changelog. [TheYOSH]
- Update README.md. [TheYOSH]
- Update README.md. [TheYOSH]
- Update weather based timing. [TheYOSH]
- Update submodule Leaflet.fullscreen. [TheYOSH]
- Update submodule gentelella. [TheYOSH]
- Update German translation. Thanks to [@Barbara1984](https://github.com/Barbara1984) [#105](https://github.com/theyosh/TerrariumPI/issues/105). [TheYOSH]
- Update changelog. [TheYOSH]
- Update README.md. [TheYOSH]
- Small update to the installler. [TheYOSH]
- Update README.md. [TheYOSH]

**Other**
------
- Merge pull request [#109](https://github.com/theyosh/TerrariumPI/issues/109) from theyosh/feature/ph. [TheYOSH]

  Feature/ph
- Merge branch 'feature/ph' of ssh://github.com/theyosh/TerrariumPI into
  feature/ph. [TheYOSH]
- Cleaup debug code. [#108](https://github.com/theyosh/TerrariumPI/issues/108). [TheYOSH]
- We measure in smaller values. [#108](https://github.com/theyosh/TerrariumPI/issues/108). [TheYOSH]
- First attempt for supporting PH device. [#87](https://github.com/theyosh/TerrariumPI/issues/87). [TheYOSH]
- Better export date formatting. [TheYOSH]
- Merge pull request [#107](https://github.com/theyosh/TerrariumPI/issues/107) from nke69/master. [TheYOSH]

  Add traduction and minor bug
- Hide environment part status indicator when there are no switchtes
  selected. [TheYOSH]
- Force sensor start time. [TheYOSH]
- Found the magic number [#82](https://github.com/theyosh/TerrariumPI/issues/82). [TheYOSH]
- Code cleanup. [TheYOSH]
- Code Cleanup. [TheYOSH]
- Cleanup sensor scanning. [TheYOSH]
- Load last 100KB of logfile data to start with. Add option to download
  full logfile. [TheYOSH]
- Merge branch 'master' of https://github.com/theyosh/TerrariumPI.
  [TheYOSH]
- Keep tailing after logfile rotation. [TheYOSH]
- Merge pull request [#98](https://github.com/theyosh/TerrariumPI/issues/98) from nke69/master. [TheYOSH]

  Update France language by [@nke69](https://github.com/nke69)
- Remove the wrongly add button from the environment page. [#97](https://github.com/theyosh/TerrariumPI/issues/97).
  [TheYOSH]
- Merge branch 'master' of https://github.com/theyosh/TerrariumPI.
  [TheYOSH]
- Translate table fields to France. [#92](https://github.com/theyosh/TerrariumPI/issues/92). [TheYOSH]
- Merge pull request [#92](https://github.com/theyosh/TerrariumPI/issues/92) from nke69/master. [TheYOSH]

  Merged language france


3.3.0 (2018-02-06)
------------------

**New**
------
- Add debug logging. [TheYOSH]
- Add photo saving option to the webcam. [TheYOSH]
- Added first part for timer functionality with power switches. This
  update brings only updates to the webinterface and configuration. The
  timer functionality is not yet implemented. [#72](https://github.com/theyosh/TerrariumPI/issues/72). [TheYOSH]
- Add export data option. [#69](https://github.com/theyosh/TerrariumPI/issues/69). [TheYOSH]
- Add extra information when TerrariumPI starts. [TheYOSH]

**Fixes**
------
- Fix average temperatur readout. [TheYOSH]
- Fix open door logging. [TheYOSH]
- Fix audio player time display. [TheYOSH]
- Fix showing times instead of alarms when using timer mode. Fix [#85](https://github.com/theyosh/TerrariumPI/issues/85).
  [TheYOSH]
- Fix timers. [TheYOSH]
- Fix saving new remote webcam. [TheYOSH]
- Fix dimmer on bug. [TheYOSH]
- Fix pulldown settings menu. [TheYOSH]
- Fix UTF-8 characters in Weather urls. Close [#77](https://github.com/theyosh/TerrariumPI/issues/77). [TheYOSH]
- Fix export timestamp. [TheYOSH]
- Fix webcam error logging. [TheYOSH]
- Fix file rights. [TheYOSH]

**Updates**
------
- Update changelog. [TheYOSH]
- Update installer. [TheYOSH]
- Update README.md. [TheYOSH]
- Update Dutch and English translations. [TheYOSH]
- Updated logging. [TheYOSH]
- Update version number. [TheYOSH]
- Update changelog. [TheYOSH]
- Refactored a lot code. Updated form processing. Added timers in the
  environment system based on [#47](https://github.com/theyosh/TerrariumPI/issues/47). Code cleanup by more re-using code.
  [TheYOSH]
- Update version number. [TheYOSH]
- Update English language. [TheYOSH]
- Major update. Rewritten and simplicated a lot of Pyton and JS code.
  Less caching issues when adding new sensors, switches etc. Better
  reuse of functions and repeating code. [TheYOSH]
- Update changelog. [TheYOSH]
- Update config code. [TheYOSH]
- Update configuration code and webcam part. [TheYOSH]
- Update Terrarium door code based on new switch code. [TheYOSH]
- Update changelog. [TheYOSH]
- Update CHANGELOG. [#72](https://github.com/theyosh/TerrariumPI/issues/72). [TheYOSH]
- Update language files. [#72](https://github.com/theyosh/TerrariumPI/issues/72). [TheYOSH]
- Update timer functionality. [#72](https://github.com/theyosh/TerrariumPI/issues/72). [TheYOSH]
- Next update for power switch timers. The timer functionality is
  implemented. Not very wel tested yet. [#72](https://github.com/theyosh/TerrariumPI/issues/72). [TheYOSH]
- Update Leaflet to version 1.3.1. [TheYOSH]
- Update submodules. [TheYOSH]
- Update weather icons. [TheYOSH]
- Update weather icons. [TheYOSH]
- Update README.md. [TheYOSH]
- Update expection logging. [TheYOSH]
- Update weahter skycons. [TheYOSH]
- Update weather skycons. [TheYOSH]
- Update exception logging. [TheYOSH]

**Other**
------
- Show dashboard graphs legend. [TheYOSH]
- Force heater and cooler of when lights are going on. [TheYOSH]
- Clear translation files. [TheYOSH]
- Better fields names for timer fields. [TheYOSH]
- Also show sensors when enabled in timer mode. [TheYOSH]
- Better logging and disable alarm for disabled environment parts.
  [TheYOSH]
- Also show sensors when enabled in timer mode. [TheYOSH]
- Calculate next day already. This will reduce the amount off loops when
  the period has ended. [TheYOSH]
- Merge branch 'master' of https://github.com/theyosh/TerrariumPI.
  [TheYOSH]
- Use localhost for PiGPIO connection. [TheYOSH]
- More yes are true :P. [TheYOSH]
- Removed disabled code. [TheYOSH]
- Refactor audio playlists. Refactor a bunch of Javascript. [TheYOSH]
- Merge pull request [#83](https://github.com/theyosh/TerrariumPI/issues/83) from theyosh/feature/switch_timers. [TheYOSH]

  Update changelog
- Cleanup weather html code. [TheYOSH]
- Merge branch 'master' into feature/switch_timers. [TheYOSH]
- Merge branch 'master' into feature/switch_timers. [TheYOSH]
- Finetine dimmer css. [TheYOSH]
- Fine tuning power switch css. [TheYOSH]
- Remove not used variable. [TheYOSH]
- Merge branch 'master' into feature/switch_timers. [TheYOSH]
- Merge branch 'master' of https://github.com/theyosh/TerrariumPI.
  [TheYOSH]


3.2.1 (2017-11-26)
------------------

**New**
------
- Add another check for failing weather data. [#52](https://github.com/theyosh/TerrariumPI/issues/52). [TheYOSH]
- Add extra check for weather data. [#52](https://github.com/theyosh/TerrariumPI/issues/52). [TheYOSH]
- Add publications. [TheYOSH]
- Add translations to audio files table and dropzone. [TheYOSH]

**Fixes**
------
- Fix utf-8 check for non string values. [#52](https://github.com/theyosh/TerrariumPI/issues/52). [TheYOSH]
- Fix door detection in sprayer engine. Fix [#59](https://github.com/theyosh/TerrariumPI/issues/59). [TheYOSH]
- Fix alarm warnings. [TheYOSH]
- Fixed environment averages. [TheYOSH]

**Updates**
------
- Update README.md. [TheYOSH]
- Update version. [TheYOSH]
- Update README.md. [TheYOSH]
- Update German translation. [TheYOSH]
- Update environment averages. [TheYOSH]
- Update Fancybox. [TheYOSH]
- Update German translation [#55](https://github.com/theyosh/TerrariumPI/issues/55). [TheYOSH]
- Update Dutch translation. [TheYOSH]
- Update English translation. [TheYOSH]

**Other**
------
- Support UTF-8 configuration values. [#52](https://github.com/theyosh/TerrariumPI/issues/52). [TheYOSH]
- Do not make environment parts depend on light part. [TheYOSH]
- Merge branch 'master' of https://github.com/theyosh/TerrariumPI.
  [TheYOSH]


3.2.0 (2017-11-24)
------------------

**New**
------
- Add TOC. [TheYOSH]
- Add config upgrade. [TheYOSH]
- Add files via upload. [TheYOSH]
- Add remote switches support. For now READONLY [#51](https://github.com/theyosh/TerrariumPI/issues/51). [TheYOSH]
- Add support for remote (HTTP/HTTPS) temperature and humidity sensors
  through JSON REST API. [#51](https://github.com/theyosh/TerrariumPI/issues/51). [TheYOSH]
- Add static url parser. [TheYOSH]
- Add CORS headers for Ajax REST calls. [TheYOSH]

**Fixes**
------
- Fix for remote data timeouts. [TheYOSH]
- Fix remote dimmer data collectin. [TheYOSH]
- Fix remote dimmer state updates. [TheYOSH]

**Updates**
------
- Update Dutch translation. [TheYOSH]
- Update changelog. [TheYOSH]
- Update README.md. [TheYOSH]
- Update README.md. [TheYOSH]
- Update language files. [TheYOSH]
- Update dashboard. Hide not enabled environment parts. [TheYOSH]
- Small player updates. [TheYOSH]
- Update soundcard code to support random soundcard order (2) [TheYOSH]
- Update soundcard code to support random soundcard order. [TheYOSH]
- Update readme. [TheYOSH]
- Update version number. [TheYOSH]

**Other**
------
- Merge pull request [#53](https://github.com/theyosh/TerrariumPI/issues/53) from theyosh/feature/remote_data. [TheYOSH]

  Feature/remote data
- Better load indicator. (2) [TheYOSH]
- Better load indicator. [TheYOSH]
- Merge branch 'master' into feature/remote_data. [TheYOSH]
- Merge branch 'master' into feature/remote_data. [TheYOSH]
- Code cleanup and add connection timeouts. [TheYOSH]


3.1.1 (2017-11-20)
------------------

**New**
------
- Add disabled door status. [TheYOSH]
- Add Apple icon. [TheYOSH]

**Updates**
------
- Update changelog. [TheYOSH]
- Updated top indicators. Hide disabled indicators on small screens.
  [TheYOSH]

**Other**
------
- Quotes. [TheYOSH]
- Code cleanup. [TheYOSH]
- Cleanup unused code. [TheYOSH]
- Cleanup HTML, Javascript and CSS code. [TheYOSH]


3.1.0 (2017-11-15)
------------------

**New**
------
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
------
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
- Final fix German language. Thanks [@vanessa2013.](https://github.com/vanessa2013.) [TheYOSH]
- Fix German translation. [TheYOSH]
- Fix water price calculation. [TheYOSH]
- Fix [#40](https://github.com/theyosh/TerrariumPI/issues/40). Keeping your iguana nicely warm. [TheYOSH]
- Fix [#36](https://github.com/theyosh/TerrariumPI/issues/36). [TheYOSH]

**Updates**
------
- Update changelog. [TheYOSH]
- Update changelog. [TheYOSH]
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
------
- Fucking Apple does not support javascript toLocaleString on iOS.
  Stupid! [TheYOSH]
- Merge pull request [#47](https://github.com/theyosh/TerrariumPI/issues/47) from theyosh/feature/audio_modules. [TheYOSH]

  Feature/audio modules. Fix [#42](https://github.com/theyosh/TerrariumPI/issues/42)
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
------
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
------
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
------
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
------
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
------
- Add sync command. [TheYOSH]

**Fixes**
------
- Fix wrong timers and updated German language. fix [#33](https://github.com/theyosh/TerrariumPI/issues/33). [TheYOSH]
- Fixed weather icons. [TheYOSH]
- Small HTML fixes. [TheYOSH]
- Fix HTML code in Dutch translation. Was broke in usage page. [TheYOSH]

**Updates**
------
- Update changelog. [TheYOSH]
- Update version number. [TheYOSH]
- Update README.md. [TheYOSH]
- Update README.md. [TheYOSH]
- Update install and update documentation. [TheYOSH]

**Other**
------
- Merge branch 'master' of https://github.com/theyosh/TerrariumPI.
  [TheYOSH]
- Refactor weather code to use inheritance. [TheYOSH]
- Merge branch 'master' of https://github.com/theyosh/TerrariumPI.
  [TheYOSH]
- Allow negative temperature settings. [TheYOSH]


2.8.1 (2017-09-30)
------------------

**New**
------
- Added a link in the Usage link to https://pinout.xyz to help end users
  that are not familiar with different pin numbering, updated and fixed
  some of the italian translation    modified:
  locales/it_IT/LC_MESSAGES/terrariumpi.mo    modified:
  locales/it_IT/LC_MESSAGES/terrariumpi.po    modified:
  locales/terrariumpi.pot. [Lorenzo Faleschini]

**Updates**
------
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
------
- Finished Dutch translation. [TheYOSH]
- Forced decimal number input by using input patterns. [TheYOSH]
- Merge pull request [#26](https://github.com/theyosh/TerrariumPI/issues/26) from penzoiders/master. [TheYOSH]

  updated translation and original strings to help user with GPIO pinout numbering


2.8 (2017-09-26)
----------------

**New**
------
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
------
- Update switch logging to add the old switch state in front of the new
  state. Should fix broken switch graphs. [TheYOSH]
- Fix translating sensor types. [TheYOSH]

**Updates**
------
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
------
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
------
- Added description back to working. Fix [#18](https://github.com/theyosh/TerrariumPI/issues/18). [TheYOSH]
- Add a new switch type GPIO-invert. Use it when normal GPIO is working
  in oppisite way. Fix [#20](https://github.com/theyosh/TerrariumPI/issues/20). [TheYOSH]

**Fixes**
------
- Fix webcam rotation. Settings was not saved at all :( . Fix [#19](https://github.com/theyosh/TerrariumPI/issues/19).
  [TheYOSH]
- Fixed saving new password. Added error feedback when saving is not
  successfull. And better password update check. Fix [#17](https://github.com/theyosh/TerrariumPI/issues/17). [TheYOSH]

**Updates**
------
- Update changelog. [TheYOSH]
- Update version number. [TheYOSH]
- Update translations files. [TheYOSH]


2.7 (2017-09-04)
----------------

**Fixes**
------
- Better warning message when sensor measured values are outside given
  ranges. Fix [#16](https://github.com/theyosh/TerrariumPI/issues/16). [TheYOSH]
- Fix switch callback functions. Refs [#15](https://github.com/theyosh/TerrariumPI/issues/15). [TheYOSH]
- Fix adding new temperature sensors. Refs [#15](https://github.com/theyosh/TerrariumPI/issues/15). [TheYOSH]
- Fixed bug found in [#13](https://github.com/theyosh/TerrariumPI/issues/13). Only calculate hours when lights are enabled.
  [TheYOSH]

**Updates**
------
- Update changelog. [TheYOSH]
- Update readme. [TheYOSH]
- Update gentelella. [TheYOSH]
- Update hardware text. [TheYOSH]
- Update translation. Dutch at 75% [TheYOSH]

**Other**
------
- Support OpenWeatherMap.org. [TheYOSH]
- Disable extra door and switch logging. [TheYOSH]
- Support up to 8 ports on USB relay switch. [TheYOSH]


2.6 (2017-08-06)
----------------

**New**
------
- Add profile page reloading after changing profile image. [TheYOSH]
- Add Animal Profile option. [TheYOSH]
- Add robots.txt. [TheYOSH]

**Fixes**
------
- Small fix. [TheYOSH]
- Fix missing variable in template. [TheYOSH]
- Fix 404 error in template rendering. [TheYOSH]

**Updates**
------
- Update changelog. [TheYOSH]
- Update changelog. [TheYOSH]
- Update changelog. [TheYOSH]
- Update translations. [TheYOSH]

**Other**
------
- Merge pull request [#12](https://github.com/theyosh/TerrariumPI/issues/12) from theyosh/feature/profile. [TheYOSH]

  Feature/profile
- Changed profile image uploading. [TheYOSH]
- Moved profile page to main menu. [TheYOSH]
- Remove debug. [TheYOSH]


2.5 (2017-07-28)
----------------

**New**
------
- Add fancybox. [TheYOSH]
- Added documentation v0.1. [TheYOSH]
- Add IPv6 support. [TheYOSH]

**Fixes**
------
- Fixed weather usage documentation. [TheYOSH]
- Fix issue [#9](https://github.com/theyosh/TerrariumPI/issues/9). Typo in function call. And extra fix for indicator on
  the weather page. Close [#9](https://github.com/theyosh/TerrariumPI/issues/9). [TheYOSH]

**Updates**
------
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
------
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
------
- Add caching headers for API calls - Now in UTC. [TheYOSH]
- Add caching headers for API calls. [TheYOSH]

**Fixes**
------
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
------
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
------
- Remove debug. [TheYOSH]
- Remove JS debug. [TheYOSH]
- Remove sunset and sunsrising shifting. [TheYOSH]
- More proper English. [TheYOSH]
- Refactor code to use proper English terms. Will require the renew the
  environment settings. [TheYOSH]


2.4.2 (2017-07-16)
------------------

**New**
------
- Add version checker. [TheYOSH]
- Add hardware documentation. [TheYOSH]
- Add switch GPIO errors to logfile. [TheYOSH]

**Fixes**
------
- Fix webcam warmup time variable. [TheYOSH]
- Helpsections are by default closed now. Fixed multiple clicks loaded.
  [TheYOSH]
- Fixed adding sensors and switches to the system. [TheYOSH]
- Fix door status overview page. [TheYOSH]

**Updates**
------
- Update changelog. [TheYOSH]
- Update version number. [TheYOSH]
- Update language. [TheYOSH]
- Update information page. [TheYOSH]
- Updated required fields. [TheYOSH]
- Update weather logging. [TheYOSH]
- Update OWFS port setting. Now OWFS can be disabled by setting the OWFS
  port to 0. [TheYOSH]

**Other**
------
- Removed software page. [TheYOSH]
- Remove empty lines. [TheYOSH]


2.4.1 (2017-07-15)
------------------

**New**
------
- Add js script for translations. [TheYOSH]
- Added git checkout for Gentelella bootstrap 3 template if missing.
  [TheYOSH]
- Add better empty switches/sensors loading. [TheYOSH]
- Added heater and cooler timers fields. [TheYOSH]
- Added style code to hide rows when loading. [TheYOSH]
- Add some debugging. [TheYOSH]
- Add chaching header. Disabled webserver debug output. [TheYOSH]

**Fixes**
------
- Fix translations. [TheYOSH]
- Fix dashboard environment. [TheYOSH]
- Fix environment. [TheYOSH]
- Fix spelling typos. [TheYOSH]

**Updates**
------
- Update changelog. [TheYOSH]
- Update US language. [TheYOSH]
- Updated system form fields. [TheYOSH]
- Update translations form fields. [TheYOSH]

**Other**
------
- Bla. [TheYOSH]
- Rewritten environment code. Reduces a lot of code. [TheYOSH]
- Small changes. [TheYOSH]
- Remove w1 support for switches. [TheYOSH]
- Debug cleanup. [TheYOSH]
- Smaller image. [TheYOSH]


2.4 (2017-07-14)
----------------

**New**
------
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
- Added some extra info. [TheYOSH]
- Add database recovery and update switch usage data after swithing off.
  [TheYOSH]
- Added duration information in total water and power usage. [TheYOSH]
- Added translation code. 90% off the interface can now be translated.
  [TheYOSH]
- Add languages nl_NL and en_US. [TheYOSH]
- Added day,week,month and year periods to the history graphs. [TheYOSH]
- Added logging to disc (part 1) [TheYOSH]
- Added calendar icons for graph periods. Not working yet. [TheYOSH]
- Added offline detection and dynamic reloading new webcams when adding.
  [TheYOSH]
- Added system stats auto refresh and graph Y axis formatter. [TheYOSH]
- Added support for authentication when changing settings. [TheYOSH]
- Added option to reconfigure the door sensor GPIO pin. [TheYOSH]
- Added USB webcam support. [TheYOSH]
- Added support for TLS websockets. [TheYOSH]
- Added submodule gentelella. [TheYOSH]
- Added some documentation. [TheYOSH]
- Added system pages. Refortmat HTML en JS code. Cleanup debug code.
  Rewritten history data retrieval. [TheYOSH]
- Added webcam support. Refactored history data and code. Moved JS code.
  Finetuned different parts. [TheYOSH]
- Added needed empty folders. [TheYOSH]
- Added submodules. [TheYOSH]
- Added some more information and a screenshot. [TheYOSH]
- Added link to github page. [TheYOSH]

**Fixes**
------
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
- Fix door pin exception. [TheYOSH]
- Fix for running without any switchboard. [TheYOSH]
- Fix duration calculation when timer is used. [TheYOSH]
- Fix for initial language with default config. [TheYOSH]
- Fix install script. Added extra dependencies. [TheYOSH]
- Fix for total power and water usage. [TheYOSH]
- Fix generating 404 error pages. [TheYOSH]
- Optimized database. Optimized total power and water usage calculation.
  Fixed gauge reloading. [TheYOSH]
- Last small fixes and cleanups. [TheYOSH]
- HTML code cleanup. Better translations. Better caching of webdata.
  Cleaner CSS code. Fixed progress loader on page. [TheYOSH]
- Fixed graph caching bug final. [TheYOSH]
- Fixed graph caching bug. [TheYOSH]
- Install fix for granting rights to the USB FTDI device. [TheYOSH]
- Removed debug code and fixed javascript form processing. [TheYOSH]
- Fixed door messages indicator. Changed graph tick size. Removed socket
  switch toggle. [TheYOSH]
- Fixed total water and power usage calculation. [TheYOSH]
- Fixed graph tickers. Home menu is now active from start. [TheYOSH]
- Fixed empty settings startup and reloading switches after
  reconfiguring. [TheYOSH]
- Fixed dashboard environment indicators. [TheYOSH]
- Pretify graphs. Fixed authentication. [TheYOSH]
- Fixed error switch callback during boot. Fixed collector. [TheYOSH]
- Rewritten data collector and fixed average data calculation. [TheYOSH]
- Fixed starting the system with empty settings. [TheYOSH]
- Fixed door sensor. [TheYOSH]
- Fixed lost sockets. [TheYOSH]
- Fixed crashing threads with RPi.GPIO events. [TheYOSH]
- Fixed form processing when editing settings. [TheYOSH]
- Fix growing scrollbar. [TheYOSH]
- Small JS fixes. [TheYOSH]
- Fixed HTML and JS code layout. [TheYOSH]
- Remove unused modules, fixed heater trigger, added total power and
  waterflow. [TheYOSH]
- Fixed updating weather source. [TheYOSH]
- Fixed clean up command in installer. [TheYOSH]
- Fixed bottle submodule. [TheYOSH]
- Updated temperature indicator. Fixed weather graph title. Fixed value
  in graph tooltip. [TheYOSH]
- Removed some debug code and old comments. Fixed graph timing for
  wattage usage. [TheYOSH]

**Updates**
------
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
- Updated to latest Gentelella template. [TheYOSH]
- Update language. [TheYOSH]
- Updated webcam object. Added extra retries before giving up and put
  webcam offline. [TheYOSH]
- Update system defaults. [TheYOSH]
- Upgraded Leaflet to version 1.0.3. [TheYOSH]
- Update languages. [TheYOSH]
- Updated reloading of webcams. [TheYOSH]
- Updated language file generation. [TheYOSH]
- Updated languages. [TheYOSH]
- Updated installation script to enable TerrariumPI auto start at boot
  time. [TheYOSH]
- Update to leaflet 1.0.2. [TheYOSH]
- Update to master of gentelella. [TheYOSH]
- Updated the graphs drawing. Now it is more modular and easier to
  extend with other periods. [TheYOSH]
- Update gitignore to ingore all logfiles. [TheYOSH]
- Updated total power usage. Bug. [TheYOSH]
- Renamed internal plugin function. Always update dashoard with socket
  (re)connect. [TheYOSH]
- Update default GPIO pin to BOARD modus. [TheYOSH]
- Latest update version 1. [TheYOSH]
- Update external libraries - cleanup. [TheYOSH]
- Update external libraries. [TheYOSH]
- Update copyright date. [TheYOSH]
- Update external libs. [TheYOSH]
- Updated jQuery library. [TheYOSH]
- Updated external libraries. [TheYOSH]
- Update submodules. [TheYOSH]
- Updated submodules. [TheYOSH]
- Updated external libraries. [TheYOSH]
- Updated submodules. [TheYOSH]
- Updated readme - install. [TheYOSH]
- Updated startup script for more stability. [TheYOSH]
- Update submodule. [TheYOSH]
- Updated submodules. [TheYOSH]

**Other**
------
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
- Disabled caching for html files. Does not work with translated pages.
  [TheYOSH]
- Removed disabled code. [TheYOSH]
- Merge branch 'master' of https://github.com/theyosh/TerrariumPI.
  [TheYOSH]
- Cleanup terrarium collector code and added logging. [TheYOSH]
- Print to console that server is running. [TheYOSH]
- Changed settings order. [TheYOSH]
- Better user detection in startup. [TheYOSH]
- Check if server is started as user root and better logging. [TheYOSH]
- Some HTML cleanup and re-enabled webcams. [TheYOSH]
- Splitted web access requests to own logfile. [TheYOSH]
- Changed default logging. [TheYOSH]
- Rewritten data logging (again). [TheYOSH]
- Trying to use modulo for graph data. Not stable yet. [TheYOSH]
- Removed debug. [TheYOSH]
- Release the SQL database earlier for better performance. [TheYOSH]
- Smaller dropdown menu for settings in graphs. [TheYOSH]
- Make toggling switches through GET requests with authentication.
  [TheYOSH]
- Use systemtime and added day and night indicator. [TheYOSH]
- Changed loading dashboard. Speed up first time loading. [TheYOSH]
- Merge branch 'master' of https://github.com/theyosh/TerrariumPI.
  [TheYOSH]
- Remove wrong mask image. [TheYOSH]
- Only spray when door closed. Easier check if sensors or switches does
  exists. [TheYOSH]
- Only post form fields that are visible. [TheYOSH]
- Merge branch 'master' of https://github.com/theyosh/TerrariumPI.
  [TheYOSH]
- Make install script executable. [TheYOSH]
- Reverd code for form parsing... ID fields are also hidden :( [TheYOSH]
- Removed old submodules references. [TheYOSH]
- Merge branch 'master' into v2. [TheYOSH]
- Moved from v1 to v2. [TheYOSH]
- Moved from v1 to v2. [TheYOSH]
- Cleanup footer. [TheYOSH]
- Ignore db journal files. [TheYOSH]
- Removed local copy of gentelella and use github version. [TheYOSH]
- Initial commit version 2.0. [TheYOSH]
- Removed old jqwidgets library. [TheYOSH]
- Removed wrong module include. [TheYOSH]
- Removed RPI Webcam installer to separate installer. [TheYOSH]
- Removed debug. [TheYOSH]
- Support txt files. [TheYOSH]
- Extra cleanup. [TheYOSH]
- Reformatted javascript and css code. [TheYOSH]
- Living on the edge.... use latest beta of Leaflet. [TheYOSH]
- Initial release. [TheYOSH]
- Initial commit. [TheYOSH]
