import os
import cv2
import datetime
import numpy as np
import time
from base64 import b64decode
from json import load, dump
import paho.mqtt.client as mqtt
from posture_classification.pose_module import PoseEstimator
from posture_classification.posture_module import PostureClassifier
from dotenv import load_dotenv

load_dotenv()

BROKER_IP = os.environ['BROKER_IP']
BROKER_PORT = 1883
IMAGES_TOPIC = 'images'

estimator = PoseEstimator()

images_test_dir = './images_test'
images_test_detected_dir = './images_test_detected'
classes = ['correta', 'incorreta']

logs = None
log_file_path = 'logs.json'


def main():
    global logs

    if not os.path.exists(images_test_dir):
        os.mkdir(images_test_dir)

    if not os.path.exists(images_test_detected_dir):
        os.mkdir(images_test_detected_dir)

    logs = read_log_file()
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

    # print("Message received")
    timestamp = datetime.datetime.now()

    image_data = b64decode(message.payload)
    image_as_np = np.frombuffer(image_data, dtype=np.uint8)

    # print('Iniciando detecção dos pontos-chave')

    frame = cv2.imdecode(image_as_np, flags=1)
    image_name = f'{images_test_dir}/{timestamp}.jpeg'
    cv2.imwrite(image_name, frame)

    start = time.time()
    
    frame_detected, body_marks = estimator.process_capture(frame)
    classifier = PostureClassifier(body_marks)
    result = classifier.make_classification()
    
    class_result = classes[round(result[0][0])]
    print(f'\n\nPostura: {class_result} / Score: {result[0]}')
    print(f'Tempo: {time.time() - start} s\n')

    log = {
        'path': image_name,
        'postura': class_result,
        'score': float(result[0][0])
    }

    for key in result[1].keys():
        log[key] = float(result[1][key])

        result[1].items()

    write_log_file(log)

    image_detected_name = f'{images_test_detected_dir}/{timestamp}.jpeg'
    cv2.imwrite(image_detected_name, frame_detected)


def read_log_file():
    with open(log_file_path, 'r') as log_file:
        try:
            previous_logs = load(log_file)
        except:
            previous_logs = []
    
    return previous_logs


def write_log_file(log):
    global logs

    logs.append(log)

    with open(log_file_path, 'w') as log_file:
        dump(logs, log_file, indent=2)

if __name__ == '__main__':
    main()