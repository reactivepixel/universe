# Load Cust module
from sys import path
path.append('./py_ctrl')
from LEDStrip import LEDStrip
from HeartBeat import HeartBeat

# Mqtt
import paho.mqtt.client as mqtt

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


heart.startHeart()



# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("lobby")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    strip.clear()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
