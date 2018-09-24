# https://github.com/pskowronek/epaper-clock-and-more, Apache 2 license

import logging
import RPi.GPIO as GPIO


class Buttons(object):

    action_in_progress = False


    def __init__(self, key1, key1_action, key2, key2_action, key3, key3_action, key4, key4_action, close_action):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(key1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(key2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(key3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(key4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.add_event_detect(key1, GPIO.FALLING, callback=lambda pin: self.button_pressed(1, key1_action, close_action), bouncetime=200)
        GPIO.add_event_detect(key2, GPIO.FALLING, callback=lambda pin: self.button_pressed(2, key2_action, close_action), bouncetime=200)
        GPIO.add_event_detect(key3, GPIO.FALLING, callback=lambda pin: self.button_pressed(3, key3_action, close_action), bouncetime=200)
        GPIO.add_event_detect(key4, GPIO.FALLING, callback=lambda pin: self.button_pressed(4, key4.action, close_action), bouncetime=200)


    def set_busy(self):
        self.action_in_progress = True


    def set_not_busy(self):
        self.action_in_progress = False


    def busy(self):
        return self.action_in_progress


    def button_pressed(self, buttonNo, open_action, close_action):
        if self.busy():
            logging.info("Button #{} ignored".format(buttonNo))
            return
        try:
            self.set_busy()
            logging.info("Button #{} pressed".format(buttonNo))
            open_action()
        finally:
            logging.info("Finishing button key press handling")
            close_action()

