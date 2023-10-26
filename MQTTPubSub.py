import time 
import paho.mqtt.client as mqtt
import random

broker = "localhost"
topic = "testTopic"

def connect_mqtt():

    client = mqtt.Client("PruebaMQTT")

    @client.connect_callback()
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected OK")
        else:
            print("Bad connection")

    @client.log_callback()
    def on_log(client, userdata, level, buf):
        print(f"Log : {buf}")

    @client.disconnect_callback()
    def on_disconnect(client, userdata, rc):
        if rc != 0:
            print("Unexpected disconnection.")

    client.connect(broker, port = 1883, keepalive = 10)
    return client

def publish_mqtt(client):
    # Generating random numbers as payload
    while True: 
        message = str(random.randint(1, 30))
        client.publish(topic, message)
        time.sleep(2)

def run():
    client = connect_mqtt()
    client.loop_start()
    publish_mqtt(client)
    client.loop_stop()

if __name__ == '__main__':
    run()