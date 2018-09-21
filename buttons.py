# https://github.com/pskowronek/epaper-clock-and-more, Apache 2 license

import logging
import os
import RPi.GPIO as GPIO


class Buttons(object):

    key1 = int(os.environ.get("EPAPER_GPIO_PIN_FOR_KEY1", "5"))
    key2 = int(os.environ.get("EPAPER_GPIO_PIN_FOR_KEY2", "6"))
    key3 = int(os.environ.get("EPAPER_GPIO_PIN_FOR_KEY3", "13"))
    key4 = int(os.environ.get("EPAPER_GPIO_PIN_FOR_KEY4", "19"))


    def __init__(self, epaper):
        self.epaper = epaper
        self.register()


    def register(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.key1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.key2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.key3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.key4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.add_event_detect(self.key1, GPIO.FALLING, callback=self.button1_pressed, bouncetime=200)
        GPIO.add_event_detect(self.key2, GPIO.FALLING, callback=self.button2_pressed, bouncetime=200)
        GPIO.add_event_detect(self.key3, GPIO.FALLING, callback=self.button3_pressed, bouncetime=200)
        GPIO.add_event_detect(self.key4, GPIO.FALLING, callback=self.button4_pressed, bouncetime=200)

    
    def button1_pressed(self, pin):
        logging.info("Button #1 pressed")
        self.epaper.display_gmaps_details()
                   

    def button2_pressed(self, pin):
        logging.info("Button #2 pressed")
        self.epaper.display_airly_details()


    def button3_pressed(self, pin):
        logging.info("Button #3 pressed")
        self.epaper.display_weather_details()


    def button4_pressed(self, pin):
        logging.info("Button #4 pressed")
        self.epaper.display_system_details()


