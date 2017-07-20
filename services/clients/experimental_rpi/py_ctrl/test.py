import time
from LEDStrip import LEDStrip
from HeartBeat import HeartBeat

runOnPi = True

fps = 0.017 # 1sec / 60 frames
stripPixels = 30
data_pin = 20
clock_pin = 21

# Strip Config
strip = LEDStrip(['g', 'r', 'b'], stripPixels, data_pin, clock_pin)

if runOnPi:
    strip.initStripGPIO()

# matrixIndex, matrix = strip.genMatrix(stripPixels, 500)
imageMatrixIndex, imageMatrix = strip.genImageMatrix('./server/images/60x_24bit_color_test_pattern_rainbow.png');

# print imageMatrix[29,1]

strip.setCurrentMatrix(imageMatrixIndex)

# HeartBeat
heart = HeartBeat(fps)
if runOnPi:
    heart.registerCommand(strip.idleStep)



#
# for x in range(10):
#     print assignment[0]
#     strip.bounceHead()
#


# print imageMatrix[0]
heart.startHeart()

print('Locked and Loaded')
