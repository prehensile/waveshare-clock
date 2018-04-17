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

from PIL import Image, ImageDraw, ImageFont
#import imagedata

import datetime
import time
import os

import requests

import icons


EPD_WIDTH = 400
EPD_HEIGHT = 300

DEBUG_MODE = True


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
            '°',
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


    def draw_weather_icon( self, buf, icon_id, pos ):

        fn_icon = os.path.join(
            "./icons",
            icons.icons[icon_id]
        )
        img_icon = Image.open( fn_icon )

        buf.paste( img_icon, pos )


    def update_weather( self, buf ):

        r = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={
                "q" : "London,GB",
                "units" : "metric",
                "appid" : os.environ.get( "WEATHER_KEY" )
            }
        )
        j=r.json()

        temp = j['main']['temp']
        temp_min = j['main']['temp_min']
        temp_max = j['main']['temp_max']


        self.draw_weather_icon(
            buf,
            j['weather'][0]['icon'],
            [15,215]
        )


        draw = ImageDraw.Draw( buf )

        caption = "%0.0f" % temp
        top_y = 194

        self.draw_temp( 150, top_y, caption, 100, 60, 9, draw )

        mid_y = top_y + 17

        caption = "%0.0f" % temp_min
        self.draw_small_temp( 250, mid_y, caption, draw )

        caption = "%0.0f" % temp_max
        self.draw_small_temp( 350, mid_y, caption, draw )


    def update_for_datetime( self, dt ):

        formatted = dt.strftime( '%H%M' )

        if formatted != self._str_time:

            img_buf = Image.new('1', (EPD_WIDTH, EPD_HEIGHT), 1)    # 1: clear the frame

            # constant shapes burnt into back.bmp
            img_buf.paste( self._back )

            # draw weather into buffer
            self.update_weather( img_buf )
            
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
    clock = PaperClock()
    while True:
        clock.update_for_datetime(
            datetime.datetime.now()
        )
        time.sleep(0.5)



def main():
    epd = epd4in2.EPD()
    epd.init()

    # For simplicity, the arguments are explicit numerical coordinates
    img_buf = Image.new('1', (EPD_WIDTH, EPD_HEIGHT), 1)    # 1: clear the frame
    # draw = ImageDraw.Draw(image)
    # font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 24)
    # draw.rectangle((0, 6, 400, 30), fill = 0)
    # draw.text((100, 10), 'e-Paper demo', font = font, fill = 255)
    # draw.rectangle((200, 80, 360, 280), fill = 0)
    # draw.arc((240, 80, 380, 220), 0, 360, fill = 255)
    # draw.rectangle((0, 80, 160, 280), fill = 255)
    # draw.arc((40, 80, 180, 220), 0, 360, fill = 0)
    
    # epd.display_frame(epd.get_frame_buffer(image))

    str_time = "XXXX"

    im_width = 100
    while True:
        dt = datetime.datetime.now()

        formatted = dt.strftime( '%H%M' )

        if formatted != str_time:
            
            offs = 0
            for n in formatted:
                fn = 'images/%s.bmp' % n
                img_num = Image.open(fn)
                img_buf.paste( img_num, (offs,0) )
                offs += im_width
            
            epd.display_frame(
                epd.get_frame_buffer( img_buf )
            )

            str_time = formatted

    # You can get frame buffer from an image or import the buffer directly:
    # epd.display_frame(imagedata.MONOCOLOR_BITMAP)
