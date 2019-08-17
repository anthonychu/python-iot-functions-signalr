from dotenv import load_dotenv
load_dotenv()

from datetime import datetime
import json
import os
import ssl
import sys
import time

import paho.mqtt.client as mqtt

from config import Config
from iothub import IotHub
from sensor import SensorSimulator

connection_string = os.getenv('CONNECTION_STRING')

if connection_string == '':
    print("Missing Connection String")
    sys.exit(1)

config = Config(connection_string)
iot = IotHub(config.hub_address, config.device_id, config.shared_access_key)
sensor = SensorSimulator()

sample_rate_in_seconds = 0.5


def on_connect(client, userdata, flags, rc):
    print("Connected with result code: %s" % rc)
    client.subscribe(iot.hub_topic_subscribe)


def on_disconnect(client, userdata, rc):
    print("Disconnected with result code: %s" % rc)
    client.username_pw_set(iot.hub_user, iot.generate_sas_token(
        iot.endpoint, iot.shared_access_key))


def on_message(client, userdata, msg):
    print("Message received: %s" % msg)


def on_publish(client, userdata, mid):
    print("Message {0} sent from {1} at {2}".format(
        str(mid), config.device_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))


def publish():
    while True:
        try:
            reading = sensor.read()
            msg = json.dumps(reading)
            client.publish(iot.hub_topic_publish, msg)
            time.sleep(sample_rate_in_seconds)
        except KeyboardInterrupt:
            print("IoTHubClient sample stopped")
            return
        except:
            print("Unexpected error")
            time.sleep(4)


client = mqtt.Client(config.device_id, mqtt.MQTTv311)

client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.on_publish = on_publish

client.username_pw_set(iot.hub_user, iot.generate_sas_token())
client.tls_set()
client.connect(config.hub_address, 8883)

client.loop_start()

publish()