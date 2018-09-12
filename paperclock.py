# Original code: https://github.com/prehensile/waveshare-clock
# Modifications: https://github.com/pskowronek/eink-clock-and-more, Apache 2 license

import logging
import json
import os
import time
from PIL import Image

import drawing
from airly import Airly
from weather import Weather
from gmaps import GMaps


# only update once an hour within these ranges
DEAD_TIMES = [
    range(1,5)          # TODO make it configurable via env vars
]

DEVICE_TYPE = os.environ.get("EINK_TYPE", 'waveshare-2.7')


if DEVICE_TYPE == 'waveshare-2.7':          # TODO refactor to use enums
    # Display resolution for 2.7"
    EPD_WIDTH       = 176
    EPD_HEIGHT      = 264
    MONO_DISPLAY    = False
elif DEVICE_TYPE == 'waveshare-4.2':
    # Display resolution for 4.2"
    EPD_WIDTH       = 400
    EPD_HEIGHT      = 300
    MONO_DISPLAY    = True
else:
    raise Exception('Incorrect eink screen type: ' + DEVICE_TYPE)


MONO_DISPLAY = bool(os.environ.get("EINK_MONO", MONO_DISPLAY))   # one may override but must replace relevant library edpXinX.py, by default lib for 2.7 is bi-color, 4.2 is mono


class PaperClock(object):

    airly = Airly()
    weather = Weather()
    gmaps1 = GMaps(os.environ.get("FIRST_TIME_TO_DESTINATION_LAT"), os.environ.get("FIRST_TIME_TO_DESTINATION_LON"), "first")
    gmaps2 = GMaps(os.environ.get("SECOND_TIME_TO_DESTINATION_LAT"), os.environ.get("SECOND_TIME_TO_DESTINATION_LON"), "second")


    def __init__(self, debug_mode=False):

        self._debug_mode = debug_mode
        if not debug_mode:
            if DEVICE_TYPE == 'waveshare-2.7':
                import epd2in7
                self._epd = epd2in7.EPD()
            elif DEVICE_TYPE == 'waveshare-4.2':
                import epd4in2
                self._epd = epd4in2.EPD()

            self._epd.init()

        self._str_time = "XXXX"


    def display(self, black_buf, red_buf, dt):
        if self._debug_mode:
            debug_output = "/tmp/paperclock-" + dt.strftime("%H-%M-%S")
            logging.info("Debug mode - saving screen output to: " + debug_output + "* bmps")
            black_buf.save(debug_output + "_bw_frame.bmp")
            red_buf.save(debug_output + "_red_frame.bmp")
            return

        if not MONO_DISPLAY:
            self._epd.display_frame(
                self._epd.get_frame_buffer(black_buf),
                self._epd.get_frame_buffer(red_buf)
            )
        else:
            self._epd.display_frame(
                self._epd.get_frame_buffer(black_buf)
            )


    def display_buffer(self, black_buf, red_buf, dt):

        if DEVICE_TYPE == 'waveshare-2.7':
            black_buf = black_buf.transpose(Image.ROTATE_90)
            black_buf = black_buf.resize((EPD_WIDTH, EPD_HEIGHT), Image.LANCZOS)

            red_buf = red_buf.transpose(Image.ROTATE_90)
            red_buf = red_buf.resize((EPD_WIDTH, EPD_HEIGHT), Image.LANCZOS)

        self.display(black_buf, red_buf, dt)


    def update_for_datetime(self, dt):
        time_format = "%H%M"
        formatted = dt.strftime(time_format)

        # set blank minutes if time's hour is within dead ranges
        h = formatted[:2]
        for dead_range in DEAD_TIMES:
            if int(h) in dead_range:
                formatted = "{}  ".format(h)

        if formatted != self._str_time:

            weather_data = PaperClock.weather.get()
            logging.info("--- weather: " + json.dumps(weather_data))

            airly_data = PaperClock.airly.get()
            logging.info("--- airly: " + json.dumps(airly_data))

            gmaps1_data = PaperClock.gmaps1.get()
            logging.info("--- gmaps1: " + json.dumps(gmaps1_data))

            gmaps2_data = PaperClock.gmaps2.get()
            logging.info("--- gmaps2: " + json.dumps(gmaps2_data))

            black_frame, red_frame = drawing.draw_frame(
                MONO_DISPLAY,
                formatted,
                weather_data,
                airly_data,
                gmaps1_data,
                gmaps2_data
            )
            self.display_buffer(black_frame, red_frame, dt)

            self._str_time = formatted

        time.sleep(60)
