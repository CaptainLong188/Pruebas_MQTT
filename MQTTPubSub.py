import time 
import paho.mqtt.client as mqtt

broker = "localhost"
topic = "testTopic"

# Called when the client has log information
def on_log(client, userdata, level, buf):
    print(f"Log : {buf}")

# Called when the broker responds to our connection request
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected OK")
    else:
        print("Bad connection")

# Called when the client disconnects from the server
def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection.")

client = mqtt.Client("PruebaMQTT")

client.on_connect = on_connect
client.on_log = on_log
client.on_disconnect = on_disconnect

client.connect(broker)
client.loop_start()
client.publish(topic = topic, payload = 123)
time.sleep(4)
client.loop_stop()
client.disconnect()