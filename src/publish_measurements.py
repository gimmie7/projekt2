import argparse
import paho.mqtt.client as mqtt
import json
import time
from em340.em340 import Em340
from em340.measurement import Measurement
from helper.scheduler import PeriodicScheduler

# Settings and default values
port = 'COM4' # serial port
interval = 15 # in seconds
siot_center_url = 'siot.net'
siot_center_port = 1883
parser = argparse.ArgumentParser()
parser.add_argument("--p", help="serial port where your modbus device is plugged in, e.g. COM4 on Windows or /dev/ttyUSB0 on Linux")
parser.add_argument("--i", help="interval in seconds for publishing data to siot center", type=float)
args = parser.parse_args()

if args.p:
    port = args.p
if args.i:
    interval = args.i

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print('on message: ' + msg.topic + ' ' + str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(siot_center_url, siot_center_port)

# em340
em340 = Em340(port)
print('run script with the following settings: port={0}, intervall in sec={1}, siot center url={2}, siot center port={3}'
.format(port, interval, siot_center_url, siot_center_url))

def publish():
    '''
    read data from em340 and publish the data to the siot center
    '''
    measurement = em340.read_phase1()
    payload = {
        "ts": int(time.time()),
        "p": measurement.p,
        "s": measurement.s,
        "q": measurement.q,
        "i": measurement.i
    }
    payload_out = json.dumps(payload)

    try:
        client.publish('siot/DAT/AF3A-CFE9-B0F7-01A1-349D-FB34-2F3B-96E9/9ea93a6d-797c-7621-a9b5-ce3704718093', payload_out)
        print(payload_out)
    except:
        print('publish of message {} failed'.format(payload_out))

periodic_scheduler = PeriodicScheduler()  
periodic_scheduler.setup(interval, publish) # it executes the event just once  
periodic_scheduler.run() # starts the scheduler  
