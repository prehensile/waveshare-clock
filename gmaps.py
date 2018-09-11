# Original code: https://github.com/prehensile/waveshare-clock
# Modifications: https://github.com/pskowronek/eink-clock-and-more, Apache 2 license

from acquire import Acquire

import logging
import json
import os
import string
import requests
from collections import namedtuple

GMapsTuple = namedtuple( 'Gmaps', ['time_to_dest', 'time_to_dest_in_traffic' ] )

class GMaps(Acquire):
    
    def __init__(self, lat, lon, name):
        self.lat = lat
        self.lon = lon
        self.name = name

    def cache_name(self):
        return "gmaps-{}.json".format(self.name)

    def acquire(self):
        logging.info( "Getting time to get to dest1 from the internet...")

        try:
            r = requests.get(
                "https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&departure_time=now&origins={},{}&destinations={},{}&key={}".format(
                    os.environ.get( "LAT" ),            # move it to c-tor (and the same for other impls of acquire)
                    os.environ.get( "LON" ),            # move it to c-tor (and the same for other impls of acquire)
                    self.lat,
                    self.lon,
                    os.environ.get( "GOOGLE_MAPS_KEY" ) # move it to c-tor (and the same for other impls of acquire)
                ),
            )
            return r
        except Exception as e:
            logging.exception( e )

        return None

    def get(self):

        gmaps_data = self.load()

        return GMapsTuple(
            time_to_dest=gmaps_data['rows'][0]['elements'][0]['duration']['value'], # in seconds
            time_to_dest_in_traffic=gmaps_data['rows'][0]['elements'][0]['duration_in_traffic']['value'] # in seconds

        )

