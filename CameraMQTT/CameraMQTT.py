import os
import paho.mqtt.client as mqtt
from picamera import PiCamera
from io import BytesIO
from base64 import b64encode
from time import sleep
from dotenv import load_dotenv

load_dotenv()

BROKER_IP = os.environ['BROKER_IP']
BROKER_PORT = 1883
IMAGES_TOPIC = 'images'

CAMERA_RESOLUTION = (640, 480)
CAPTURE_PERIOD = 10 # in seconds


def capture(camera: PiCamera, image_stream: BytesIO, resolution: tuple, format='jpeg', rotation=0, vflip=False):
    camera.resolution = resolution
    camera.vflip = vflip
    camera.rotation = rotation
    camera.capture(image_stream, format= format)


def read_image(image_stream: BytesIO) -> bytes:
    image_stream.seek(0)
    return image_stream.read()


def main():
    client = mqtt.Client('camera')
    client.connect(BROKER_IP, BROKER_PORT)

    camera = PiCamera()
    
    while True:
        client.loop()
        try:
            image_stream = BytesIO()

            capture(camera, image_stream, CAMERA_RESOLUTION, rotation=90)
            
            image = read_image(image_stream)
            image_stream.close()

            data = b64encode(image)

            client.publish(IMAGES_TOPIC, data)
            print("Sending image")
            sleep(CAPTURE_PERIOD)

        except:
            camera.close()
            break

        finally:
            image_stream.close()


main()
