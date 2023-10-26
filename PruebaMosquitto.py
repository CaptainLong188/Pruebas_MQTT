import time 
import random
import paho.mqtt.client as mqtt

hostname = "localhost"
broker_port = 1883
topic = "testTopic"

# Create a new MQTT client 
client = mqtt.Client()

# MQTT Callback functions
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.on_connect = on_connect


def on_message(client, userdata, msg):
    print(f"Received message '{msg.payload}' on topic '{msg.topic}'")

client.on_message = on_message

# Connect to MQTT broker
client.connect(hostname, broker_port)

# Generating random numbers as payload
while True: 
    message = str(random.randint(1, 100))
    result = client.publish(topic, message)
    status = result[0]

    if status == 0:
        print(f"Send {message} to topic {topic}")
    else:
        print(f"Failed to send message to topic {topic}")
    time.sleep(2)