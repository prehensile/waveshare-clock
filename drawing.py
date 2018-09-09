# -*- coding: utf-8 -*-

# Original code: https://github.com/prehensile/waveshare-clock
# Modifications: https://github.com/pskowronek/eink-clock-and-more, Apache 2 license

import os 

from PIL import Image, ImageDraw, ImageFont

import icons

# Display resolution for 2.7" (temporary measure until support for both 2.7" and 4.2" implemented)
EPD_WIDTH       = 176
EPD_HEIGHT      = 264

# Virtual canvas size
CANVAS_WIDTH = 400
CANVAS_HEIGHT = 300

def draw_temp( center_x, y, temp, temp_size, deg_size, deg_offset, draw ):
    font = ImageFont.truetype('./font/default', temp_size)
    text_width = font.getsize( temp )
    draw.text(
        (center_x-(text_width[0]/2), y),
        temp,
        font=font,
        fill=255
    )

    point_width = font.getsize( u'°')

    font = ImageFont.truetype('./font/default', deg_size)
    draw.text(
        (center_x+(text_width[0]/2) - point_width[0]/2 + 10, y+deg_offset),
        u'°',
        font=font,
        fill=255
    )


def draw_small_temp( center_x, y, caption, draw ):

    draw_temp(
        center_x,
        y,
        caption,
        60,
        40,
        7,
        draw
    )

def draw_weather_icon( buf, fn_icon, pos ):

    fn_icon = os.path.join(
        "./icons",
        fn_icon
    )
    img_icon = Image.open( fn_icon )

    buf.paste( img_icon, pos )


def draw_weather( buf, weather ):
    back = Image.open( 'images/back.bmp' )
    buf.paste( back, (0, 200))

    icon = icons.darksky[ weather.icon ]
    draw_weather_icon(
        buf,
        icon,
        [15,215]
    )

    draw = ImageDraw.Draw( buf )

    caption = "%0.0f" % weather.temp
    top_y = 194

    draw_temp( 150, top_y, caption, 100, 60, 6, draw )

    mid_y = top_y + 17

    caption = "%0.0f" % weather.temp_min
    draw_small_temp( 250, mid_y, caption, draw )

    caption = "%0.0f" % weather.temp_max
    draw_small_temp( 350, mid_y, caption, draw )

def draw_clock(img_buf, formatted_time):

    im_width = 100
    offs = 0
    for n in formatted_time:
        if n == " ":
            n = "_SPACE"
        fn = 'images/%s.bmp' % n
        img_num = Image.open(fn)
        img_num = img_num.resize((img_num.size[0], img_num.size[1]/2), Image.LANCZOS)

        img_buf.paste( img_num, (offs,0) )
        offs += im_width

def draw_aqi( x, y, text, text_size, draw ):
    font = ImageFont.truetype('./font/default', text_size)
    draw.text(
        (x, y),
        text,
        font=font,
        fill=255
    )

def draw_airly(buf, airly):
    back = Image.open( 'images/back.bmp' )
    buf.paste( back, (0, 100))

    draw = ImageDraw.Draw( buf )

    caption = "AQI: %0.0f" % airly.aqi
    draw_aqi( 7, 95, caption, 90, draw )


def draw_frame( formatted_time, weather, airly ):
    img_buf = Image.new('1', (CANVAS_WIDTH, CANVAS_HEIGHT), 1)    # 1: clear the frame
    red_buf = Image.new('1', (CANVAS_WIDTH, CANVAS_HEIGHT), 1)    # 1: clear the red frame


    # draw weather into buffer
    draw_weather( img_buf, weather )
    
    # draw AQI into buffer
    draw_airly( img_buf, airly )
    
    # draw clock into buffer
    draw_clock( img_buf, formatted_time )
    
    img_buf = img_buf.transpose(Image.ROTATE_90)
    img_buf = img_buf.resize((EPD_WIDTH, EPD_HEIGHT), Image.LANCZOS)

    red_buf = red_buf.transpose(Image.ROTATE_90)
    red_buf = red_buf.resize((EPD_WIDTH, EPD_HEIGHT), Image.LANCZOS)

    return img_buf, red_buf
