# https://github.com/pskowronek/epaper-clock-and-more, Apache 2 license

import logging
import os
import RPi.GPIO as GPIO


class Buttons(object):

    key1 = int(os.environ.get("EPAPER_GPIO_PIN_FOR_KEY1", "3"))
    key2 = int(os.environ.get("EPAPER_GPIO_PIN_FOR_KEY2", "6"))
    key3 = int(os.environ.get("EPAPER_GPIO_PIN_FOR_KEY3", "13"))
    key4 = int(os.environ.get("EPAPER_GPIO_PIN_FOR_KEY4", "19"))


    def __init__(self, clock):
        self.clock = clock
        self.register()


    def register(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(key1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(key2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(key3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(key4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.add_event_detect(key1, GPIO.FALLING, callback=button1_pressed, bouncetime=200)
        GPIO.add_event_detect(key2, GPIO.FALLING, callback=button2_pressed, bouncetime=200)
        GPIO.add_event_detect(key3, GPIO.FALLING, callback=button3_pressed, bouncetime=200)
        GPIO.add_event_detect(key4, GPIO.FALLING, callback=button4_pressed, bouncetime=200)

    
    def button1_pressed(self):
        logging.info("Button #1 pressed")


    def button2_pressed(self):
        logging.info("Button #2 pressed")


    def button3_pressed(self):
        logging.info("Button #3 pressed")


    def button4_pressed(self):
        logging.info("Button #4 pressed")


