_Language versions:_\
[![EN](https://github.com/pskowronek/epaper-clock-and-more/raw/master/www/flags/lang-US.png)](https://github.com/pskowronek/epaper-clock-and-more) 
[![PL](https://github.com/pskowronek/epaper-clock-and-more/raw/master/www/flags/lang-PL.png)](https://translate.googleusercontent.com/translate_c?sl=en&tl=pl&u=https://github.com/pskowronek/epaper-clock-and-more)
[![DE](https://github.com/pskowronek/epaper-clock-and-more/raw/master/www/flags/lang-DE.png)](https://translate.googleusercontent.com/translate_c?sl=en&tl=de&u=https://github.com/pskowronek/epaper-clock-and-more) 

# Clock + weather + AQI + traffic - on Raspberry Pi & e-paper [![Build Status](https://travis-ci.org/pskowronek/epaper-clock-and-more.svg?branch=master)](https://travis-ci.org/pskowronek/epaper-clock-and-more)

This is a forked project of [waveshare-clock](https://github.com/prehensile/waveshare-clock) that only displayed clock and weather and supported only Waveshare 4.2inch B&W displays.
This project enhances the orignal project to support Waveshare 2.7inch displays with red die (BWR) and adds additional features:
- gauges for current traffic drive times for two configured destinations (thanks to Google Maps API)
- gauge for air quality index (AQI) of home location (thanks to Airly.eu API)
- buttons handlers to display detailed information about: weather, air quality, traffic and system information (on supported devices, i.e. 2.7inch HUT with switches)
- font with relaxed license already included in the project

For both new gauges one may configure warning levels - in such a case the particular gauge becomes red (on supported devices, i.e. 2.7inch BWR).

## Hardware Requirements

- [Raspberry Pi Zero](https://botland.com.pl/moduly-i-zestawy-raspberry-pi-zero/9749-raspberry-pi-zero-wh-512mb-ram-wifi-bt-41-ze-zlaczami.html) or similar
- [e-paper display 2.7inch HUT](https://botland.com.pl/wyswietlacze-e-paper/9656-waveshare-e-paper-hat-b-27-264x176px-modul-z-wyswietlaczem-trojkolorowym-nakladka-do-raspberry-pi.html) or e-paper display 4.2inch B&W display with SPI
- 8-16GB SD card

## Installation

- install [Raspbian](https://www.raspberrypi.org/downloads/) on SD card using [this](https://www.raspberrypi.org/documentation/installation/installing-images/README.md) instruction
- enable and configure WiFi before you start the system - more [here](https://howchoo.com/g/ndy1zte2yjn/how-to-set-up-wifi-on-your-raspberry-pi-without-ethernet)
- find the IP of RPi by scanning you local network or take a look at your router to find a new device connected to your network
- SSH to your raspberry: ssh pi@10.20.30.40
- python should be already present, you may want to verify this by running: ```python --version```
- install git: ```sudo apt install git```
- issue this command to fetch this project: ```git clone https://github.com/pskowronek/epaper-clock-and-more.git```
- go to project directory: ```cd epaper-clock-and-more``` and install required python modules: ```pip install -r requirements.txt```
- edit run-clock.sh and configure:
  - your home location (lon & lat)
  - two destinations to check traffic delays
  - a key for traffic information from Google Maps - you can get it [here](https://developers.google.com/maps/documentation/embed/get-api-key) *)
  - a key for weather forecast from DarkSky.net - you can get it [here](https://darksky.net/dev/register) *)
  - a key for Air Quality Index data from Airly.eu - you can get it [here](https://developer.airly.eu/register) *)
  - type of e-paper device, whether is it 2.7 or 4.2 (by default it is pre-configured for 2.7" BWR)
- run the script: ```./run-clock.sh``` (hit Ctrl-C to exit)

*) Data are being fetched every 10 minutes so they should comply with developer free accounts limitations.

## Tech details

### 2.7inch & 4.2inch support

Since the original project supported 4.2inch B&W displays only the code has been modified to support also 2.7inch B+W+R displays. This has been done by adding a second red canvas and down-sizing the black and red canvases to smaller resolutions as required by 2.7inch displays.

### 2.7inch display refresh

E-paper 2.7inch by Waveshare does not support partial refresh and every modification of displayed data requires full refresh which takes around 5s meantime flickering a lot.


## TODOs

- better support for button key press (to avoid multiple action execution if you press the button too long)
- rework drawing.py
- configurable cache per data provider
- add system info (executed by 4th button)
- better time/delay handling to refresh every 60s (use scheduler)
- detailed info executed by key press should be kept on screen for some amount of time (now the clock update closes/repaints the info)
- service script and instructions to launch epaper-clock-and-more on system start

## License

Since this project is a fork the original licenses still apply. The modifications and enhancements are being done under Apache 2 license.

## Authors

- [Piotr Skowronek](https://github.com/pskowronek)
- [Original author](https://github.com/prehensile)

