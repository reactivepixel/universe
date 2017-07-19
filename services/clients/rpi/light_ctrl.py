# Mqtt
import paho.mqtt.client as mqtt
import subprocess
import json

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
        p = subprocess.call('sudo python ./py_ctrl/clear.py', shell=True)
    elif(payload['action'] == 'test'):
        p = subprocess.call('sudo python ./py_ctrl/test.py', shell=True)
        os.killpg(os.getpgid(pro.pid), signal.SIGTERM)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.0.11", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
