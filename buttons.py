# https://github.com/pskowronek/epaper-clock-and-more, Apache 2 license

import logging
import RPi.GPIO as GPIO


class Buttons(object):

    action_in_progress = False


    def __init__(self, keys, button_handler):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(keys[0], GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(keys[1], GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(keys[2], GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(keys[3], GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.add_event_detect(keys[0], GPIO.FALLING, callback=lambda pin: self.button_pressed(1, button_handler), bouncetime=200)
        GPIO.add_event_detect(keys[1], GPIO.FALLING, callback=lambda pin: self.button_pressed(2, button_handler), bouncetime=200)
        GPIO.add_event_detect(keys[2], GPIO.FALLING, callback=lambda pin: self.button_pressed(3, button_handler), bouncetime=200)
        GPIO.add_event_detect(keys[3], GPIO.FALLING, callback=lambda pin: self.button_pressed(4, button_handler), bouncetime=200)


    def set_busy(self):
        self.action_in_progress = True


    def set_not_busy(self):
        self.action_in_progress = False


    def busy(self):
        return self.action_in_progress


    def button_pressed(self, buttonNo, open_action):
        if self.busy():
            logging.info("Button #{} ignored".format(buttonNo))
            return
        try:
            self.set_busy()
            logging.info("Button #{} pressed".format(buttonNo))
            open_action(buttonNo)
        finally:
            logging.info("Finishing button key press handling")

