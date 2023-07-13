import cv2
import os
import numpy as np
from posture_classification.pose_module import PoseEstimator
from posture_classification.posture_module import PostureClassifier
from posture_classification.posture_analyzer import PostureAnalyzer

classes = ['correta', 'incorreta']
estimator = PoseEstimator()

images_test_dir = './images_test'
images_analyzed_dir = './images_analyzed'

images = os.listdir(images_test_dir)

for image in images:

    with open(f'{images_test_dir}/{image}', 'rb') as image_file:
        image_data = image_file.read()

    image_as_np = np.frombuffer(image_data, dtype=np.uint8)

    frame = cv2.imdecode(image_as_np, flags=1)

    frame_detected, body_marks = estimator.process_capture(frame)

    classifier = PostureClassifier(body_marks)
    result, shap_values = classifier.make_classification()

    class_result = classes[round(result[0])]

    print(f'\n\nPostura: {class_result} / Score: {result}')

    if class_result == classes[1]:
        analyzer = PostureAnalyzer(body_marks, shap_values, frame)

        frame_analyzed = analyzer.explain_image()
        cv2.imwrite(f'{images_analyzed_dir}/{image}', frame_analyzed)