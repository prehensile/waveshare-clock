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
import logging.handlers

import babel

#import imagedata
from paperclock import PaperClock


DEBUG_MODE = os.environ.get( "CLOCK_DEBUG", "no" ) == "yes"


def main():

    tz_name = "GMT" if DEBUG_MODE else time.tzname[1]
    tz_sys = babel.dates.get_timezone(
        tz_name
    )

    clock = PaperClock( debug_mode=DEBUG_MODE )
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
        formatter = logging.Formatter('PaperClock: %(message)s')
        handler = logging.handlers.SysLogHandler( address=log_address )
        handler.setFormatter( formatter )
    
    logger.addHandler( handler )


if __name__ == '__main__':
    init_logging()
    try:
        main()
    except Exception as e:
        logging.exception( e )
        raise
