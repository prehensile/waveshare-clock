##
 #  @filename   :   main.cpp
 #  @brief      :   4.2inch e-paper display demo
 #  @author     :   Yehui from Waveshare
 #
 #  Copyright (C) Waveshare     July 28 2017
 #
 # Permission is hereby granted, free of charge, to any person obtaining a copy
 # of this software and associated documnetation files (the "Software"), to deal
 # in the Software without restriction, including without limitation the rights
 # to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 # copies of the Software, and to permit persons to  whom the Software is
 # furished to do so, subject to the following conditions:
 #
 # The above copyright notice and this permission notice shall be included in
 # all copies or substantial portions of the Software.
 #
 # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 # IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 # FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 # AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 # LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 # OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 # THE SOFTWARE.
 ##

import datetime
import time
import os
import sys
import logging

#import imagedata
import babel
import babel.dates

import weather
import drawing


EPD_WIDTH = 400
EPD_HEIGHT = 300

DEBUG_MODE = os.environ.get( "CLOCK_DEBUG", "no" ) == "yes"


class PaperClock( object ):

    def __init__( self ):
        
        if not DEBUG_MODE:
            import epd4in2
            self._epd = epd4in2.EPD()
            self._epd.init()
        
        self._str_time = "XXXX"


    def display_buffer( self, buf ):
        
        if DEBUG_MODE:
            buf.save( "debug.bmp" )
            return
        
        self._epd.display_frame(
            self._epd.get_frame_buffer( buf )
        )


    def update_for_datetime( self, dt ):

        tz_display = babel.dates.get_timezone('Europe/London')
        formatted = babel.dates.format_time( dt, "HHmm", tzinfo=tz_display )

        if formatted != self._str_time:

            w = weather.get_weather()

            frame = drawing.draw_frame(
                EPD_WIDTH, EPD_HEIGHT,
                formatted,
                w
            )
            self.display_buffer( frame )
            
            self._str_time = formatted


def main():

    tz_name = "GMT" if DEBUG_MODE else time.tzname[1]
    tz_sys = babel.dates.get_timezone(
        tz_name
    )

    clock = PaperClock()
    while True:
        clock.update_for_datetime(
            datetime.datetime.now( tz_sys )
        )
        time.sleep(0.5)


def init_logging():

    logger = logging.getLogger()
    logger.setLevel( logging.DEBUG )

    handler = None
    if DEBUG_MODE:
        handler = logging.StreamHandler( sys.stdout )
    else:
        log_address = '/var/run/syslog' if sys.platform == 'darwin' else '/dev/log'
        handler = logging.handlers.SysLogHandler( address=log_address )
    
    logger.addHandler( handler )


if __name__ == '__main__':
    init_logging()
    try:
        main()
    except Exception as e:
        logging.exception( e )
        raise
