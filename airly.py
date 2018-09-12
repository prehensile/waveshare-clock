# Original code: https://github.com/prehensile/waveshare-clock
# Modifications: https://github.com/pskowronek/eink-clock-and-more, Apache 2 license

from acquire import Acquire

import logging
import os
import requests
from collections import namedtuple


AirlyTuple = namedtuple('Airly', ['pm25', 'pm10', 'aqi'])


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

        return AirlyTuple(
            pm25=airly_data["current"]["values"][1]['value'],
            pm10=airly_data["current"]["values"][2]['value'],
            aqi=airly_data["current"]["indexes"][0]['value']
        )

