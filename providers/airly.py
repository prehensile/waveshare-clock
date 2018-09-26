# Original code: https://github.com/prehensile/waveshare-clock
# Modifications: https://github.com/pskowronek/epaper-clock-and-more, Apache 2 license

from acquire import Acquire

import logging
import requests
from collections import namedtuple


AirlyTuple = namedtuple('Airly', ['pm25', 'pm10', 'hummidity', 'pressure', 'aqi', 'level', 'advice'])


class Airly(Acquire):


    DEFAULT = AirlyTuple(pm25=-1, pm10=-1, pressure=-1, hummidity=-1, aqi=-1, level='n/a', advice='n/a')


    def __init__(self, key, lat, lon, cache_ttl):
        self.key = key
        self.lat = lat
        self.lon = lon
        self.cache_ttl = cache_ttl


    def cache_name(self):
        return "airly.json"


    def ttl(self):
        return self.cache_ttl


    def acquire(self):
        logging.info("Getting a Airly.eu status from the internet...")

        try:
            r = requests.get(
                "https://airapi.airly.eu/v2/measurements/point?indexType=AIRLY_CAQI&lat={}&lng={}".format(
                    self.lat,
                    self.lon
                ),
                headers = {
                    "apikey" : self.key,
                    "Accept-Language" : "en",
                    "Accept" : "application/json"
                }
            )
            return r
        except Exception as e:
            logging.exception(e)

        return None


    def get(self):
        try:
            airly_data = self.load()
            if airly_data is None:
                return self.DEFAULT

            return AirlyTuple(
                pm25=airly_data["current"]["values"][1]['value'],
                pm10=airly_data["current"]["values"][2]['value'],
                pressure=airly_data["current"]["values"][3]['value'],
                hummidity=airly_data["current"]["values"][4]['value'],
                aqi=airly_data["current"]["indexes"][0]['value'],
                level=airly_data["current"]["indexes"][0]['level'],
                advice=airly_data["current"]["indexes"][0]['advice']
            )

        except Exception as e:
            logging.exception(e)
            return self.DEFAULT


