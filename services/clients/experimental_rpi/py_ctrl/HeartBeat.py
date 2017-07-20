import time # For heartBeat timing
import uuid # For IDing the Strips

class HeartBeat:
    def __init__(self, rate):
        self.uuid = str(uuid.uuid4())

        # Floating Point rate. FPS
        self.rate = rate

        self.pulse = False

        self.registeredCommands = []

    def preBeat(self):
        return self

    def beat(self):
        # print 'lub'
        self.preBeat()


        for cmd in self.registeredCommands:
            cmd()

        self.postBeat()
        # print 'dub'
        return self

    def postBeat(self):
        return self

    def startHeart(self):
        self.pulse = True
        while self.pulse:
            self.beat()
            time.sleep(self.rate)

    def stopHeart(self):
        self.pulse = False
        return True

    def registerCommand(self, cmd):
        self.registeredCommands.append(cmd)
        return True
