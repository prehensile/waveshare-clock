# Original code: https://github.com/prehensile/waveshare-clock
# Modifications: https://github.com/pskowronek/epaper-clock-and-more, Apache 2 license

from acquire import Acquire

import logging
import os
import requests
from collections import namedtuple


AirlyTuple = namedtuple('Airly', ['pm25', 'pm10', 'hummidity', 'pressure', 'aqi', 'level', 'advice'])


class Airly(Acquire):


    def cache_name(self):
        return "airly.json"


    def acquire(self):
        logging.info("Getting a Airly.eu status from the internet...")

        try:
            r = requests.get(
                "https://airapi.airly.eu/v2/measurements/point?indexType=AIRLY_CAQI&lat={}&lng={}".format(
                    os.environ.get("LAT"),
                    os.environ.get("LON")
                ),
                headers = {
                    "apikey" : os.environ.get("AIRLY_KEY"),
                    "Accept-Language" : "en",
                    "Accept" : "application/json"
                }
            )
            return r
        except Exception as e:
            logging.exception(e)

        return None


    def get(self):
        airly_data = self.load()
        if airly_data is None:
            return AirlyTuple(pm25=-1, pm10=-1, pressure=-1, humidity=-1, aqi=-1, level='n/a', advice='n/a')

        return AirlyTuple(
            pm25=airly_data["current"]["values"][1]['value'],
            pm10=airly_data["current"]["values"][2]['value'],
            pressure=airly_data["current"]["values"][3]['value'],
            hummidity=airly_data["current"]["values"][4]['value'],
            aqi=airly_data["current"]["indexes"][0]['value'],
            level=airly_data["current"]["indexes"][0]['level'],
            advice=airly_data["current"]["indexes"][0]['advice']
        )

