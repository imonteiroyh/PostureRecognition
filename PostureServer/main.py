import os
import cv2
import datetime
import numpy as np
import time
from base64 import b64decode, b64encode
from json import load, dump, loads, dumps
import paho.mqtt.client as mqtt
from posture_classification.pose_module import PoseEstimator
from posture_classification.posture_module import PostureClassifier
from posture_classification.posture_analyzer import PostureAnalyzer
from dotenv import load_dotenv

load_dotenv()

BROKER_IP = os.environ['BROKER_IP']
BROKER_PORT = 1883
IMAGES_TOPIC = 'camera/images'
CAPTURE_TOPIC = 'camera/capture'
CLASSIFICATION_TOPIC = 'posture/classification'

MINIMUM_BODY_MARKS = 10

estimator = PoseEstimator()

images_test_dir = './images_test'
images_test_detected_dir = './images_test_detected'
classes = ['correta', 'incorreta']

logs = None
log_file_path = 'logs.json'


def main():
    global logs

    # if not os.path.exists(images_test_dir):
    #     os.mkdir(images_test_dir)

    # if not os.path.exists(images_test_detected_dir):
    #     os.mkdir(images_test_detected_dir)

    # logs = read_log_file()
    
    client = start_client()

    client.on_message = on_message
    client.subscribe(IMAGES_TOPIC)

    client.publish(CAPTURE_TOPIC)
    client.loop_forever()


def start_client() -> mqtt.Client:
    client = mqtt.Client()
    client.connect(BROKER_IP, BROKER_PORT)
    return client


def on_message(client, userdata, message):
    global estimator

    # print("Message received")
    # timestamp = datetime.datetime.now()
    frame = read_image(message.payload)

    # print('Iniciando detecção dos pontos-chave')

    # image_name = f'{images_test_dir}/{timestamp}.jpeg'
    # cv2.imwrite(image_name, frame)

    start = time.time()
    
    frame_detected, body_marks = estimator.process_capture(frame)

    marks_count = 0
    for mark in body_marks:
        if mark:
            marks_count += 1

    if marks_count < MINIMUM_BODY_MARKS:
        payload = {
            'class': 'indeterminada',
            'image': encode_image_to_base64(frame)
        }
    
    else:
        classifier = PostureClassifier(body_marks)
        result, shap_values = classifier.make_classification()

        class_result = classes[round(result[0])]

        print(f'\n\nPostura: {class_result} / Score: {result[0]}')
        
        if class_result == classes[1]:
            analyzer = PostureAnalyzer(body_marks, shap_values, frame, is_incorrect=True)
        else:
            analyzer = PostureAnalyzer(body_marks, shap_values, frame, is_incorrect=False)
        
        frame_analyzed = analyzer.explain_image()
        payload = {
            'class': class_result,
            'image': encode_image_to_base64(frame_analyzed)
        }

    client.publish(CLASSIFICATION_TOPIC, dumps(payload))
    client.publish(CAPTURE_TOPIC)
    
    # print(f'SHAP: {shap_values}')
    # print(f'Tempo: {time.time() - start} s\n')

    # log = {
    #     'path': image_name,
    #     'postura': class_result,
    #     'score': float(result[0][0])
    # }

    # for key in result[1].keys():
    #     log[key] = float(result[1][key])

    #     result[1].items()

    # write_log_file(log)

    # image_detected_name = f'{images_test_detected_dir}/{timestamp}.jpeg'
    # cv2.imwrite(image_detected_name, frame_detected)

def read_image(image_base64):
    image_data = b64decode(image_base64)
    image_as_np = np.frombuffer(image_data, dtype=np.uint8)
    frame = cv2.imdecode(image_as_np, flags=1)
    return frame

def encode_image_to_base64(image):
    _, im_encoded = cv2.imencode('.jpg', image)
    return b64encode(im_encoded.tobytes()).decode()

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