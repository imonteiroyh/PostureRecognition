import os
import paho.mqtt.client as mqtt
from picamera import PiCamera
from io import BytesIO
from base64 import b64encode
from time import sleep
from dotenv import load_dotenv

load_dotenv()
camera = PiCamera()

BROKER_IP = os.environ['BROKER_IP']
BROKER_PORT = 1883
IMAGES_TOPIC = 'camera/images'
CAPTURE_TOPIC = 'camera/capture'

CAMERA_RESOLUTION = (640, 480)

def capture(camera: PiCamera, image_stream: BytesIO, resolution: tuple, format='jpeg', rotation=0, vflip=False):
    camera.resolution = resolution
    camera.vflip = vflip
    camera.rotation = rotation
    camera.capture(image_stream, format= format)


def read_image(image_stream: BytesIO) -> bytes:
    image_stream.seek(0)
    return image_stream.read()


def on_message(client, userdata, message):
    global camera

    if message.topic == CAPTURE_TOPIC:
        try:
            image_stream = BytesIO()

            capture(camera, image_stream, CAMERA_RESOLUTION, rotation=90)

            image = read_image(image_stream)
            image_stream.close()

            data = b64encode(image)

            client.publish(IMAGES_TOPIC, data)
            print("Sending image")

        except:
            pass

        finally:
            image_stream.close()


def main():
    client = mqtt.Client('camera')
    client.connect(BROKER_IP, BROKER_PORT)

    client.on_message = on_message
    client.subscribe(CAPTURE_TOPIC)

    client.loop_forever()


main()