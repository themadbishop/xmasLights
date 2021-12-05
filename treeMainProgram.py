#!/usr/bin/env python3
# rpi_ws281x library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

import time
from rpi_ws281x import *
import random
import json

# LED strip configuration:
LED_STRING_COUNT = 700
LED_STRIP_COUNT = 24
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

stripflaresize = 12

class stripflare:

    fid = 0
    color = {}

    def __init__( self, myid=0, mycolor=[0,0,0], brightness=1 ):
        global stripflaresize
        #self.id = myid * 10
        self.color[myid*stripflaresize + (stripflaresize-1)] = [ int(x*1*brightness) for x in [255,255,255] ]
        for g in range( stripflaresize - 3 ):
            pct = g/( stripflaresize - 3 ) 
            self.color[myid*stripflaresize+g+2] = [ int(x*pct*brightness) for x in mycolor ]
        self.color[myid*stripflaresize+1] = [0,0,0]
        self.color[myid*stripflaresize] = [0,0,0]
        print(json.dumps(self.color,indent=2))

    def getColors(self):
        return self.color

class stringflare:

    fid = 0
    color = {}

    def __init__( self, myid=0, mycolor=[0,0,0], brightness=1 ):
        #self.id = myid * 10
        self.color[myid*10+9] = [ int(x*1) for x in [255,255,255] ]
        self.color[myid*10+8] = [ int(x*1) for x in mycolor]
        self.color[myid*10+7] = [ int(x*1) for x in mycolor]
        self.color[myid*10+6] = [ int(x*.8) for x in mycolor]
        self.color[myid*10+5] = [ int(x*.6) for x in mycolor]
        self.color[myid*10+4] = [ int(x*.4) for x in mycolor]
        self.color[myid*10+3] = [ int(x*.2) for x in mycolor]
        self.color[myid*10+2] = [ int(x*.1) for x in mycolor]
        self.color[myid*10+1] = [ int(x*0) for x in mycolor]
        self.color[myid*10] = [0,0,0]

    def getColors(self):
        return self.color

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

    stringshow = {}
    stringflares = []
    for i in range(int(LED_STRING_COUNT/10)):
        stringflares.append(stringflare(myid=i,mycolor=colorschemes[i%len(colorschemes.keys())]))

    stripshow = {}
    stripflares = []
    for i in range(int(LED_STRIP_COUNT/stripflaresize)):
        stripflares.append(stripflare(myid=i,mycolor=colorschemes[i%len(colorschemes.keys())]))
    #lightflares.append(flare(myid=0,mycolor=[255,0,0]))
    #lightflares.append(flare(myid=1,mycolor=[0,255,0]))
    #lightflares.append(flare(myid=2,mycolor=[0,0,255]))
    #lightflares.append(flare(myid=3,mycolor=[255,255,0]))
    #lightflares.append(flare(myid=4,mycolor=[0,255,255]))
    
    for lflare in stringflares:
        lcolors = lflare.getColors()
        for pixel in lcolors.keys():
            stringshow[pixel]=lcolors[pixel]

    for lflare in stripflares:
        lcolors = lflare.getColors()
        for pixel in lcolors.keys():
            stripshow[pixel]=lcolors[pixel]

    i = 0
    while True:
        step = {}
        for pixel in stringshow.keys():
            string.setPixelColor((pixel+i)%LED_STRING_COUNT, Color(stringshow[pixel][0],stringshow[pixel][1],stringshow[pixel][2]))
        for pixel in stripshow.keys():
            strip.setPixelColor((pixel+i)%LED_STRIP_COUNT, Color(stripshow[pixel][0],stripshow[pixel][1],stripshow[pixel][2]))
        string.show()
        strip.show()

        i=(i+1)%LED_STRING_COUNT
        time.sleep(.1)           