from strip import LEDStrip

class Ctrl:
    def __init__(self, stripsInfo):
        self.stripsInfo = stripsInfo
        self.strips = []

        for stripInfo in stripsInfo:
            strip = {}
            strip['info'] = stripInfo
            strip['data_pin'] = stripInfo['data_pin']
            strip['clock_pin'] = stripInfo['clock_pin']
            strip['ledTotal'] = stripInfo['ledTotal']
            strip['instance'] = self.initStrip(strip)
            self.strips.append(strip)

    def initStrip(self, strip):
        instance = LEDStrip(['g', 'r', 'b'], strip['ledTotal'], strip['data_pin'], strip['clock_pin'])
        instance.initStripGPIO()
        return instance

    def renderImageAsAnimation(self, timelineInstance, imgSrc='images/60x_24bit_color_test_pattern_rainbow.png', loadAll=True):

        if loadAll:
            for strip in self.strips:
                imageMatrixIndex, imageMatrix = strip['instance'].genImageMatrix(imgSrc);
                strip['instance'].setCurrentMatrix(imageMatrixIndex)
                timelineInstance.registerOnPlayCommand(strip['instance'].renderNextAssignments)
        timelineInstance.playing = True

    def clearBufferAll(self):
        for strip in self.strips:
            strip['instance'].clear()

    def clearAndPause(self, timelineInstance):
        self.clearBufferAll()
        # timelineInstance.pause()
