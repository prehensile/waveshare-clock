# -*- coding: utf-8 -*-
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

from PIL import Image, ImageDraw, ImageFont
#import imagedata
import babel
import babel.dates

import icons
import weather


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
        self._back = Image.open( 'images/back.bmp' )


    def display_buffer( self, buf ):
        
        if DEBUG_MODE:
            buf.save( "debug.bmp" )
            return
        
        self._epd.display_frame(
            self._epd.get_frame_buffer( buf )
        )


    def draw_temp( self, center_x, y, temp, temp_size, deg_size, deg_offset, draw ):
        font = ImageFont.truetype('./font/AkzidenzGrotesk-Cond.otf', temp_size)
        sz = font.getsize( temp )
        draw.text(
            (center_x-(sz[0]/2), y),
            temp,
            font=font,
            fill=255
        )

        font = ImageFont.truetype('./font/AkzidenzGrotesk-Cond.otf', deg_size)
        draw.text(
            (center_x+(sz[0]/2), y+deg_offset),
            u'°',
            font=font,
            fill=255
        )


    def draw_small_temp( self, center_x, y, caption, draw ):

        self.draw_temp(
            center_x,
            y,
            caption,
            80,
            40,
            10,
            draw
        )


    def draw_weather_icon( self, buf, fn_icon, pos ):

        fn_icon = os.path.join(
            "./icons",
            fn_icon
        )
        img_icon = Image.open( fn_icon )

        buf.paste( img_icon, pos )


    def draw_weather( self, buf ):

        w = weather.get_weather()

        
        icon = icons.darksky[ w.icon ]
        self.draw_weather_icon(
            buf,
            icon,
            [15,215]
        )


        draw = ImageDraw.Draw( buf )

        caption = "%0.0f" % w.temp
        top_y = 194

        self.draw_temp( 150, top_y, caption, 100, 60, 9, draw )

        mid_y = top_y + 17

        caption = "%0.0f" % w.temp_min
        self.draw_small_temp( 250, mid_y, caption, draw )

        caption = "%0.0f" % w.temp_max
        self.draw_small_temp( 350, mid_y, caption, draw )


    def update_for_datetime( self, dt ):

        tz_display = babel.dates.get_timezone('Europe/London')
        formatted = babel.dates.format_time( dt, "Hmm", tzinfo=tz_display )

        if formatted != self._str_time:

            img_buf = Image.new('1', (EPD_WIDTH, EPD_HEIGHT), 1)    # 1: clear the frame

            # constant shapes burnt into back.bmp
            img_buf.paste( self._back )

            # draw weather into buffer
            self.draw_weather( img_buf )
            
            im_width = 100
            offs = 0
            for n in formatted:
                fn = 'images/%s.bmp' % n
                img_num = Image.open(fn)
                img_buf.paste( img_num, (offs,0) )
                offs += im_width

            self.display_buffer( img_buf )
            
            self._str_time = formatted


if __name__ == '__main__':
    
    tz_sys = babel.dates.get_timezone( time.tzname[1] )

    clock = PaperClock()
    while True:
        clock.update_for_datetime(
            datetime.datetime.now( tz_sys )
        )
        time.sleep(0.5)

