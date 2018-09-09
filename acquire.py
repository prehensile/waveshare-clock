# Original code: https://github.com/prehensile/waveshare-clock
# Modifications: https://github.com/pskowronek/eink-clock-and-more, Apache 2 license

import logging

import json
import os
import string
import time
from collections import namedtuple

import requests

class Acquire():

    def cache_name(self):
        return "base.json"

    def cache_path(self):
        pth_cache = os.path.expanduser( "~/.eink-display/cache/" )
        if not os.path.exists( pth_cache ):
            os.makedirs( pth_cache )
        return os.path.join( pth_cache, self.cache_name() )


    def load_cached(self):
        cached = None
        fn_cache = self.cache_path()
        if os.path.exists(fn_cache):
            logging.info( "load cache file: %s" % fn_cache )
            with open(fn_cache) as fp:
                return json.load(fp)

        return None

    def get_cache_ts(self):
        fn_cache = self.cache_path()
        if os.path.exists(fn_cache):
            return os.path.getmtime(fn_cache)
        return None


    def acquire(self):
        logging.warn( "Don't call base!")
        return None


    def load(self):
        # start from cached data 
        acquired_data = self.load_cached()

        # no data has been cached yet
        if acquired_data is None:
            logging.info("No cache found")
            acquired_json = self.acquire()
            if acquired_json is not None:
                acquired_data = acquired_json.json()
                # write just acquired data to cache
                fn_cache = self.cache_path()
                with open(fn_cache,'wb') as fp:
                    fp.write( acquired_json.text.encode('utf-8') )
            else:
                acquired_data = None
        else:
            # get last modified time for cache...
            ts_cache = self.get_cache_ts()

            # refresh every 10 minutes
            if ts_cache is not None:
                now = time.time()
                if (now - ts_cache) > 60*10: # every 10 mins
                    logging.info("Cache too old, renewing...")
                    acquired_json = self.acquire()
                    acquired_data = acquired_json.json()
                    fn_cache = self.cache_path()
                    with open(fn_cache,'wb') as fp:
                        fp.write( acquired_json.text.encode('utf-8') )

        return acquired_data

    def get(self):
        logging.warn( "Don't call base" )
        return None
