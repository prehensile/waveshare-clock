import os
import json
import time
from collections import namedtuple

import requests


Weather = namedtuple( 'Weather', ['temp','temp_min','temp_max','icon'] )


def fetch_data():
    
    forecast_data = None

    pth_cache = os.path.expanduser( "~/.clock/cache/" )
    if not os.path.exists( pth_cache ):
        os.makedirs( pth_cache )

    fn_cache = os.path.join( pth_cache, "darksky.json" )
    if os.path.exists(fn_cache):
        
        print( "load cache file: %s" % fn_cache )

        # get last modification date for cache file
        now = time.time()
        mtime = os.path.getmtime(fn_cache)
        
        # recache every 10 minutes
        if (now - mtime) < (60*10):
            print( "Use cached forecast")
            with open(fn_cache) as fp:
                forecast_data = json.load(fp)

    
    if forecast_data is None:

        print( "Get a fresh forecast")
        r = requests.get(
            "https://api.darksky.net/forecast/{}/{}".format(
                os.environ.get( "DARKSKY_KEY" ),
                os.environ.get( "LAT_LON" )
            ),
            params = {
                "units" : "si",
                "exclude" : "minutely,hourly,alerts,flags"
            }
        )
        
        forecast_data = r.json()
        
        # write firecast data to cache
        with open(fn_cache,'wb') as fp:
            fp.write( r.text.encode('utf-8') )

    return forecast_data


def get_weather():

    forecast_data = fetch_data()        
    d = forecast_data["daily"]["data"][0]

    temp_min = d["temperatureLow"]
    temp_max = d["temperatureHigh"]

    c = forecast_data['currently']

    return Weather(
        temp=c['temperature'],
        temp_min=temp_min,
        temp_max=temp_max,
        icon=c['icon']
    )

if __name__ == '__main__':
    print( get_weather() )
