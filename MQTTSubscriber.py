import time 
import paho.mqtt.client as mqtt
import random

broker = "localhost"
topic = "sensor/nivel_de_agua"

def connect_mqtt():

    client = mqtt.Client("PruebaSubscriberMQTT")

    @client.connect_callback()
    def on_connect(client, userdata, flags, rc):
        print(f"{mqtt.connack_string(rc)}")

    @client.log_callback()
    def on_log(client, userdata, level, buf):
        print(f"Log : {buf}")

    @client.message_callback()
    def on_message(client, userdata, msg):
        print(f"Received {msg.payload.decode()} from topic {msg.topic}")

    @client.disconnect_callback()
    def on_disconnect(client, userdata, rc):
        if rc != 0:
            print("Unexpected disconnection.")

    client.connect(broker, port = 1883, keepalive = 60)
    return client

def subscribe_mqtt(client):
    client.subscribe(topic)

def run():
    client = connect_mqtt()
    subscribe_mqtt(client)
    client.loop_forever()

if __name__ == '__main__':
    run()