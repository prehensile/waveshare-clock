# Original code: https://github.com/prehensile/waveshare-clock
# Modifications: https://github.com/pskowronek/eink-clock-and-more, Apache 2 license

import logging
import json
import time
from datetime import datetime

import drawing
from airly import Airly
from weather import Weather


# only update once an hour within these ranges
DEAD_TIMES = [
    range(0,1),
    range(10,11)
]

class PaperClock( object ):

    airly = Airly()
    weather = Weather()

    def __init__( self, debug_mode=False ):
        
        self._debug_mode = debug_mode
        if not debug_mode:
            #import epd4in2
            import epd2in7

            #self._epd = epd4in2.EPD()
            self._epd = epd2in7.EPD()
            self._epd.init()
        
        self._str_time = "XXXX"


    def display_buffer( self, buf, red_buf, dt ):
        
        if self._debug_mode:
            debug_output = "/tmp/paperclock-" + dt.strftime("%H-%M-%S")
            logging.info("Debug mode - saving screen output to: " + debug_output + "* bmps")
            buf.save(debug_output + "_bw_frame.bmp")
            red_buf.save(debug_output + "_red_frame.bmp")
            return
        
        self._epd.display_frame(
            self._epd.get_frame_buffer( buf ),
            self._epd.get_frame_buffer( red_buf)
        )


    def update_for_datetime( self, dt ):
        start = time.time()
        time_format = "%H%M"
        formatted = dt.strftime(time_format)

        # set blank minutes if time's hour is within dead ranges
        h = formatted[:2]
        for dead_range in DEAD_TIMES:
            if int(h) in dead_range:
                formatted = "{}  ".format( h )

        if formatted != self._str_time:

            weather_data = PaperClock.weather.get()
            logging.info("--- weather: " + json.dumps(weather_data))

            airly_data = PaperClock.airly.get()
            logging.info("--- airly: " + json.dumps(airly_data))

            frame, frame_red = drawing.draw_frame(
                formatted,
                weather_data,
                airly_data
            )
            self.display_buffer( frame, frame_red, dt )
            
            self._str_time = formatted
      
        time.sleep(60)
