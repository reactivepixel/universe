#!/usr/bin/python

import time
import math
import uuid
from dotstar import Adafruit_DotStar


class LEDStrand:
    def __init__(self, totalLEDs, data_pin, clock_pin):
        self.uuid = str(uuid.uuid4())
        self.totalLEDs = totalLEDs
        self.data_pin = data_pin
        self.clock_pin = clock_pin
        self.stripCtrl = Adafruit_DotStar(self.totalLEDs, self.data_pin, self.clock_pin)

        self.playHead = 0
        self.endTail = -self.totalLEDs  + 1

        self.defaultColor = 0xFF0000

        self.pulse = []

        self.stripCtrl.begin()
        self.stripCtrl.setBrightness(64)

    def setColor(self, color_rgba):
        red_channel = color_rgba[0]
        green_channel = color_rgba[1]
        blue_channel = color_rgba[2]
        alpha_channel = color_rgba[3]

        for led_index in range(0, self.totalLEDs):
            self.stripCtrl.setPixelColor(led_index, green_channel, red_channel, blue_channel)
        self.stripCtrl.setBrightness(alpha_channel)
        self.playHead = 0 # Reset playhead to 0

        self.stripCtrl.show() # Execute changes

        return self

    def clear(self, show=True):
        self.stripCtrl.clear() # Clears buffer for strip, does not write to strip
        if(show): self.stripCtrl.show() # writes clear to strip if supplied
        return self

    def stepHead(self):
        # self.stripCtrl.setPixelColor(self.playHead, self.defaultColor)
        self.stripCtrl.setPixelColor(self.playHead, 31, 31, 31)
        self.stripCtrl.setPixelColor(self.endTail, 0)
        self.stripCtrl.show() # Refresh the strip

        self.playHead += 1
        if(self.playHead >= self.totalLEDs):
            self.playHead = 0
            self.defaultColor >>= 8
            if(self.defaultColor == 0): self.defaultColor = 0xFF0000
        self.endTail += 1
        if(self.endTail >= self.totalLEDs): self.endTail = 0
        return self

    def heartBeat(self):
        "Autonomic functions get called here on the reg"
        if(self.pulse):
            for pulseService in self.pulse:
                pulseService()
    def addToPulse(self, callback):
        self.pulse.append(callback)


strips = []

fps = 10

strips.append(LEDStrand(30, 19, 26))
strips.append(LEDStrand(60, 20, 21))


strips[0].clear()
strips[1].clear()
