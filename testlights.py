#!/usr/bin/env python3
# rpi_ws281x library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

import time
from rpi_ws281x import *
import random

# LED strip configuration:
LED_STRING_COUNT = 700
LED_STRIP_COUNT = 600
LED_STRING_PIN  = 18     # GPIO pin connected to the pixels (18 uses PWM!).
LED_STRIP_PIN = 19
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 180     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_STRING_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP_CHANNEL = 1
NUM_PER_SEC = 4

def colorWipe(strip, color, wait_ms=10):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()
        #time.sleep(wait_ms/1000.0)

if __name__ == '__main__':

    strip = Adafruit_NeoPixel(LED_STRIP_COUNT, LED_STRIP_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_STRIP_CHANNEL)
    strip.begin()
    string = Adafruit_NeoPixel(LED_STRING_COUNT, LED_STRING_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_STRING_CHANNEL)
    string.begin()

    colorschemes = {
        0: [255,0,0],
        1: [0,255,0],
        2: [0,0,255],
        3: [255,255,0],
        4: [0,255,255],
        5: [255,0,255],
        6: [255,255,255]
    }

    while True:
        i = random.randrange(7)
        i = 5
        colorWipe(strip, Color(colorschemes[i][0], colorschemes[i][1], colorschemes[i][2]))  # Red wipe
        colorWipe(string, Color(colorschemes[i][0], colorschemes[i][1], colorschemes[i][2]))  # Red wipe
        time.sleep(1)
        #colorWipe(strip, Color(0, 255, 0))  # Blue wipe
        #colorWipe(strip, Color(0, 0, 255))  # Green wipe
