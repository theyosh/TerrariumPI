---
title: "Energenie USB"
categories: [Hardware, Relay]
tags: [relay, energenie]

image:
  src: /assets/img/Energenie_USB.webp
  alt: "Energenie USB header image"

device_address: "Enter the relay number from 1 - 4. Optional you can enter the Serial address of the board if you have multiple relay boards like: `1,0035685`"
device_auto_detect: true
---

## Information
EG-PM2 / EG-PMS2 is a power outlet strip with advanced power management features. It is possible to individually switch 4 sockets on or off manually via your PC, by timer schedule, or by programmable special events (eg: switch on my scanner whenever I start Photoshop, or have my printer switched on only when I really print)

[More information ...](https://energenie.com/item.aspx?id=7556)

## Outdated software

**This is included in the Docker image.**

In order to support newer devices you need to upgrade the software package `sispmctl`. The current version on the Raspberry PI is unfortunally outdated. Upgrading is a manual action, which will install a second `sispmctl` on your system on the location `/usr/local/bin/` which my software will automatically detect. So after upgrading `sispmctl` and restarting TerrariumPI, you should be good to go.

Go to [https://sourceforge.net/projects/sispmctl/files/sispmctl/](https://sourceforge.net/projects/sispmctl/files/sispmctl/) and enter the folder with the highest version number. At time of writing that is 4.9

1. Install needed libraries: `sudo apt install libusb-dev`
2. Install sispmctl:
```console
wget https://sourceforge.net/projects/sispmctl/files/sispmctl/sispmctl-4.9/sispmctl-4.9.tar.gz/download -O sispmctl-4.9.tar.gz
tar zxvf sispmctl-4.9.tar.gz
cd sispmctl-4.9/
./configure
make
sudo make install
sudo ldconfig
```
3. Restart TerrariumPI service ([FAQ]({% link _faq/systemd.md %}#restart))

The needed permisions to connect to the device through USB are already set.


{% include_relative _relay_detail.md %}