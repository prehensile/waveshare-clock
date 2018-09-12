#!/bin/bash

# comment out 2 lines below when you configurate the environment variables
echo "Please edit and configure this script for your needs"
exit 1


# Lat & lon of your home (a base point)
export LAT=50.0720519
export LON=20.0373204

# A key for traffic delays from Google Maps Distance Matrix API
export GOOGLE_MAPS_KEY=GET_YOUR_OWN_KEY     # get the key from: https://developers.google.com/maps/documentation/embed/get-api-key
# A key for weather forecasts from DarkSky.net API
export DARKSKY_KEY=GET_YOUR_OWN_KEY         # get the key from: https://darksky.net/dev/register
# A key for AQI (Air Quality Index) from AIRLY.EU API (data for certain countries only as yet)
export AIRLY_KEY=GET_YOUR_OWN_KEY           # get the key from: https://developer.airly.eu/register

export AQI_WARN_LEVEL=75                    # above this value the displayed block will become red (on supported displays)

# Lat & lon of destination you want to calculate the current driving time including traffic
export FIRST_TIME_TO_DESTINATION_LAT=49.9684476
export FIRST_TIME_TO_DESTINATION_LON=20.4303646
# The displayed block will become red (on supported displays) when driving time exceeds by % 
export FIRST_TIME_WARN_ABOVE_PERCENT=50

# Lat & lon of second destination (for a second member of a household?) you want to calculate the current driving time including traffic
export SECOND_TIME_TO_DESTINATION_LAT=49.9684476
export SECOND_TIME_TO_DESTINATION_LON=20.4303646
# The displayed block will become red (on supported displays) when driving time exceeds by % 
export SECOND_TIME_WARN_ABOVE_PERCENT=50

# A type of EPAPER display you want to use - either Waveshare 4"2 (mono) or 2"7 (bi-color) - this automatically sets EPAPER_MONO to True for 2"7 and to False for 4"7
#export EPAPER_TYPE=waveshare-4.2
export EPAPER_TYPE=waveshare-2.7
# You can override the setting as whether the display is mono or not - though, it will require update (replacement) of relevant epdXinX.py library to support mono or bi-color
#export EPAPER_MONO=True
# You can ovveride as to wether to listen for button press (enabled by default)
#export EPAPER_BUTTONS_ENABLED=True
# You can override GPIO pins assigned to buttons (these values are set by default)
#export EPAPER_GPIO_PIN_FOR_KEY1=5
#export EPAPER_GPIO_PIN_FOR_KEY2=6
#export EPAPER_GPIO_PIN_FOR_KEY3=13
#export EPAPER_GPIO_PIN_FOR_KEY4=19

python main.py
