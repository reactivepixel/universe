# Mqtt
import paho.mqtt.client as mqtt
import subprocess
import json
import time

import os
import signal

# The callback for when the client receives a CONNACK response from the server.
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
    elif(payload['action'] == 'test'):
        print('==== Detected ===== Test')
        # p = subprocess.call('sudo python ./py_ctrl/test.py', shell=True)
        # os.killpg(os.getpgid(pro.pid), signal.SIGTERM)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

# while True:
#     time.sleep(self.rate)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
# client.loop_forever()
client.loop_start()
