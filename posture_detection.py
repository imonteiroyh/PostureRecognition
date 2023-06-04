import cv2
import os
import sys
import time
import argparse
import pandas as pd
from posture_classification.pose_module import PoseEstimator
from posture_classification.posture_module import PostureClassifier

parser = argparse.ArgumentParser()
parser.add_argument('type', help='Objetivo da detecção de pontos-chave')
args = parser.parse_args()

if args.type not in ['image', 'video', 'webcam']:
    sys.exit()

if __name__ == '__main__':
    print('Iniciando detecção dos pontos-chave')

    estimator = PoseEstimator()

    # Imagem
    data = pd.DataFrame()
    if args.type == 'image':

            for folder in ['correct/', 'incorrect/']:

                subfolders = ['arm_up/', 'chest_sloped/', 'chest_turned/', 'legs_up/', 'neck_sloped/', 'neck_turned/'] if folder == 'incorrect/' else ['/']
                for subfolder in subfolders:
                    i = 0
                    for file in os.listdir('image/' + folder + subfolder):
                        frame = cv2.imread('image/' + folder + subfolder + file)

                        start = time.time()
                        frame, body_marks = estimator.process_capture(frame)
                        classifier = PostureClassifier(body_marks)

                        info = classifier.get_info()
                        info_dataframe = pd.DataFrame.from_dict(info, orient='index').T
                        info_dataframe['file'] = file
                        info_dataframe['class'] = True if folder == 'incorrect/' else False

                        data = pd.concat([data, info_dataframe], ignore_index=True)
                        print(f'Tempo: {time.time() - start}')

                        # cv2.imshow(file, frame)
                        # cv2.waitKey(0)

                        # cv2.imwrite('image_processed/' + file, frame)



    # Video
    if args.type == 'video':

        capture = cv2.VideoCapture('video.mp4')
        writer = cv2.VideoWriter_fourcc(*'mp4v')

        output_fps = 30
        frame_size = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        output = cv2.VideoWriter('video_output.mp4', writer, output_fps, frame_size)

        while True:
            print('Leitura do vídeo iniciada')

            frame_read_sucess, frame = capture.read()

            if not frame_read_sucess:
                break

            start = time.time()
            frame, body_marks = estimator.process_capture(frame)
            print(f'Tempo: {time.time() - start}')

            cv2.imshow('Frame', frame)

            output.write(frame)

            key = cv2.waitKey(1) & 0xFF

            if key == ord('q'):
                break

    # Webcam
    if args.type == 'webcam':

        capture = cv2.VideoCapture(0)
        cam_is_open = capture.isOpened()

        if cam_is_open:
            time.sleep(2)

            print('Captura de vídeo iniciada')

            while True:
                frame_read_sucess, frame = capture.read()

                if not frame_read_sucess:
                    break

                start = time.time()
                frame, body_marks = estimator.process_capture(frame)
                print(f'Tempo: {time.time() - start}')

                cv2.imshow('Frame', frame)

                key = cv2.waitKey(1) & 0xFF

                if key == ord('q'):
                    break

            capture.release()

        else:
            print('Não foi possível abrir a câmera')

cv2.destroyAllWindows()
data.to_csv('features_dataset.csv')