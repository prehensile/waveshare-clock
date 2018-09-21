# -*- coding: utf-8 -*-

# Original code: https://github.com/prehensile/waveshare-clock
# Modifications: https://github.com/pskowronek/epaper-clock-and-more, Apache 2 license

import os 
from PIL import Image, ImageDraw, ImageFont
import icons


# Virtual canvas size
CANVAS_WIDTH = 400
CANVAS_HEIGHT = 300

# Celcius symbol
CELSIUS_SYMBOL = u'°'


def draw_text(x, y, text, font_size, draw):
    font = ImageFont.truetype('./font/default', font_size)
    draw.text((x, y), unicode(text, "utf-8"), font=font, fill=0)


def draw_temp(center_x, y, temp, temp_size, deg_size, deg_offset, draw):
    font = ImageFont.truetype('./font/default', temp_size)
    text_width = font.getsize(temp)
    draw.text((center_x - (text_width[0] / 2), y), unicode(temp, "utf-8"), font=font, fill=255)

    point_width = font.getsize(CELSIUS_SYMBOL)

    font = ImageFont.truetype('./font/default', deg_size)
    draw.text((center_x + (text_width[0] / 2) - point_width[0] / 2 + 10, y + deg_offset), CELSIUS_SYMBOL, font=font, fill=255)


def draw_small_temp(center_x, y, caption, draw):
    draw_temp(center_x, y, caption, 60, 40, 7, draw)


def draw_weather_icon(buf, fn_icon, pos):
    fn_icon = os.path.join(
        "./icons",
        fn_icon
    )
    img_icon = Image.open(fn_icon)
    buf.paste(img_icon, pos)


def draw_weather(buf, weather):
    back = Image.open('images/back.bmp')
    buf.paste(back, (0, 200))

    icon = icons.darksky[ weather.icon ]
    draw_weather_icon(
        buf,
        icon,
        [15,215]
    )

    draw = ImageDraw.Draw(buf)

    caption = "%0.0f" % weather.temp
    top_y = 194

    draw_temp(150, top_y, caption, 100, 60, 6, draw)

    mid_y = top_y + 17

    caption = "%0.0f" % weather.temp_min
    draw_small_temp(250, mid_y, caption, draw)

    caption = "%0.0f" % weather.temp_max
    draw_small_temp(350, mid_y, caption, draw)


def draw_clock(img_buf, formatted_time):

    im_width = 100
    offs = 0
    for n in formatted_time:
        if n == " ":
            n = "_SPACE"
        fn = 'images/%s.bmp' % n
        img_num = Image.open(fn)
        img_num = img_num.resize((img_num.size[0], img_num.size[1] / 2), Image.NEAREST)

        img_buf.paste(img_num, (offs, 0))
        offs += im_width


def draw_text_aqi(x, y, text, text_size, draw):    
    font = ImageFont.truetype('./font/default', text_size)
    font_width = font.getsize(text)

    # lower font size to accommodate huge polution levels
    if font_width[0] > 100:
        font = ImageFont.truetype('./font/default', text_size * 2 / 3)

    draw.text((x, y), unicode(text, "utf-8"), font=font, fill=255)


def draw_text_eta(x, y, text, text_size, draw):    
    font = ImageFont.truetype('./font/default', text_size)
    font_width = font.getsize(text)
    
    # lower font size to accommodate time in minutes
    if font_width[0] > 100:
        font = ImageFont.truetype('./font/default', text_size * 2 / 3)
    font_width = font.getsize(text)

    # one more time lower font size to accommodate time in minutes - yes, would be nice to convert value to hours or ... days
    if font_width[0] > 100:
        font = ImageFont.truetype('./font/default', text_size * 2 / 4)

    draw.text((x, y), unicode(text, "utf-8"), font=font, fill=255)


def draw_airly(black_buf, red_buf, airly):
    buf = black_buf if airly.aqi < int(os.environ.get("AQI_WARN_LEVEL", "75")) else red_buf

    back = Image.open('images/back_aqi.bmp')
    buf.paste(back, (0, 100))

    draw = ImageDraw.Draw(buf)

    caption = "%i" % int(round(airly.aqi))
    draw_text_aqi(25, 100, caption, 90, draw)


def draw_eta(idx, black_buf, red_buf, gmaps, warn_above_percent):
    secs_in_traffic = 1.0 * gmaps.time_to_dest_in_traffic
    secs = 1.0 * gmaps.time_to_dest
    buf = black_buf if secs < 0 or secs * (100.0 + warn_above_percent) / 100.0 > secs_in_traffic else red_buf

    back = Image.open("images/back_eta_{}.bmp".format(idx))
    buf.paste(back, (((idx + 1) * CANVAS_WIDTH) / 3 , 100))

    draw = ImageDraw.Draw(buf)

    caption = "%i" % int(round(secs_in_traffic / 60))

    draw_text_eta(50  + ((idx + 1) * CANVAS_WIDTH) / 3 , 100, caption, 70, draw)


def draw_shutdown(is_mono):
    black_buf = Image.new('1', (CANVAS_WIDTH, CANVAS_HEIGHT), 1)
    red_buf = black_buf if (is_mono) else Image.new('1', (CANVAS_WIDTH, CANVAS_HEIGHT), 1)
    shutdown_icon = Image.open("images/shutdown.bmp")
    red_buf.paste(shutdown_icon, (0, 0))
    return black_buf, red_buf


def draw_airly_details(airly):
    black_buf = Image.new('1', (CANVAS_WIDTH, CANVAS_HEIGHT), 1)
    red_buf = Image.new('1', (CANVAS_WIDTH, CANVAS_HEIGHT), 1)
    draw = ImageDraw.Draw(black_buf)
    draw_text(10, 10, "Air Quality Index by Airly.eu", 35, draw)

    draw_text(10, 60, "PM 2.5: {}, PM 10: {}".format(airly.pm25, airly.pm10), 30, draw)
    draw_text(10, 90, "AQI: {}, level: {}".format(airly.aqi, airly.level), 30, draw)
    draw_text(10, 120, "Advice:", 30, draw)
    draw_text(10, 150, airly.advice.encode('utf-8'), 25, draw)
    draw_text(10, 200, "Hummidity: {}".format(airly.hummidity), 30, draw)
    draw_text(10, 230, "Pressure:  {}".format(airly.pressure), 30, draw)

    return black_buf, red_buf


def draw_gmaps_details(gmaps1, gmaps2):
    black_buf = Image.new('1', (CANVAS_WIDTH, CANVAS_HEIGHT), 1)
    red_buf = Image.new('1', (CANVAS_WIDTH, CANVAS_HEIGHT), 1)
    draw = ImageDraw.Draw(black_buf)
    draw_text(10, 10, "Traffic info by Google", 35, draw)

    draw_text(10, 60, "From: {}".format(gmaps1.origin_address.encode('utf-8')), 25, draw)
    draw_text(10, 120, "To #1: {}".format(gmaps1.destination_address.encode('utf-8')), 25, draw)
    draw_text(10, 150, "{}, avg: {}m, now: {}m".format(gmaps1.distance, gmaps1.time_to_dest / 60, gmaps1.time_to_dest_in_traffic / 60), 30, draw)

    draw_text(10, 200, "To #2: {}".format(gmaps2.destination_address.encode('utf-8')), 25, draw)
    draw_text(10, 230, "{}, avg: {}m, now: {}m".format(gmaps2.distance, gmaps2.time_to_dest / 60, gmaps2.time_to_dest_in_traffic / 60), 30, draw)

    return black_buf, red_buf


def draw_weather_details(weather):
    black_buf = Image.new('1', (CANVAS_WIDTH, CANVAS_HEIGHT), 1)
    red_buf = Image.new('1', (CANVAS_WIDTH, CANVAS_HEIGHT), 1)
    draw = ImageDraw.Draw(black_buf)
    draw_text(10, 10, "Weather by DarkSky.net", 35, draw)

    draw_text(10, 90, "Temperature: {}{}".format(weather.temp, CELSIUS_SYMBOL.encode('utf-8')), 30, draw)
    draw_text(10, 120, "Daily min: {}{}, max: {}{}".format(weather.temp_min, CELSIUS_SYMBOL.encode('utf-8'), weather.temp_max, CELSIUS_SYMBOL.encode('utf-8')), 30, draw)
    draw_text(10, 150, "Summary: ", 30, draw)
    draw_text(10, 180, "{}".format(weather.summary.encode('utf-8')), 25, draw)

    draw_text(10, 210, "Forecast: ", 30, draw)
    draw_text(10, 240, "{}".format(weather.forecast_summary.encode('utf-8')), 20, draw)

    return black_buf, red_buf


def draw_system_details():
    black_buf = Image.new('1', (CANVAS_WIDTH, CANVAS_HEIGHT), 1)
    red_buf = Image.new('1', (CANVAS_WIDTH, CANVAS_HEIGHT), 1)
    draw = ImageDraw.Draw(black_buf)
    draw_text(10, 10, "System info", 35, draw)

    # TBD

    return black_buf, red_buf


def draw_frame(is_mono, formatted_time, weather, airly, gmaps1, gmaps2):
    black_buf = Image.new('1', (CANVAS_WIDTH, CANVAS_HEIGHT), 1)

    # for mono display we simply use black buffer so all the painting will be done in black
    red_buf = black_buf if (is_mono) else Image.new('1', (CANVAS_WIDTH, CANVAS_HEIGHT), 1)

    # draw clock into buffer
    draw_clock(black_buf, formatted_time)

    # draw time to dest into buffer
    draw_eta(0, black_buf, red_buf, gmaps1, int(os.environ.get("FIRST_TIME_WARN_ABOVE_PERCENT", "50")))

    # draw time to dest into buffer
    draw_eta(1, black_buf, red_buf, gmaps2, int(os.environ.get("SECOND_TIME_WARN_ABOVE_PERCENT", "50")))

    # draw AQI into buffer
    draw_airly(black_buf, red_buf, airly)

    # draw weather into buffer
    draw_weather(black_buf, weather)

    return black_buf, red_buf
