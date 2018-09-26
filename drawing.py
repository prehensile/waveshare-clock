# -*- coding: utf-8 -*-

# Original code: https://github.com/prehensile/waveshare-clock
# Modifications: https://github.com/pskowronek/epaper-clock-and-more, Apache 2 license

from PIL import Image, ImageDraw, ImageFont
import textwrap

from resources import icons


class Drawing(object):


    # Virtual canvas size
    CANVAS_WIDTH = 400
    CANVAS_HEIGHT = 300

    # Temperature symbol
    TEMPERATURE_SYMBOL = u'°'


    def __init__(self, darksky_units, storm_distance_warn, aqi_warn_level, primary_time_warn_above, secondary_time_warn_above):
        self.distance_symbol = 'km' if darksky_units == 'si' else 'mi'
        self.storm_distance_warn = storm_distance_warn
        self.aqi_warn_level = aqi_warn_level
        self.primary_time_warn_above = primary_time_warn_above
        self.secondary_time_warn_above = secondary_time_warn_above


    def load_font(self, font_size):
        return ImageFont.truetype('./resources/font/default', font_size)


    def draw_text(self, x, y, text, font_size, draw, color=0):
        font = self.load_font(font_size)
        draw.text((x, y), unicode(text, "utf-8"), font=font, fill=color)
        return y + font_size * 1.2  # +20%


    def draw_multiline_text(self, x, y, text, font_size, draw, color=0):
        height = 0
        font = self.load_font(font_size)
        text_width = font.getsize(text)
        if text_width[0] * 1.05 > self.CANVAS_WIDTH - x:
            break_at = len(text) * (self.CANVAS_WIDTH - x) / text_width[0]  # rough estimation (proportion: text width to screen size minus start pos vs unknown to string len)
            lines = textwrap.wrap(text, width=break_at)
            line_counter = 0
            for line in lines:
                draw.text((x, y + line_counter * font_size * 1.1), unicode(line, "utf-8"), font=font, fill=color)
                line_counter += 1
                height += font_size * 1.2
        else:
            draw.text((x, y), unicode(text, "utf-8"), font=font, fill=color)
            height += font_size * 1.2
      
        return y + height


    def draw_weather_icon(self, buf, fn_icon, pos):
        img_icon = Image.open("./resources/icons/" + fn_icon)
        buf.paste(img_icon, pos)


    def draw_weather(self, buf, red_buf, weather):
        start_pos = (0, 200)
    
        back = Image.open('./resources/images/back.bmp')
        buf.paste(back, start_pos)

        icon = icons.darksky.get(weather.icon, None)
        if icon is not None:
            self.draw_weather_icon(
                buf,
                icon,
                [start_pos[0] + 15, start_pos[1] + 15]
            )

        draw = ImageDraw.Draw(buf)
        red_draw = ImageDraw.Draw(red_buf)

        top_y = start_pos[1] - 6

        caption = "{:0.0f}{}".format(weather.temp, self.TEMPERATURE_SYMBOL.encode('utf-8'))
        self.draw_text(85, top_y, caption, 90, draw, 255)

        storm_distance_warning = self.storm_distance_warn

        if weather.alert_title is not None:
            top_y = top_y + 3
            caption = "[!] {}".format(weather.alert_title.lower().encode('utf-8'))
            draw.rectangle((215, top_y + 5, self.CANVAS_WIDTH - 10, top_y + 95), 255, 255)
            red_draw.rectangle((215, top_y + 5, self.CANVAS_WIDTH - 10, top_y + 95), 0, 0)
            self.draw_multiline_text(220, top_y, caption, 23, red_draw, 255)
        elif weather.nearest_storm_distance is not None and weather.nearest_storm_distance <= storm_distance_warning:
            top_y = top_y + 3
            caption = "Storm @ {}{}".format(weather.nearest_storm_distance, self.distance_symbol)
            draw.rectangle((215, top_y + 5, self.CANVAS_WIDTH - 10, top_y + 95), 255, 255)
            red_draw.rectangle((215, top_y + 5, self.CANVAS_WIDTH - 10, top_y + 95), 0, 0)
            top_y = top_y + 7
            self.draw_multiline_text(230, top_y, caption, 40, red_draw, 255)
        else:
            top_y = top_y + 17
            caption = "{:0.0f}{} {:0.0f}{}".format(weather.temp_min, self.TEMPERATURE_SYMBOL.encode('utf-8'), weather.temp_max, self.TEMPERATURE_SYMBOL.encode('utf-8'))
            self.draw_text(205, top_y, caption, 60, draw, 255)


    def draw_clock(self, img_buf, formatted_time):
        start_pos = (0, 0)
        im_width = 100
        offs = 0
        for n in formatted_time:
            if n == " ":
                n = "_SPACE"
            fn = 'resources/images/%s.bmp' % n
            img_num = Image.open(fn)
            img_num = img_num.resize((img_num.size[0], img_num.size[1] / 2), Image.NEAREST)
            img_buf.paste(img_num, (start_pos[0] + offs, start_pos[1]))
            offs += im_width
        divider = Image.open('resources/images/clock-middle.bmp')
        img_buf.paste(divider, (self.CANVAS_WIDTH / 2 - 10, start_pos[1] + 10))


    def draw_text_aqi(self, x, y, text, text_size, draw):    
        font = self.load_font(text_size)
        font_width = font.getsize(text)

        # lower font size to accommodate huge polution levels
        if font_width[0] > 100:
            font = self.load_font(text_size * 2 / 3)

        draw.text((x, y), unicode(text, "utf-8"), font=font, fill=255)


    def draw_text_eta(self, x, y, text, text_size, draw):    
        font = self.load_font(text_size)
        font_width = font.getsize(text)
    
        # lower font size to accommodate time in minutes
        if font_width[0] > 100:
            font = self.load_font(text_size * 2 / 3)
        font_width = font.getsize(text)

        # one more time lower font size to accommodate time in minutes - yes, would be nice to convert value to hours or ... days
        if font_width[0] > 100:
            font = self.load_font(text_size * 2 / 4)

        draw.text((x, y), unicode(text, "utf-8"), font=font, fill=255)


    def draw_airly(self, black_buf, red_buf, airly):
        start_pos = (0, 100)
        buf = black_buf if airly.aqi < self.aqi_warn_level else red_buf

        back = Image.open('./resources/images/back_aqi.bmp')
        buf.paste(back, start_pos)

        draw = ImageDraw.Draw(buf)

        caption = "%3i" % int(round(airly.aqi))
        self.draw_text_aqi(start_pos[0] + 25, start_pos[1] - 5, caption, 90, draw)


    def draw_eta(self, idx, black_buf, red_buf, gmaps, warn_above_percent):
        start_pos = (50  + ((idx + 1) * self.CANVAS_WIDTH) / 3, 100)
        secs_in_traffic = 1.0 * gmaps.time_to_dest_in_traffic
        secs = 1.0 * gmaps.time_to_dest
        buf = black_buf if secs < 0 or secs * (100.0 + warn_above_percent) / 100.0 > secs_in_traffic else red_buf

        back = Image.open("./resources/images/back_eta_{}.bmp".format(idx))
        buf.paste(back, (((idx + 1) * self.CANVAS_WIDTH) / 3 , 100))

        draw = ImageDraw.Draw(buf)

        caption = "%2i" % int(round(secs_in_traffic / 60))

        self.draw_text_eta(start_pos[0], start_pos[1], caption, 70, draw)


    def draw_shutdown(self, is_mono):
        black_buf = Image.new('1', (self.CANVAS_WIDTH, self.CANVAS_HEIGHT), 1)
        red_buf = black_buf if (is_mono) else Image.new('1', (self.CANVAS_WIDTH, self.CANVAS_HEIGHT), 1)
        shutdown_icon = Image.open("./resources/images/shutdown.bmp")
        red_buf.paste(shutdown_icon, (0, 0))
        return black_buf, red_buf


    def draw_airly_details(self, airly):
        black_buf = Image.new('1', (self.CANVAS_WIDTH, self.CANVAS_HEIGHT), 1)
        red_buf = Image.new('1', (self.CANVAS_WIDTH, self.CANVAS_HEIGHT), 1)
        draw = ImageDraw.Draw(black_buf)
        self.draw_text(10, 10, "Air Quality Index by Airly.eu", 35, draw)

        self.draw_text(10, 60, "PM 2.5: {}, PM 10: {}".format(airly.pm25, airly.pm10), 30, draw)
        self.draw_text(10, 90, "AQI: {}, level: {}".format(airly.aqi, airly.level), 30, draw)
        y = self.draw_multiline_text(10, 140, "Advice: {}".format(airly.advice.encode('utf-8')), 25, draw)
        y = self.draw_text(10, y, "Hummidity: {}".format(airly.hummidity), 30, draw)
        y = self.draw_text(10, y, "Pressure:  {}".format(airly.pressure), 30, draw)

        return black_buf, red_buf


    def draw_gmaps_details(self, gmaps1, gmaps2):
        black_buf = Image.new('1', (self.CANVAS_WIDTH, self.CANVAS_HEIGHT), 1)
        red_buf = Image.new('1', (self.CANVAS_WIDTH, self.CANVAS_HEIGHT), 1)
        draw = ImageDraw.Draw(black_buf)
        self.draw_text(10, 10, "Traffic info by Google", 35, draw)

        y = self.draw_multiline_text(10, 50, "From: {}".format(gmaps1.origin_address.encode('utf-8')), 25, draw)
        y = self.draw_multiline_text(10, y, "To #1: {}".format(gmaps1.destination_address.encode('utf-8')), 25, draw)
        y = self.draw_text(10, y, "{}, avg: {}m, now: {}m".format(gmaps1.distance, gmaps1.time_to_dest / 60, gmaps1.time_to_dest_in_traffic / 60), 30, draw)

        y = self.draw_multiline_text(10, y, "To #2: {}".format(gmaps2.destination_address.encode('utf-8')), 25, draw)
        self.draw_text(10, y, "{}, avg: {}m, now: {}m".format(gmaps2.distance, gmaps2.time_to_dest / 60, gmaps2.time_to_dest_in_traffic / 60), 30, draw)

        return black_buf, red_buf


    def draw_weather_details(self, weather):
        black_buf = Image.new('1', (self.CANVAS_WIDTH, self.CANVAS_HEIGHT), 1)
        red_buf = Image.new('1', (self.CANVAS_WIDTH, self.CANVAS_HEIGHT), 1)
        draw = ImageDraw.Draw(black_buf)
        self.draw_text(10, 10, "Weather by DarkSky.net", 35, draw)

        self.draw_text(10, 65, "Temperature: {}{}".format(weather.temp, self.TEMPERATURE_SYMBOL.encode('utf-8')), 30, draw)
        self.draw_text(10, 95, "Daily min: {}{}, max: {}{}".format(weather.temp_min, self.TEMPERATURE_SYMBOL.encode('utf-8'), weather.temp_max, self.TEMPERATURE_SYMBOL.encode('utf-8')), 30, draw)
        y = self.draw_multiline_text(10, 145, "Daily summary: {}".format(weather.summary.encode('utf-8')), 25, draw)
    
        caption = None
        if weather.alert_description is not None:
            caption = "Alert: {}".format(weather.alert_description.encode('utf-8'))
        else:
            caption = "Forecast: {}".format(weather.forecast_summary.encode('utf-8'))
        self.draw_multiline_text(10, y, caption, 25, draw)

        return black_buf, red_buf


    def draw_system_details(self, sys_info):
        black_buf = Image.new('1', (self.CANVAS_WIDTH, self.CANVAS_HEIGHT), 1)
        red_buf = Image.new('1', (self.CANVAS_WIDTH, self.CANVAS_HEIGHT), 1)
        draw = ImageDraw.Draw(black_buf)
        self.draw_text(10, 10, "System info", 35, draw)

        self.draw_text(10, 80, "Uptime: {}".format(sys_info.uptime), 30, draw)
        self.draw_text(10, 120, "CPU usage: {}".format(sys_info.cpu_usage), 30, draw)
        self.draw_text(10, 160, "Mem usage: {}".format(sys_info.mem_usage), 30, draw)
        self.draw_text(10, 200, "Disk free: {}".format(sys_info.free_disk), 30, draw)

        return black_buf, red_buf


    def draw_frame(self, is_mono, formatted_time, weather, airly, gmaps1, gmaps2):
        black_buf = Image.new('1', (self.CANVAS_WIDTH, self.CANVAS_HEIGHT), 1)

        # for mono display we simply use black buffer so all the painting will be done in black
        red_buf = black_buf if (is_mono) else Image.new('1', (self.CANVAS_WIDTH, self.CANVAS_HEIGHT), 1)

        # draw clock into buffer
        self.draw_clock(black_buf, formatted_time)

        # draw time to dest into buffer
        self.draw_eta(0, black_buf, red_buf, gmaps1, self.primary_time_warn_above)

        # draw time to dest into buffer
        self.draw_eta(1, black_buf, red_buf, gmaps2, self.secondary_time_warn_above)

        # draw AQI into buffer
        self.draw_airly(black_buf, red_buf, airly)

        # draw weather into buffer
        self.draw_weather(black_buf, red_buf, weather)

        return black_buf, red_buf


