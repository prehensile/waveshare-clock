# https://github.com/pskowronek/epaper-clock-and-more, Apache 2 license

import logging
import RPi.GPIO as GPIO


class Buttons(object):


    def __init__(self, epaper, key1, key2, key3, key4):
        self.epaper = epaper
        self.key1 = key1
        self.key2 = key2
        self.key3 = key3
        self.key4 = key4
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


