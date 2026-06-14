import paho.mqtt.client as mqtt
import time
import random
import json

client = mqtt.Client()
client.connect("broker.hivemq.com", 1883)

while True:
    data = {
        "bin_id": 1,
        "fill": random.randint(10, 100)
    }

    client.publish("smartbin/data", json.dumps(data))
    print("Sent:", data)

    time.sleep(3)