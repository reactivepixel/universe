from AnimationCtrl.timeline import Timeline
from LEDs.strip import LEDStrip
import paho.mqtt.client as mqtt
import json

#############
# Config

fps = 0.017 # 1sec / 60 frames
stripPixels = 30
data_pin = 20
clock_pin = 21

timeline = Timeline()

# Strip Config
strip = LEDStrip(['g', 'r', 'b'], stripPixels, data_pin, clock_pin)
strip.initStripGPIO()

imageMatrixIndex, imageMatrix = strip.genImageMatrix('images/60x_24bit_color_test_pattern_rainbow.png');
strip.setCurrentMatrix(imageMatrixIndex)
timeline.registerOnPlayCommand(strip.idleStep)

def callback():
    print('Who calls the callbacks?')


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("lobby")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    payload = json.loads(msg.payload)

    if(payload['action'] == 'clear'):
        # p = subprocess.call('sudo python ./py_ctrl/clear.py', shell=True)
        print('==== Detected ===== Clear')
        strip.clear()
        timeline.pause()
    elif(payload['action'] == 'test'):
        print('==== Detected ===== Test')
        timeline.play()
    elif(payload['action'] == 'info'):
        print('==== Detected ===== Info')
        print(timeline.getInfo())
        # p = subprocess.call('sudo python ./py_ctrl/test.py', shell=True)
        # os.killpg(os.getpgid(pro.pid), signal.SIGTERM)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("Chapman-MBP.local", 1883, 60)

# while True:
#     time.sleep(self.rate)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
# client.loop_forever()
client.loop_start()

print(timeline.getInfo())


timeline.registerOnPlayCommand(callback)
timeline.runFrameLoop()
