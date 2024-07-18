---
title: 🎉 10 Year Anniversary 🥳
date: 2024-08-01 00:00:00 +0000
categories: [Website, News]
tags: [anniversary, 10-year]
pin: true

image:
  path: /assets/img/10-year-party-ballons.webp
  src: /assets/img/10-year-party-ballons.webp
  alt: 10 year anniversary header image
---

![10 year anniversary](/assets/img/10-year-party-ballons.webp){: .left width="150" }It has ben 10 years now when this project started. It started all to learn a new programming language Python, and as a lazy programmer does, to automate stuff.

![Raspberry PI Logo](/assets/img/RaspberryPI_Logo.webp){: .right width="150" }And the [Raspberry PI](https://en.wikipedia.org/wiki/Raspberry_Pi) was about 2 years old, and that gave me the idea to combine the three things. Automate my terrarium with a Raspberry PI and Python code.

![8 years old Gecko chilling](/assets/img/Chilling_Gecko_age_8_years.webp){: .left width="150" }I had my [Madagascar day gecko](https://en.wikipedia.org/wiki/Phelsuma_grandis) already for 4 years and I got a bit vet up with daily water spraying, and changing the timers to make some kind of seasons with longer and shorter daylight. So the idea of making my own controlling software for controlling the relays based on time or sensors. And would make sure that the humidity is always at the correct value.

> **TerrariumPI was born!**

## Basic setup

It started back in 2013 with the idea to automate my terrarium as it is getting annoying to spray every day. As the lights where already done by a simple timer. And with the new Raspberry PI this project was born.

![1 Wire bus](/assets/img/1-WireLong.webp){: .right width="150" }So I added some [DS18B20]({% link _hardware/1-wire_sensor.md %}#ds18b20) temperature sensors to the PI using [1-Wire](https://pinout.xyz/pinout/1_wire). And found some 1-wire humidity sensors that could be used on the same GPIO pins. So I got temperature and humidity readout. This was pretty cool, as you can hook up 255 sensors on the 1-wire bus. So plenty of room left for more sensors. I used a few temperature sensors and a single humidity sensor.

And a cool feature of the 1-wire system is that it does not require any setup. You can just scan the 1-wire bus, and use all sensors that are available.

The next actions was to toggle relays. So I started with [basic relays]({% link _hardware/ftdi_relay.md %}). And hooked up some lights to it. Later on, a small heat mat. And those relays where connected through USB. Because that was easier then using GPIO pins.

And all was made in [Python](https://www.python.org/) in order to learn a new language. Using INI like config files for configuration.

After a while I added 'realtime' weather information through 3rd party APIs. And the webcam was already supported by making a JPEG image every X seconds. No live streaming, but almost 'live' image.

![TerrariumPI Version 0.3 August 2014](/assets/img/TerrariumPI_v0.3_2014-08-28.webp)
_TerrariumPI Version 0.3 August 2014_

## Early version

So when the basic setup was running, it would be nice to have at least a nice status web page which give the current state. As I was making websites since 1998, it should be possible to make a web gui. But one thing I cannot do... is making a design. As you can see above. :point_up: :smiley:

This is still a simple version with only temperature and humidity sensor support.

And this version already supported magnetic sensors so you can make door sensors. This was a nice feature, because now you are sure the terrarium doors are closed. And I added some nice logic that the sprayer should never toggle on when the door is open. This way, your house will not get wet when the door is not closed well. And you will stay dry when working in the terrarium. :grinning:

## Code on Github

![GitHub Logo](/assets/img/GitHub-Logo.webp){: .right .invert width="150" }In order to keep the code save and backup-ed, I started to put the code on Github in [january 2016](https://github.com/theyosh/TerrariumPI/commit/2ca75beac3adb1a50107412442c9427fa1ea4ebf). Also I needed to learn a bit more about git and using branches, code fixes and creating new features. So again, original goal was to learn more about working with git.

At this point, we are at version 0.9.

And after that, I just start committing new code. Never thought that the code would ever be used by somebody else...

In 2020 it was archived by Github for the [Arctic Code Vault](https://archiveprogram.github.com/arctic-vault/) project.

## First issues and requests

It took more than 1 year, but there it was. The [first issue](https://github.com/theyosh/TerrariumPI/issues/1). I was bit stunned, because somebody was using this software. Never thought this would happen. :smiley:

This resulted in the first requests for new hardware. And that forced me to think about a more plug-able system where you can easy add new hardware. As a relay has always the same functions, you only have to create code for the actual low level control. Logic should not depend on a single relay.

And that was the first feature request in july 2017. It took more than a year, but never knowing that the issue counter will reach **900+** [issues](https://github.com/theyosh/TerrariumPI/issues) after 10 years.

## Publications

![Hack a Day publication](/assets/img/publications/Pubication_Hackaday-TerrariumPI-21-11-2017.webp){: .right width="150" }In the end of 2017 [some magazines made a publication](/TerrariumPI/tags/publication/) about TerrariumPI. Again, I did not expect this, nor I was aware of it. Only [Hack a Day]({% link _posts/2017-11-21-hack_a_day.md %}) send me a nice email warning that the GUI could be a bit busier as they where about the publish a story about TerrariumPI. It was very nice of them to give a heads up. :thumbsup:

But it had some impact, as the new requests and first bugs are getting in through new issues.

And the GUI just kept running. :wink:

## New hardware

![Hardware overview](https://raw.githubusercontent.com/theyosh/TerrariumPI/3.4.2/static/images/documentation/hardware_overview.jpg)
_Hardware overview when started back in 2014_

So, it started with just a few sensors and relays, and now it has support for:

- 32 types of relays
- 37 types of sensors
- 5 types buttons
- 9 types of webcams

Which most of them I do not even own.

From version [TerrariumPI 3.0](https://github.com/theyosh/TerrariumPI/releases/tag/3.0.0) there is power dimmer support, which made it possible to mimic sunrise and sunset actions. You could now turn a light of in 30 minutes. Which means every 18 seconds the light went up by 1%. Which was really a very nice new feature.

But after a few years, more and more hardware was requested by other people. And by adding support for those requests, my software grow. This is a nice thing, as more and more people can use it. But supporting more and more hardware, cost my time. So I thought, there should be a kind of 'payment' for supporting new hardware. So I asked pictures of running setups in return. And that made a rather big issue with a [lot of pictures](https://github.com/theyosh/TerrariumPI/issues/210). It is just nice to look at to get some inspiration.

![Hardware overview](/assets/img/hardware_testing_2024.webp)
_Hardware overview in 2024_

And as far as I know, I was able to support 90% of the requests for new hardware. Which I think is pretty neat.

### Lesson learned

A lot of hardware support has been added. And during those years I learned that you always have to by more hardware than needed. Because hardware will always break down in a weekend. Or the hardware is not available anymore as it was to old.
Therefore my advise is always:

> Buy at least 1 backup device when you order new hardware
> {: .prompt-tip }

### Raspberry PI versions

![Raspberry PI 1 Model B+](/assets/img/raspberry_pi_1b.webp){: .right width="150" }During those 10 years, we have had 5 Raspberry PI versions and 2 Pi Zero versions. Which we try to support all. And this is succeeded for about 80%.

The first Raspberry PI is probably not supported anymore. But as long as you can install Raspbian Lite OS, you should be able to run TerrariumPI. The new Raspberry PI 5 is not yet fully supported. There is a hardware change in chips and not all used libraries are updated to support that.

![Raspberry PI 3 Model B+](/assets/img/pi3specs.jpg){: .left width="150" }
And the software can be pretty CPU intensive, I never thought it possible to run on a Raspberry Pi Zero. But it does. It depends on what kind of hardware you use with it. Network connected hardware is easier to process, than physical connected devices. USB and GPIO connected devices needs CPU time to operate. And that means more CPU usage. But I got some reports that a Raspberry PI Zero is working. So that is also pretty cool.

## Code migrations

![Python Logo](/assets/img/python-logo.webp){: .right width="150" }And during those 10 years, code evolves. TerrariumPI got new features, and support more and more hardware, which lead to use more external libraries. And not all those libraries are maintained actively. Which give some headaches about upgrading TerrariumPI.

The first big hurdle was the migration from [Python 2.7 to Python 3.5](https://github.com/theyosh/TerrariumPI/releases/tag/3.9.0). Which means making code that works on both Python versions. But also needed to find libraries that work on both Python versions. This was a 2 year struggle. But we managed. And we dropped Python 2.7 support with TerrariumPI version 3.0.

After that, it was keeping up with the Python versions. From 3.5 to 3.7 was not a big problem. But now you see that old libraries are getting behind. And this is for now not breaking, but it will be in the future. We will see how this goes.

### 'Blind' coding

Some times there was a request for hardware that I did not own, or able to by. So then we did some extreme programming. I made some code and pushed to Github. The requester is than downloading the new code and test it. With screenshots of the errors and with some answers on questions I could make the next step. This could take some evenings, but it always worked! And it was always a nice happening when it worked. I made code without being able to test. And still made it work! :raised_hands:

### Remote coding

Or some times, it was possible to get remote access to the Raspberry PI. And than it was easy to create new code to support new hardware. But here I was really amazed that people trusted me on their Raspberry PI in their home network. But I never abused it! And it helped a lot.

## Gui upgrades

![jQuery Logo](/assets/img/jquery-logo.webp){: .left width="150" }As you have already seen, the GUI has made a few transitions in those 10 years. We are now running for 2+ years with [Svelte](https://svelte.dev). Which is a nice Javascript reactive framework. It was easier to learn than Vue.js or React.js. \
But it did not start that way.

The first GUI was made with custom HTML and a lot of jQuery. To let it look like a Single Page Application. Because that was booming 10 years ago. Now it is pretty normal.

But I am not a GUI developer so it looked not that good, and it has a very high "[My First Sony](https://www.youtube.com/watch?v=n68TnOyoeU0)" look. Bulky and colorful. As you can see in the first screenshot on this page.

Then I found [Gentelella admin template](https://colorlib.com/polygon/gentelella/) which gave it a bit more professional look. This has been the gui for more than 3 years. It did upgrade the look from time to time. But it was a nice admin gui which I could use for TerrariumPI. It saved a lot of CSS hassling.

![TerrariumPI Version 2.5 July 2017](/assets/img/TerrariumPI_2.5_2017.webp)
_TerrariumPI Version 2.5 July 2017_

A vew years later I found [AdminLTE](https://adminlte.io/themes/v3/). A more up to date GUI with the same functionality as Gentelella. But it looked a bit fresher. So we shifted to AdminLTE about 4 years ago. But still it was a lot of jQuery and a lot of vanilla java scripting.

![Svelte Logo](/assets/img/SvelteLogo.png){: .right width="150" }This could done better, and than I found [Svelte](https://svelte.dev). Which looked nice to work with. And it was pretty easy to learn. And the best thing is that I could drop a lot of custom/vanilla javascript that used jQuery. With svelte, you just program in a single file you CSS, JavaScript and HTML code. And the javascript code will be compiled and optimized during building the GUI. This produced the fasted GUI at the moment.

![TerrariumPI Version 4.10.1 July 2024](/assets/img/TerrariumPI_4.10.1_2024.webp)
_TerrariumPI Version 4.10.1 July 2024_

## Stability

When I started the automate my terrarium, a question that popped up pretty quickly was:

> **How long will the hardware last?**

I was using a wet based terrarium. The humidity is always above 60%. And electronics and water do not work that well together. So I looked for some water resistant sensors which could handle some moist air. For temperature sensors, there are shielded DS18B20 sensors, which can even be submerged in water. For humidity I just picked some hardware and placed it in an enclosed box with some holes in it. So direct water could hardly get in, but the humid air will, and can be measured.

But also, how long with the Raspberry PI stay working? How long with the SD card stay alive? All kind of questions of which there is basically one way of find out. Just by starting and see how long it all lasts...

### Hardware

For the hardware part, I am pretty amazed how long it will last. My temperature and humidity senors are now working for more than 7 years in the current terrarium. And they do not show any problems. I am so crossing my fingers (:crossed_fingers:) that is stays that way. Because I cannot change them :smile:. They are all placed in hidden spots, so you cannot see the sensors unless you know where they are. But also hard to replace when needed. \
Until now, only one sensor has been broken. Lucky we can (ignore sensors)[], and TerrariumPI will just keep running.

But also the relays I use, are now 10+ years old. I still use the first relay board I bought when I started TerrariumPI. And it still working like a charm. Heavily covered under dust, but still going strong.

![CD Card](/assets/img/sd-card.webp){: .right width="150" }My SD card is now at least 4 years old. And maybe older, as the last time the SD card is formatted begin 2020. And this is something which I did not expected. I was afraid that the SD card will not last that long. Because TerrariumPI is writing a lot to the SD card. Every 30 seconds there will be database updates with new sensor data. And it does log a lot of information while running. But this logging has been moved to memory based storage, and once a night a copy will be zipped and stored on the SD card. So 24 hours logging only result in a few seconds of writing to the SD card. This was a pretty nice feature and I guess it does help to keep the SD card alive.

And the Raspberry PI is a Raspberry Pi 3 Model B which I bought in begin 2017. Which is also running now for more than 7 years! You can find some [build pictures here](#build-pictures-2017). It needs some extra cooling, as it is lying on top of my terrarium between the heating and UV lights. But still with version 4.9.0 the CPU usage is reduced by 35%. So my old Raspberry PI can still keep up!

![TerrariumPI CPU year graph](/assets/img/munin-cpu-load.webp)

### Uptime

![Uptime image](/assets/img/uptime.webp){: .left width="150" }For this kind of software reliability and uptime is key. Because the goal is to make our lives easier, and that of the animal optimal. So the software is written in a way, that it can handle a lot of instable hardware. A single failure will not crash the software. It will send out warnings, but it should keep working.

Now is the uptime a bit cheated here, because we ues the OS uptime. So if you restart TerrariumPI software itself, it will not reset the uptime. But than again, how often do you restart TerrariumPI. It should only be done with an upgrade, or when everything goes wrong. Other than that, no restart is needed, and the OS uptime is easier to use. The only restarts that could happen is when there are new kernel updates which always needs a restart of the OS.

So in October 2022 [@jornobe](https://github.com/jornobe) mentioned [almost 4 months of uptime](https://github.com/theyosh/TerrariumPI/discussions/741). Which was cool to see. And at November 2023 I reached an uptime of 6 months. Yeah! I call this pretty stable!

**All with all, I would say, TerrariumPI is pretty stable. Maybe we can call it "rock solid"!**

## Database struggles

![SQLite Logo](/assets/img/SQLite-Logo.webp){: .left width="150" }With the years, the database with sensor and relay history will grow. And that gave some problems in the past 10 years. I just have tackled a new database problem this year.

It started just to saving historical sensor data for showing nice graphs on the dashboard. Never calculated how much data that would be. So here is a quick math.

We update every 30 seconds, which will result in new data. But here already, we only store the sensor data once a minute. So effectively we have 1 data entry per minute per sensor in the database:

- 24 \* 60 = 1440 entries per day
- 7 \* 1440 = 10080 entries per week
- 30 \* 1440 = 43200 entries per month
- 12 \* 43200 = 518400 entries per year

So that is more than **half a million** entries a year per sensor[^footnote_total_records] :stuck_out_tongue_winking_eye: An average record looks like this:

`e4ab8fe88aee2b16c749c4f1c38d4a6d|2023-03-10 14:22:00.000000|804.0|0.0|1500.0|300.0|1200.0|0`

![Graph up](/assets/img/graph-up.webp){: .right width="150" }And lets say it takes about 90 bytes to store a record. So 90 \* 518400 = 46656000 bytes, roughly 47MB per year per sensor. I use about 30 sensors, so that will take about 1400MB or 1,4GB a year! Which also means 155.520.00 records in the database. That is **150 million** records. As you can see this is not just a few records... \
Maybe I had to do some calculation up front :rofl:

So we created a [clean up script](https://github.com/theyosh/TerrariumPI/blob/main/contrib/db_cleanup.py), which will delete all data older than 60 weeks. As the graphs can only show data for maximal 1 year. So sensor data older than 60 week can safely be removed. But this has to be done manually. It will takes at least an hour to do.

### Relay data

This also made the logging for relays change a bit. Storing every minute that a relay is on, is not handy. So for relays we only write to the database when the relay changes state. And at least once an hour. This to make the graphs easier to make. But relay data will NOT be cleaned, as we want to be able to calculate the total power and water usage.

But again, after many years of data, the total power and water usage calculation took about 15 seconds. This is just due to the amount of data. We could optimize this by storing calculated totals per year or per month. But that was a bit more work to fix, than the final solution. And the real problem was that these totals where calculated every time a relay changed, or at the end of every 30 seconds run. \
But this is not smart, as the totals only change when the relay goes off. Than we know the last powered on period, and can we calculate new power and water totals. Together with a caching mechanism, this data will only updated when a relay goes off, or once an hour at maximum. This was a big CPU saver, as we can see in the graph above with the CPU usage drop.

![Total power and water usage info boxes](/assets/img/Totals_power_water.webp)
_Total power and water usage info boxes_

All this data will result in a **2.1GB** SQLite database to work with. And this proves that SQLite is pretty fast on low level hardware.

## Documentation

![Jekyll Logo](/assets/img/Jekyll-logo-vector-01.webp){: .right width="150" }
As every developer knowns, documentation is always something we do afterwards. Which results in not doing at all. And this was no different. But after a few years, I had to answer the same questions over and over. So documentation is needed.

First it was inside the web GUI, but that means, that you need to install the software, before you can read all the options and what it can do. So that did not work. Also, I wanted to be able to update the documentation without releasing a new version.

So for version 3.X we made a [Github Wiki](https://github.com/theyosh/TerrariumPI/wiki). Where the image on the right is still a live image from my running terrarium. So after working out the most documentation, I was not happy with the look, and how to edit. So that meant, we have to look to something else.

![Chirpy Jekyll Template Logo](/assets/img/ChirpyTemplate.webp){: .left width="75" }It should run on Github pages, which made it easier to host. Also, for a documentation website, there should no need for a dynamic backend. So after look around, we found Jekyll for building the HTML side. And, again, we needed a template. This time I found Chirpy Template. Which was pretty nice, had some nice extra features.

And this made is also possible to update just the documentation, build a new version with Github actions, and the new documentation is deployed. And now almost everything should be documented. And the content is all in text files, so a migration in the future is still possible.

## Different languages

At the moment TerrariumPI is translated to 14 languages. Again, this is something I could not do without other people that are using TerrariumPI. And this is now nicely done with [Weblate](https://weblate.org/). An online translation tool, that you can use for free when you host it yourself.

[![Translation status](https://weblate.theyosh.nl/widgets/terrariumpi/-/multi-auto.svg)](https://weblate.theyosh.nl/engage/terrariumpi/)

In the beginning translations where added by pull requests after changing .PO and .MO files. But this was a bit difficult for less technical people. And not all TerrariumPI users are tech people.

So we needed something else. And we found [Weblate](https://weblate.org/). A nice web based tool, which does not need any technical knowledge. Only English for reading source language. All translations will automatically added to the code after 24 hours. As I am not able to validate translations as I can't read them, they are automatically approved. :innocent:

## Contributors

And here is a list of persons that added some code or translations to TerrariumPI. Of which I am very thank full.

![GitHub Contributors Image](https://contrib.rocks/image?repo=theyosh/TerrariumPI)

## 10 years later

And now, 10 years later, the software is running stable and reliable. Which was the goal in the beginning. It took some more years, and a lot of extra features, but we made it. **10 years old! !! PAAARTEEEEYYY !!**

<div style="width:100%;height:0;padding-bottom:56%;position:relative;"><iframe src="https://giphy.com/embed/ZJB5EPInvETQY" width="100%" height="100%" style="position:absolute" frameBorder="0" class="giphy-embed" allowFullScreen></iframe></div><p><a href="https://giphy.com/gifs/disco-ZJB5EPInvETQY">via GIPHY</a></p>

## Historical pictures

{% include image-gallery.html folder="/assets/img/photos" %}

[^footnote_total_records]: This is all theoretical. There could be sensor data missing due to errors.
