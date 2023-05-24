import cv2
import sys
import time
import argparse
from pose_module import PoseEstimator

parser = argparse.ArgumentParser()
parser.add_argument('type', help='Objetivo da detecção de pontos-chave')
args = parser.parse_args()

if args.type not in ['image', 'video', 'webcam']:
    sys.exit()

if __name__ == '__main__':
    print('Iniciando detecção dos pontos-chave')

    estimator = PoseEstimator()

    # Imagem
    if args.type == 'image':

        frame = cv2.imread('image.jpg')

        start = time.time()
        frame, body_marks, hand_marks = estimator.process_capture(frame)
        print(f'Tempo: {time.time() - start}')

        cv2.imshow('Frame', frame)
        cv2.waitKey(0)

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
            frame, body_marks, hand_marks = estimator.process_capture(frame)
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
                frame, body_marks, hand_marks = estimator.process_capture(frame)
                print(f'Tempo: {time.time() - start}')

                cv2.imshow('Frame', frame)

                key = cv2.waitKey(1) & 0xFF

                if key == ord('q'):
                    break

            capture.release()

        else:
            print('Não foi possível abrir a câmera')

cv2.destroyAllWindows()