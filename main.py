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

# Original code: https://github.com/prehensile/waveshare-clock
# Modifications: https://github.com/pskowronek/epaper-clock-and-more, Apache 2 license

import os
import sys
import logging
import logging.handlers
import signal
import atexit
import sdnotify

import time
from pytz import timezone
from datetime import datetime
from tzlocal import get_localzone

from epaper import EPaper


DEBUG_MODE = os.environ.get("EPAPER_DEBUG_MODE", "false") == "true"
shutting_down = False
after_details = False
epaper = None


def main():
    global epaper
    global shutting_down
    global after_details

    epaper = EPaper(debug_mode=DEBUG_MODE)

    atexit.register(shutdown_hook)
    signal.signal(signal.SIGTERM, signal_hook)

    buttons = None
    if not DEBUG_MODE and (os.environ.get("EPAPER_BUTTONS_ENABLED", "true") == "true"):
        from buttons import Buttons
        buttons = Buttons(
            int(os.environ.get("EPAPER_GPIO_PIN_FOR_KEY1", "5")),
            lambda: epaper.display_gmaps_details(),
            int(os.environ.get("EPAPER_GPIO_PIN_FOR_KEY2", "6")),
            lambda: epaper.display_airly_details(),
            int(os.environ.get("EPAPER_GPIO_PIN_FOR_KEY3", "13")),
            lambda: epaper.display_weather_details(),
            int(os.environ.get("EPAPER_GPIO_PIN_FOR_KEY4", "19")),
            lambda: epaper.display_system_details(),
            lambda: action_after_details()
        )

    notifier = sdnotify.SystemdNotifier()
    notifier.notify("READY=1")

    while True:
        notifier.notify("WATCHDOG=1")
        logging.info("Going to refresh the main screen...")

        if shutting_down:
            logging.info("... or not - app is shutting down.")
            break
        if buttons is None or not buttons.busy():
            if buttons:
                buttons.set_busy()
            refresh_main_screen(epaper)
            if buttons:
                buttons.set_not_busy()
        else:
            logging.info("Ignoring main screen refresh due to button's orignating action")

        for i in range(30):
            if after_details:
                logging.info("State after button press - wait a while before refreshing the main window (to keep the info on display)...")
                time.sleep(5)
                after_details = False
                buttons.set_not_busy()
                break
            time.sleep(2)


def refresh_main_screen(epaper):
    utc_dt = datetime.now(timezone('UTC'))  # time readings should be done in epaper itself (probably using acquire.py w/o caching)
    epaper.display_main_screen(utc_dt.astimezone(get_localzone()))
    if DEBUG_MODE:
        epaper.display_weather_details()
        epaper.display_airly_details()
        epaper.display_gmaps_details()


def action_after_details():
    global after_details

    logging.info("Informing main thread that button action has just finished")
    after_details = True


def signal_hook(*args):
    if shutdown_hook():
        logging.info("calling exit 0")
        sys.exit(0) 


def shutdown_hook():
    global epaper
    global shutting_down
    if shutting_down:
        return False
    shutting_down = True
    logging.info("You are now leaving the Python sector - the app is being shutdown.")
    if epaper is not None:
        logging.info("...but, let's try to display shutdown icon")
        epaper.display_shutdown()
        logging.info("...finally going down")
    return True


def init_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    logger.addHandler(handler)
    
    if not DEBUG_MODE:
        log_address = '/var/run/syslog' if sys.platform == 'darwin' else '/dev/log'
        formatter = logging.Formatter('EPaper: %(message)s')
        handler = logging.handlers.SysLogHandler(address=log_address)
        handler.setFormatter(formatter)


if __name__ == '__main__':
    init_logging()
    try:
        main()
    except Exception as e:
        logging.exception(e)
        raise
