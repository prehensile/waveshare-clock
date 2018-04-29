# -*- coding: utf-8 -*-

import os 

from PIL import Image, ImageDraw, ImageFont

import icons


def draw_temp( center_x, y, temp, temp_size, deg_size, deg_offset, draw ):
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


def draw_small_temp( center_x, y, caption, draw ):

    draw_temp(
        center_x,
        y,
        caption,
        80,
        40,
        10,
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

    icon = icons.darksky[ weather.icon ]
    draw_weather_icon(
        buf,
        icon,
        [15,215]
    )


    draw = ImageDraw.Draw( buf )

    caption = "%0.0f" % weather.temp
    top_y = 194

    draw_temp( 150, top_y, caption, 100, 60, 9, draw )

    mid_y = top_y + 17

    caption = "%0.0f" % weather.temp_min
    draw_small_temp( 250, mid_y, caption, draw )

    caption = "%0.0f" % weather.temp_max
    draw_small_temp( 350, mid_y, caption, draw )


def draw_frame( width, height, formatted_time, weather ):
    img_buf = Image.new('1', (width, height), 1)    # 1: clear the frame

    # constant shapes burnt into back.bmp
    back = Image.open( 'images/back.bmp' )
    img_buf.paste( back )

    # draw weather into buffer
    draw_weather( img_buf, weather )
    
    im_width = 100
    offs = 0
    for n in formatted_time:
        fn = 'images/%s.bmp' % n
        img_num = Image.open(fn)
        img_buf.paste( img_num, (offs,0) )
        offs += im_width

    return img_buf