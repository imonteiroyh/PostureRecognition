import paho.mqtt.client as mqtt
from time import sleep 
from config import BROKER_IP, BROKER_PORT

def on_message(client, userdata, message):
    print(message.payload)

client = mqtt.Client("server")
client.connect(BROKER_IP, BROKER_PORT)
client.on_message = on_message
client.subscribe('images')

client.loop_forever()