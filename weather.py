# Original code: https://github.com/prehensile/waveshare-clock
# Modifications: https://github.com/pskowronek/eink-clock-and-more, Apache 2 license

from acquire import Acquire

import os
import logging
import json
import requests
from collections import namedtuple

WeatherTuple = namedtuple( 'Weather', ['temp','temp_min','temp_max','icon'] )

class Weather(Acquire):

    def cache_name(self):
        return "darksky.json"

    def acquire(self):
        logging.info( "Get a fresh forecast from the internet...")

        try:
            r = requests.get(
                "https://api.darksky.net/forecast/{}/{},{}".format(
                    os.environ.get( "DARKSKY_KEY" ),
                    os.environ.get( "LAT" ),
                    os.environ.get( "LON" )
                ),
                params = {
                    "units" : "si",
                    "exclude" : "minutely,hourly,alerts,flags"
                }
            )
            return r

        except Exception as e:
            logging.exception( e )

        return None

    def get(self):
        forecast_data = self.load()
        d = forecast_data["daily"]["data"][0]

        temp_min = d["temperatureMin"]
        temp_max = d["temperatureMax"]

        c = forecast_data['currently']

        return WeatherTuple(
            temp=c['temperature'],
            temp_min=temp_min,
            temp_max=temp_max,
            icon=d['icon']
        )
