import time # For heartBeat timing
import uuid # For IDing the Strips

class Timeline:
    def __init__(self, timeDelay=0.015):
        self.uuid = str(uuid.uuid4())

        # Floating Point rate. FPS
        self.timeDelay = timeDelay # 1sec / 60 frames
        self.looping = True
        self.playing = False
        self.onLoadNextFrameCmds = []
        self.onPlayFrameCmds = []

    def runFrameLoop(self):
        while self.looping:
            self.loadNextFrame()
            self.enterFrame()
            self.playFrame()
            self.leaveFrame()
            time.sleep(self.timeDelay)
        return self


    def loadNextFrame(self):
        return self

    def enterFrame(self):
        self.playFrame()
        return self

    def playFrame(self):
        if self.playing:
            # print('Total Play Cmds', self.onPlayFrameCmds)
            for cmd in self.onPlayFrameCmds:
                cmd()
        return self

    def leaveFrame(self):
        return self

    def play(self):
        self.playing = True
        return self

    def pause(self):
        self.playing = False
        return True

    def registerOnLoadNextFrameCommand(self, cmd):
        self.onLoadNextFrameCmds.append(cmd)
        return True

    def registerOnPlayCommand(self, cmd):
        self.onPlayFrameCmds.append(cmd)
        return True

    def clearOnPlayCommands(self):
        self.onPlayFrameCmds = []



    def getInfo(self):
        return {
            'uuid': self.uuid,
            'timeDelay': self.timeDelay,
            'playing': self.playing,
            'onPlayFrameCmds': self.onPlayFrameCmds
            }
