# Original code: https://github.com/prehensile/waveshare-clock
# Modifications: https://github.com/pskowronek/epaper-clock-and-more, Apache 2 license

from acquire import Acquire

import logging
import requests
from collections import namedtuple


WeatherTuple = namedtuple('Weather', ['temp', 'temp_min', 'temp_max', 'icon', 'summary', 'forecast_summary'])


class Weather(Acquire):


    def __init__(self, key, lat, lon, cache_ttl):
        self.key = key
        self.lat = lat
        self.lon = lon
        self.cache_ttl = cache_ttl


    def cache_name(self):
        return "darksky.json"


    def ttl(self):
        return self.cache_ttl


    def acquire(self):
        logging.info("Getting a fresh forecast from the internet...")

        try:
            r = requests.get(
                "https://api.darksky.net/forecast/{}/{},{}".format(
                    self.key,
                    self.lat,
                    self.lon
                ),
                params = {
                    "units" : "si",
                    "exclude" : "minutely,hourly,alerts,flags"
                }
            )
            return r

        except Exception as e:
            logging.exception(e)

        return None


    def get(self):
        forecast_data = self.load()
        if forecast_data is None:
            return WeatherTuple(temp=-99, temp_min=-99, temp_max=-99, icon='n/a', summary='n/a', forecast_summary='n/a')
        
        d = forecast_data['daily']['data'][0]

        temp_min = d['temperatureMin']
        temp_max = d['temperatureMax']

        c = forecast_data['currently']

        return WeatherTuple(
            temp=c['temperature'],
            temp_min=temp_min,
            temp_max=temp_max,
            icon=d['icon'],
            summary=c['summary'],
            forecast_summary=forecast_data['daily']['summary']
        )
