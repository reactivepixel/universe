from AnimationCtrl.timeline import Timeline
from LEDs.ctrl import Ctrl
import paho.mqtt.client as mqtt
import json

# green 20, yellow 21
# Purple 26, Blue 19

# TODO investigate why 59 works but 60 doesnt
stripsInfo = [{'ledTotal': 30,'data_pin': 20, 'clock_pin': 21}, {'ledTotal': 59,'data_pin': 26, 'clock_pin': 19}]

timeline = Timeline()

ctrl = Ctrl(stripsInfo)

# Clear on Client Start
ctrl.clearAndPause(timeline)

#  Auto test
ctrl.renderImageAsAnimation(timeline)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("lobby")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    payload = json.loads(msg.payload)

    if(payload['action'] == 'clear'):
        # p = subprocess.call('sudo python ./py_ctrl/clear.py', shell=True)
        print('==== Detected ===== Clear')
        # clearAll
        ctrl.clearAndPause(timeline)

    elif(payload['action'] == 'test'):
        print('==== Detected ===== Test')
        # ctrl.clearBufferAll(timeline)
        # Render Test Image
        ctrl.renderImageAsAnimation(timeline)

    elif(payload['action'] == 'info'):
        print('==== Detected ===== Info')
        print(timeline.getInfo())
        # p = subprocess.call('sudo python ./py_ctrl/test.py', shell=True)
        # os.killpg(os.getpgid(pro.pid), signal.SIGTERM)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("Chapman-MBP.local", 1883, 60)

# Start MQTT Client
client.loop_start()

# Start the Infiniate Timeline Loop
print(timeline.getInfo())
timeline.runFrameLoop()
