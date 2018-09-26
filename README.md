_Language versions:_\
[![EN](https://github.com/pskowronek/epaper-clock-and-more/raw/master/www/flags/lang-US.png)](https://github.com/pskowronek/epaper-clock-and-more) 
[![PL](https://github.com/pskowronek/epaper-clock-and-more/raw/master/www/flags/lang-PL.png)](https://translate.googleusercontent.com/translate_c?sl=en&tl=pl&u=https://github.com/pskowronek/epaper-clock-and-more)
[![DE](https://github.com/pskowronek/epaper-clock-and-more/raw/master/www/flags/lang-DE.png)](https://translate.googleusercontent.com/translate_c?sl=en&tl=de&u=https://github.com/pskowronek/epaper-clock-and-more) 

# Clock + weather + AQI + traffic - on Raspberry Pi & e-paper [![Build Status](https://travis-ci.org/pskowronek/epaper-clock-and-more.svg?branch=master)](https://travis-ci.org/pskowronek/epaper-clock-and-more)

This is a forked project of [waveshare-clock](https://github.com/prehensile/waveshare-clock) that only displayed clock and weather and supported only Waveshare 4.2inch B&W displays.
This project enhances the original project to support Waveshare 2.7inch displays with red die (BWR) and adds the following additional features:
- gauges for current traffic drive times for two configured destinations (thanks to [Google Maps API](https://developers.google.com/maps/documentation/))
- gauge for air quality index (AQI) of home location (thanks to [Airly.eu API](http://developer.airly.eu/))
- weather gauge may display:
  - alerts issued by governmental authorities - it works for the EU, US & Canada (thanks to [DarkSky.net API](https://darksky.net/dev/docs))
  - warning about storms in defined vicinity (thanks to [DarkSky.net API](https://darksky.net/dev/docs))
- buttons support to display detailed information about: weather, air quality, traffic and system information (on supported devices, i.e. 2.7inch HUT with switches)
- font with relaxed license already included in the project

For both new gauges one may configure warning levels - in such a case the particular gauge becomes red (on supported devices, i.e. 2.7inch BWR).

## Screenshots / Photos

[![Assembled](https://pskowronek.github.io/epaper-clock-and-more/www/assembled/01.JPG)](https://pskowronek.github.io/epaper-clock-and-more/www/assembled/index.html "Photos of assembled epaper + rasberry pi zero running epaper-clock-and-more")

More photos of the assembled e-paper 2.7inch display sitting on top of Raspberry Pi zero enclosed in a custom-built LEGO™ housing and running this project are [here](https://pskowronek.github.io/epaper-clock-and-more/www/assembled/index.html "Photos of assembled epaper + rasberry pi zero running epaper-clock-and-more").

*BTW, these LEGO bricks are almost 30 years old (!)*


## Hardware Requirements

- [Raspberry Pi Zero](https://botland.com.pl/moduly-i-zestawy-raspberry-pi-zero/9749-raspberry-pi-zero-wh-512mb-ram-wifi-bt-41-ze-zlaczami.html) or similar
- [e-paper display 2.7inch HUT](https://botland.com.pl/wyswietlacze-e-paper/9656-waveshare-e-paper-hat-b-27-264x176px-modul-z-wyswietlaczem-trojkolorowym-nakladka-do-raspberry-pi.html) or e-paper display 4.2inch B&W display with SPI
- 8-16GB SD card

## Installation

- install [Raspbian](https://www.raspberrypi.org/downloads/) on SD card using [this](https://www.raspberrypi.org/documentation/installation/installing-images/README.md) instruction
- enable and configure WiFi before you start the system - more [here](https://howchoo.com/g/ndy1zte2yjn/how-to-set-up-wifi-on-your-raspberry-pi-without-ethernet)
- find the IP of RPi by scanning you local network or take a look at your router to find a new device connected to your network
- SSH to your raspberry: ```ssh pi@10.20.30.40```
- python 2.7 should be already present, you may want to verify this by running: ```python --version```
- install git: ```sudo apt install git```
- issue the command to fetch this project: ```git clone https://github.com/pskowronek/epaper-clock-and-more.git```
- go to the project directory: ```cd epaper-clock-and-more``` and install required python modules: ```pip install -r requirements.txt```
- rename run-EDIT-ME.sh to run.sh and edit run.sh to configure:
  - your home location (lon & lat)
  - two destinations to check traffic delays
  - a key for traffic information from Google Maps - you can get it [here](https://developers.google.com/maps/documentation/embed/get-api-key) *)
  - a key for weather forecast from DarkSky.net - you can get it [here](https://darksky.net/dev/register) *)
  - a key for Air Quality Index data from Airly.eu - you can get it [here](https://developer.airly.eu/register) *)
  - type of e-paper device, whether it is 2.7 or 4.2 (by default it is pre-configured for 2.7" BWR)
- run the script: ```./run.sh``` (hit Ctrl-C to exit) and verify if it works as expected
- install this project as service so it could automatically run when Raspberry boots up (more details [here](https://www.raspberrypi.org/documentation/linux/usage/systemd.md))
  - copy epaper.service to /etc/systemd/system: ```sudo cp epaper.service /etc/systemd/system/``` **)
  - verify if service works by invoking the following command: ```sudo systemctl start epaper.service```
  - enable this script so it could be run on system start: ```sudo systemctl enable epaper.service```
  - reboot device to verify if it works
  - if you needed to modify epaper.service issue this command: ```sudo systemctl daemon-reload```
  - logs can be observed in /var/log/syslog: ```sudo tail -f /var/log/syslog | grep run.sh```

*) By default data are being fetched every 10+ minutes so they should comply with developer free accounts limitations

**) If your project directory is different than /home/pi/epaper-clock-and-more then you must edit this file to reflect the correct path

## Tech details

### 2.7inch & 4.2inch support

Since the original project supported 4.2inch B&W displays only, the code has been modified to support also 2.7inch B+W+R displays. This has been done by adding a second red canvas and down-sizing the black and red canvases to smaller resolutions as required by 2.7inch displays.

### 2.7inch display refresh

E-paper 2.7inch by Waveshare does not support partial refresh and every modification of displayed data requires full refresh which takes around 5s meantime flickering a lot.

### 2.7inch display refresh made faster

You may try to turn on experimental feature to make display refresh much faster (10x quicker for black die, 2-3 times quicker for red die).
This has been achieved by modification of LUT tables of original ```epd2in7b.py``` Waveshare library. The LUT tables are used by the display
to create "waveforms" that refresh every pixel. This of course has negative consequences - the refresh isn't perfect (but still okey) and
artifacts may build-up with time. To recover the display you would need to turn off this feature and run the project for a while using original LUT tables.
To see how the tables were modified issue this command: ```diff epd2in7b.py epd2in7b_fast_lut.py```

The idea of modifying the LUT tables has been described [here](http://benkrasnow.blogspot.com/2017/10/fast-partial-refresh-on-42-e-paper.html) for 4.2" displays.
Since I don't have 4.2" display I didn't try to provide similar feature for it.

To enable this feature set the following environment variable: ```export EPAPER_FAST_REFRESH=true```


## TODOs

- rework drawing.py (~~make it a class~~ and gagues rendered w/o knowledge about their final placement)

## License

Since this project is a fork, the original licenses still apply. The modifications and enhancements are being done under Apache 2 license.

## Authors

- [Piotr Skowronek](https://github.com/pskowronek)
- [Original author](https://github.com/prehensile)

