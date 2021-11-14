---
title: Install
icon: fas fa-tools
order: 4

image:
  src: /assets/img/Installation.webp
  alt: Installation header image
---

Here we will install Raspberry PI and TerrariumPI software step by step.

# Raspberry PI

![Raspberry PI Logo](/assets/img/RaspberryPI_Logo.webp){: .right width="100" }
In order to run TerrariumPI you first need a working Raspberry PI with the '[Raspberry Pi OS Lite](https://www.raspberrypi.org/software/operating-systems/)' image. This is very important, as the Desktop version will not work well with the GPIO pins.

Also 64bit is not supported due to missing mmal code which is needed for the webcams.

## Creating SD Card

![Raspberry PI Imager](/assets/img/RPI_Imager.webp){: .right width="200" }
Download and instal the [Raspberry Pi Imager](https://www.raspberrypi.org/software/) to prepare your SD card. Make sure you have a SD card of at least 4GB of size. Bigger is better :)

When the SD card is written, you can read/write the 'boot' partition. Add a file called 'ssh' to it. This will [enable SSH on a headless Raspberry Pi (add file to SD card on another machine)](https://www.raspberrypi.org/documentation/remote-access/ssh/).

And if you want to use WiFi also add a small file called `wpa_supplicant.conf` in the 'boot' partition. The contents of the file should be something like this:
```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=[Your 2 letter country code]

network={
        ssid="[Your WiFi Name]"
        psk="[Your WiFi password]"
}
```
And that should make your Raspberry PI connect to the WiFi network first time it boots.

Put your SD card in the Pi and power it up.

# TerrariumPI

When the Raspberry PI is up and running, you should be able to SSH to it. On Linux and Mac you can use the terminal. For Windows, you can use Putty.

```console
ssh pi@[raspberrypi]
```

## Docker
As from version 4.1 there is a Docker image that can be used to run TerrariumPI. When you run it in Docker, you can skip the rest of the page. Only the migration could be followed if you want to restore your current relay history.

Install docker according to: [https://pimylifeup.com/raspberry-pi-docker/](https://pimylifeup.com/raspberry-pi-docker/)

Then you need to setup a `docker-compose.yaml` file. There is an example `docker-compose.yaml.example` which can be used as a starting point:

```yaml
version: "3.3"
services:
  terrariumpi:
    image: theyosh/terrariumpi:4.1.0
    volumes:
      - /opt/terrariumpi/logs:/TerrariumPI/log
      - /opt/terrariumpi/data:/TerrariumPI/data
      - /opt/terrariumpi/media:/TerrariumPI/media
      - /opt/terrariumpi/webcam-archive:/TerrariumPI/webcam/archive
      - /opt/terrariumpi/DenkoviRelayCommandLineTool:/TerrariumPI/3rdparty/DenkoviRelayCommandLineTool
      - /boot/config.txt:/boot/config.txt
      - /boot/cmdline.txt:/boot/cmdline.txt
      - /etc/modules:/etc/modules
      - /opt/vc/bin:/opt/vc/bin
      - /dev:/dev
    network_mode: host
    restart: always
    privileged: true
    environment:
      TZ: "Europe/Amsterdam" # timezone list can be found here https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
      ENABLE_I2C: "true"
      ENABLE_1_WIRE: "true"
      ENABLE_CAMERA: "true"
      ENABLE_SERIAL: "true"
      ENABLE_CO2_SENSORS: "true"
      AUTO_REBOOT: "true"
```
The only real setting is the `TZ` value. Make sure it is set to your local/home time zone. [A valid list can be found here](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones).


We run the container with **[privileged](https://docs.docker.com/engine/reference/run/#runtime-privilege-and-linux-capabilities)** enabled. This is less secure, but needed in order to be able to handle all the hardware that is connected to the Raspberry PI.

then you can run `docker-compose up -d` to start the docker image. It could be that it needs a reboot. After that, you should be able to access TerrariumPI on the url `http://[raspberrypi]:8090`. [Continue with the setup]({% link _tabs/setup.md %})

## Prerequisites

First we need to install Git. This is used to download the software from Github.com

```console
sudo apt -y install git
```

## Download

**Disclaimer:** If you have TerrariumPI 3 running on this Raspberry PI, then you can [read here](#backup) how to stop and make a backup.

After Git is installed, we can download the Terrariumpi source code. We will only download the latest version.

```console
git clone --branch 4.x.y.z --depth 1 https://github.com/theyosh/TerrariumPI.git
```

## Installation

And the final step is to start the installer. This will guide you through the installation process.

The first time you run the installer, it will also update the Raspberry PI OS to the latest version. This can take some more time.

```console
cd TerrariumPI
sudo ./install.sh
```

After the installation is done, reboot once and you should be able to access TerrariumPI on the url `http://[raspberrypi]:8090`. [Continue with the setup]({% link _tabs/setup.md %})

# Migration from V3 to V4

There is no real migration from version 3 to version 4. The changes are to big. So that means you have to install TerrariumPI v4 as it was a new PI. These migrations steps will only copy the existing relay history data from V3 to V4 so that the total power and water usages is still there. And the total costs are still correct. This is all what will be migrated.

If you do **not care** about your relay history, you can just skip this migration.

## Backup

So make sure you have **stopped** the old TerrariumPI. And rename the folder `TerrariumPI` to `TerrariumPI.old`. This way you have a backup of your existing working setup.

1. Stop TerrariumPI 3. [Wiki](https://github.com/theyosh/TerrariumPI/wiki/FAQ#how-to-stop-terrariumpi)

2. Make a backup of existing version. `mv /home/pi/TerrariumPI /home/pi/TerrariumPI.old`

Now, install TerrariumPI v4 as [described here](#terrariumpi). And then you need to set it up as you want. So that means adding sensors and relays. When that is running, you can start migrating the relay history data.


## Migrate

1. First make sure you have an backup of files of the old V3 version:
  - settings.cfg
  - history.db

2. Stop the TerrariumPI service before start migrating. `sudo service terrariumpi stop`

3. Enter the new TerrariumPI V4 directory. `cd /home/pi/TerrariumPI`

4. Enter the Python3 virtual environment. `souce venv/bin/activate`

5. Enter the `contrib` folder where the file `copy_relay_history.py` is located.

6. Run the script `copy_relay_history.py` with the following parameters in this order:
  - full path to OLD config (`settings.cfg`)
  - full path to OLD database (`history.db`)
  - full path to NEW database (`terrariumpi.db`)

7. Answer the questions asked by the script. This should match your old and new relays, in order to copy the historycal data.

```
Found 7 out of 8 are found. Below is a summary of the founded relays that can converted.

Relay 'Waterton verwarming' of type 'ftdi' at address '4,A500WMST'. Old ID: 7506c0e9ca0288be148b9617d959e7a6 => New ID: 91e8236ba878587c218b5a9a941a1d48
Relay 'Mister' of type 'eg-pm-lan' at address 'http://cvaVMnTiMYS35Be@192.168.5.150#2'. Old ID: 30f7595d5a055dc5b2a31127c93c9606 => New ID: 75588e78194b941b937b404db134422e
Relay 'Verwarmingmat' of type 'ftdi' at address '1,A500WMST'. Old ID: 137488ac23a2b0b516daa315641a178c => New ID: 477dd5dad0da139f8b48225acd3901d3
Relay 'UV Lamp' of type 'ftdi' at address '2,A500WMST'. Old ID: 4a2151d5834fe888820c831e9a6d8e8b => New ID: 97c45c98476b1807a4bfa7bb4d249b14
Relay 'Sproeier' of type 'ftdi' at address '3,A500WMST'. Old ID: 01ec0c8f3c4fd952c1b2aef8a4e9ec0d => New ID: beb111bdacda89f8bf13cc749ecd26c0
Relay 'Dripper plant' of type 'eg-pm-lan' at address 'http://cvaVMnTiMYS35Be@192.168.5.150#1'. Old ID: c867377cd5b6e1d4be580c1fa865ee82 => New ID: f53904eaedfac445e6cdae611612441f
Relay 'Heat lamp' of type 'nextevo-dimmer' at address '32'. Old ID: 574e22d2b2d6e54ecd5a3db8e6bb50b9 => New ID: 0e0cf978ca6bdb8eb994c186434a628e

The following relays could not be found:
Relay 'wemotest' of type 'wemo' at address '192.168.5.55'.

If you are happy with this setup, you can continue with the conversion. This will take a lot of time....
Enter 'yes' to continue. Anything else will abort.:
```

Enter yes and wait. After the migration is done, you will see a message and you can then start the TerrariumPI service. `sudo service terrariumpi start`