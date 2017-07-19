#!/usr/bin/python

import time # For heartBeat timing
import uuid # For IDing the Strips
import os # For Environmental Vars
import random # for random testing

import sys # For args from node_server

from PIL import Image
from dotstar import Adafruit_DotStar


class LEDStrand:
    def __init__(self, totalLEDs, data_pin, clock_pin, gammaCorrect_bool=False):
        self.uuid = str(uuid.uuid4())
        self.totalLEDs = totalLEDs
        self.data_pin = data_pin
        self.clock_pin = clock_pin
        self.stripCtrl = Adafruit_DotStar(self.totalLEDs, self.data_pin, self.clock_pin)

        self.playHead = 0
        self.endTail = -self.totalLEDs  + 1

        self.defaultColor = 0xFF0000

        self.matrices = []

        image = Image.open('./node_server/images/60x_fading_stripes.png').convert("RGB")
        self.matrix = image.load()
        self.width, self.height = image.size
        self.pulse = []

        self.stripCtrl.begin()
        self.stripCtrl.setBrightness(10)
        self.gammaCorrect_bool = gammaCorrect_bool

        self.gamma = bytearray(256)
        for gamma_index in range(256):
        	self.gamma[gamma_index] = int(pow(float(gamma_index) / 255.0, 2.7) * 255.0 + 0.5)

    def gammaCorrect(self, color_rgb):
        r,g,b = color_rgb

        r = self.gamma[r]
        g = self.gamma[g]
        b = self.gamma[b]

        return (r, g, b)


    def setColor(self, color_rgba, gammaCorrect_bool):

        self.gammaCorrect_bool = gammaCorrect_bool

        # Color Correct if set to true
        r,g,b,a = color_rgba
        if(self.gammaCorrect_bool): r, g, b = self.gammaCorrect((r, g, b))


        for led_index in range(self.totalLEDs):
            self.stripCtrl.setPixelColor(led_index, g, r, b) # Gamma correction for mid-range colors
        self.stripCtrl.setBrightness(a)
        self.playHead = 0 # Reset playhead to 0

        self.stripCtrl.show() # Execute changes

        return self

    def clear(self, show=True):
        self.stripCtrl.clear() # Clears buffer for strip, does not write to strip
        if(show): self.stripCtrl.show() # writes clear to strip if supplied
        return self

    def stepHead(self):
        for led_index in range(self.totalLEDs):
            if(led_index < self.width):

                # Pull Pixel info from matix
                r,g,b = self.matrix[led_index, self.playHead]

                #  Color correct if specified
                if(self.gammaCorrect_bool): color_rgba = self.gammaCorrect((r, g, b))

                # Set Buffer for this LED
                self.stripCtrl.setPixelColor(led_index, g, r, b)

        self.stripCtrl.show() # Refresh the strip

        self.playHead += 1
        if(self.playHead >= self.height):
            self.playHead = 0
        return self

    def heartBeat(self):
        "Autonomic functions get called here on the reg"
        if(self.pulse):
            for pulseService in self.pulse:
                pulseService()
    def addToPulse(self, callback):
        self.pulse.append(callback)


strips = []

fps = 60

# strips.append(LEDStrand(30, 19, 26))
strips.append(LEDStrand(30, 20, 21))


demoType = 'heartBeat'
print(demoType)
sys.stdout.flush()
# Register a service to execute on heartBeat
strips[0].addToPulse(strips[0].stepHead)
strips[1].addToPulse(strips[1].stepHead)


#
# while True:
#     for strip in strips:
#         strip.stepHead()
#     time.sleep(1.0 / fps)

if(demoType == 'set'):
    # Set Color of whole Strip
    strips[0].setColor((random.getrandbits(8), random.getrandbits(8), random.getrandbits(8), 100), True)
    strips[1].setColor((random.getrandbits(8), random.getrandbits(8), random.getrandbits(8), 100), False)

# Turn LEDs off for strips[n]
# strips[0].clear()
# strips[1].clear()

if(demoType == 'heartBeat'):
    while True:
        # print("==== Heart Beat ====")
        for strip in strips:
            # print(strip.uuid[0 : 5])
            strip.heartBeat()
        time.sleep(1.0 / fps)
