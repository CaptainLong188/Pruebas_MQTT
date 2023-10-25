import time 
import random
import paho.mqtt.client as mqtt

hostname = "192.168.1.110"
broker_port = 1883
topic = "testTopic"

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect(hostname, broker_port)
    return client

def publish(client):
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

def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)
    client.loop_stop()


if __name__ == '__main__':
    run()
