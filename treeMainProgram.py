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

stripflaresize = 12

colors = [
    [255,0,0],
    [255,255,0],
    [0,128,255],
    [255,0,128],
    [128,255,0],
    [0,0,255],
    [255,128,0],
    [128,0,255],
    [0,255,255],
    [0,255,0]
]

colorschemes = {}
for idx, scheme in enumerate(colors):
    colorschemes[idx] = colors[idx]

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

    def getColors(self):
        return self.color

class stringflare:

    pixid = 0
    mycolorschemes = {}
    state = 0
    maxstate = 0
    pixcolor = [0,0,0]
    inc = 1

    def __init__( self, myid=0, brightness=1 ):
        global colors
        self.brightness = brightness
        self.pixid = myid
        mycolors = []
        mycolors.append([0,0,0])
        mycolors.append([0,0,0])
        mycolors.extend( colors )
        mycolors.append([255,255,255])
        for idx, scheme in enumerate(mycolors):
            self.mycolorschemes[idx] = mycolors[idx]
        
    def getId(self):
        return self.pixid

    def getColors(self):
        if self.state == self.maxstate:
            self.inc = -1
        self.state = self.state + self.inc
        if self.state <= 0:
            nc = random.randrange( len(self.mycolorschemes.keys()) )
            self.pixcolor = self.mycolorschemes[nc]
            self.maxstate = 0
            if nc > 1: self.maxstate = 10
        if self.maxstate > 0:
            pct = nc/self.maxstate
        else:
            pct = 0
        return [ int(x*pct*self.brightness) for x in self.pixcolor ]



        return self.color

if __name__ == '__main__':

    strip = Adafruit_NeoPixel(LED_STRIP_COUNT, LED_STRIP_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_STRIP_CHANNEL)
    strip.begin()
    string = Adafruit_NeoPixel(LED_STRING_COUNT, LED_STRING_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_STRING_CHANNEL)
    string.begin()

    stringshow = {}
    stringflares = []
    for i in range(int(LED_STRING_COUNT)):
        stringflares.append(stringflare(myid=i))

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
        lpixid = lflare.getId()
        lcolors = lflare.getColors()
        stringshow[lpixid]=lcolors

    for lflare in stripflares:
        lcolors = lflare.getColors()
        for pixel in lcolors.keys():
            stripshow[pixel]=lcolors[pixel]

    i = 0
    while True:
        for lflare in stringflares:
            lpixid = lflare.getId()
            lcolors = lflare.getColors()
            stringshow[lpixid]=lcolors
        step = {}
        print(json.dumps(stringshow[0]))
        for pixel in stringshow.keys():
            string.setPixelColor((pixel+i)%LED_STRING_COUNT, Color(stringshow[pixel][0],stringshow[pixel][1],stringshow[pixel][2]))
        for pixel in stripshow.keys():
            strip.setPixelColor((pixel+i)%LED_STRIP_COUNT, Color(stripshow[pixel][0],stripshow[pixel][1],stripshow[pixel][2]))
        string.show()
        strip.show()

        i=(i+1)%LED_STRING_COUNT
        time.sleep(1)           