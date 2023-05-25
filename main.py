import os
import cv2
import datetime
import numpy as np
import time
from base64 import b64decode
import paho.mqtt.client as mqtt
from posture_classification.pose_module import PoseEstimator
from dotenv import load_dotenv

load_dotenv()

BROKER_IP = os.environ['BROKER_IP']
BROKER_PORT = 1883
IMAGES_TOPIC = 'images'

estimator = PoseEstimator()

images_dir = './images'
images_detected_dir = './images_detected'


def main():
    if not os.path.exists(images_dir):
        os.mkdir(images_dir)

    if not os.path.exists(images_detected_dir):
        os.mkdir(images_detected_dir)

    client = start_client()

    client.on_message = on_message
    client.subscribe(IMAGES_TOPIC)

    client.loop_forever()


def start_client() -> mqtt.Client:
    client = mqtt.Client()
    client.connect(BROKER_IP, BROKER_PORT)
    return client


def on_message(client, userdata, message):
    global estimator

    print("Message received")
    timestamp = datetime.datetime.now()

    image_data = b64decode(message.payload)
    image_as_np = np.frombuffer(image_data, dtype=np.uint8)

    print('Iniciando detecção dos pontos-chave')

    frame = cv2.imdecode(image_as_np, flags=1)
    image_name = f'{images_dir}/{timestamp}.jpeg'
    cv2.imwrite(image_name, frame)

    start = time.time()
    frame_detected, body_marks = estimator.process_capture(frame)
    print(f'Tempo: {time.time() - start}')

    image_detected_name = f'{images_detected_dir}/{timestamp}.jpeg'
    cv2.imwrite(image_detected_name, frame_detected)

if __name__ == '__main__':
    main()