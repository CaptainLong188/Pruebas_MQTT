import time 
import paho.mqtt.client as mqtt
import random

broker = "localhost"
topic = "sensor/nivel_de_agua"

def connect_mqtt():

    client = mqtt.Client("PruebaMQTT")

    @client.connect_callback()
    def on_connect(client, userdata, flags, rc):
        print(f"{mqtt.connack_string(rc)}")

    @client.log_callback()
    def on_log(client, userdata, level, buf):
        print(f"Log : {buf}")

    @client.disconnect_callback()
    def on_disconnect(client, userdata, rc):
        if rc != 0:
            print("Unexpected disconnection.")

    client.connect(broker, port = 1883, keepalive = 60)
    return client

def publish_mqtt(client):
    # Generating random numbers as payload
    while True: 
        message = str(random.randint(1, 30))
        info = client.publish(topic, message, qos = 2)
        
        if info.is_published:
            print(f"Message {message} sent to topic {topic}")

        time.sleep(2)

def run():
    client = connect_mqtt()
    client.loop_start()
    publish_mqtt(client)
    client.loop_stop()

if __name__ == '__main__':
    run()