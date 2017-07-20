import math
import time # For heartBeat timing
import uuid # For IDing the Strips
import os # For Environmental Vars
import random # for random testing

import sys # For args from node_server

from PIL import Image
from dotstar import Adafruit_DotStar

class LEDStrip:
    def __init__(self, sequence, pixels, data_pin, clock_pin, doGammaCorrect=False):
        # Generate ID for Strip
        self.uuid = str(uuid.uuid4())

        # Total LEDs
        self.pixels = pixels

        # playHead
        self.head = 0

        # Play history
        self.headHistory = [0]

        # LoadedMatrixIndex
        self.currentMatrixIndex = 0
        self.currentMatrix = {}

        self.currentMatrixHeight = 0

        # Tracking of direction of bounce head
        self.bounceHeadForward = True

        # Pin locations for data transmission
        self.data_pin = data_pin
        self.clock_pin = clock_pin

        # Instantiate the Adafruit class to control the strip
        self.ctrl = {}


        # Dotstars have a default sequence of
        self.sequence = sequence or ['r', 'g', 'b']

        # Prepwork for Gamma Correction
        self.doGammaCorrect = doGammaCorrect

        self.gamma = bytearray(256)
        for gamma_index in range(256):
        	self.gamma[gamma_index] = int(pow(float(gamma_index) / 255.0, 2.7) * 255.0 + 0.5)

        # Matrices
        self.matrices = []

    def initStripGPIO(self):
        self.ctrl = Adafruit_DotStar(self.pixels, self.data_pin, self.clock_pin)
        self.ctrl.begin()

    def setColor(self, rgba):
        # Split out color into its respective vars
        r,g,b,a = rgba

        # If Gamma Correcting, do the correction
        if(self.doGammaCorrect): r, g, b = self.gammaCorrect((r, g, b))

        for led_index in range(self.pixels):
            self.ctrl.setPixelColor(led_index, g, r, b) # Gamma correction for mid-range colors
        self.ctrl.setBrightness(a)
        self.playHead = 0 # Reset playhead to 0

        self.ctrl.show() # Execute changes

        return self

    def gammaCorrect(self, rgb):
        r,g,b = rgb

        r = self.gamma[r]
        g = self.gamma[g]
        b = self.gamma[b]

        return (r, g, b)

    def clear(self, show=True):
        # Clears buffer for strip, does not write to strip
        self.ctrl.clear()

        # writes clear to strip if supplied
        self.ctrl.show()
        return self

    def genMatrix(self, width=10, height=10, doStaticAlpha=True):
        if(width != self.pixels):
            print('Error: Matrix will not match total pixels.')
            return False

        # Init the matrix that will be filled and 'saved'
        matrix = {}

        # Rand gen value max
        maxValue = 255

        # Generate a matrix for the height and width prefilled with content
        for y in range(0, height):
            for x in range(0, width):

                # Red, Green, Blue Generation
                genR = random.randrange(maxValue)
                genG = random.randrange(maxValue)
                genB = random.randrange(maxValue)

                # Alpha Generation
                if (doStaticAlpha):
                    alphaValue = maxValue
                else:
                    alphaValue = random.randrange(maxValue)

                matrix[x,y] = (genR, genG, genB, alphaValue)

        return self.addMatrix(matrix)

    def genImageMatrix(self, imgPath):
        img = Image.open(imgPath).convert("RGBA")

        matrix = img.load()
        avgMatrix = {}
        # TODO Refactor the self.matrix vars to be an object
        w, self.currentMatrixHeight = img.size

        # Image is larger than what the strip can nativly handle
        if w > self.pixels:
            stepWidth = int(math.floor(w / self.pixels)) #
            for y in range(self.currentMatrixHeight):
                ctnCount = 0
                adjustedX = 0
                for x in range(self.pixels):
                    adjustedX = x * stepWidth

                    r,g,b,a = (0, 0, 0, 0)
                    for step in range(stepWidth):
                        R, G, B, A = matrix[adjustedX + step, y]
                        r += R
                        g += G
                        b += B
                        a += A

                    avgR, avgG, avgB, avgA = (r/stepWidth, g/stepWidth, b/stepWidth, a/stepWidth)

                    # Add averaged pixels to the matrix
                    avgMatrix[x,y] = (avgR, avgG, avgB, avgA)

        return self.addMatrix(avgMatrix)

    def addMatrix(self, matrix):
        # Determine the index of the new matrix
        matrixIndex = len(self.matrices)
        self.matrices.append(matrix)

        # Returns (index, matrix) to generators
        return (matrixIndex, self.matrices[matrixIndex])

    def advanceHead(self, bounce=False):
        self.head += 1
        if bounce == False and self.head >= self.currentMatrixHeight:
            self.head = 0

            # Record Head Movement
            self.setHeadHistory()


        return self.head

    def reverseHead(self, bounce=False):
        self.head -= 1
        if bounce == False and self.head < 0:
            self.head = self.currentMatrixHeight

            # Record Head Movement
            self.setHeadHistory()

        return self.head

    def bounceHead(self):
        if self.bounceHeadForward:
            self.advanceHead(True)
            if self.head >= self.currentMatrixHeight:
                self.head = self.currentMatrixHeight
                self.bounceHeadForward = False
                self.reverseHead()
        else:
            self.reverseHead(True)
            if self.head < 0:
                self.head = 0
                self.bounceHeadForward = True
                self.advanceHead()

        # Record Head Movement
        self.setHeadHistory()

        return self.head

    def setCurrentMatrix(self, index):
        self.currentMatrix = self.matrices[index]
        self.currentMatrixIndex = index

        return self.currentMatrix

    def getCurrentMatrix(self):
        return self.currentMatrix

    def getCurrentMatrixIndex(self):
        return self.currentMatrixIndex

    def getCurrentStripAssignment(self):
        subMatrix = {}
        for x in range(self.pixels):
            y = self.head
            subMatrix[x] = self.currentMatrix[x, y]

        return subMatrix

    def getNextStripAssignment(self):
        return False

    def getHeadHistory(self):
        return self.headHistory

    def setHeadHistory(self):
        # Add the current loc of the play head to the beginning of the history array
        self.headHistory.insert(0, self.head)
        return True

    def renderNextAssignments(self):
        assignments = self.getCurrentStripAssignment()
        self.renderStrip(assignments)
        self.bounceHead()

    def renderStrip(self, assignments):

        if(self.doGammaCorrect): r, g, b = self.gammaCorrect((r, g, b))

        for pixelIndex in assignments:
            print pixelIndex
            r,g,b,a = assignments[pixelIndex]

            # TODO setup RGB vs GRB Assignments dynamically
            self.ctrl.setPixelColor(pixelIndex, g, r, b)

        self.ctrl.setBrightness(a)
        self.ctrl.show()
