import numpy as np
import cv2
from configobj import ConfigObj
from utils import pad_right_down_corner
from layers import convolution, relu, pooling
from keras.layers import Input, Lambda, Concatenate
from keras.models import Model
from scipy.ndimage import gaussian_filter
import mediapipe as mp

class PoseEstimator():

    def __init__(self):
        self.__colors = [[85, 0, 255], [0, 0, 255], [0, 85, 255], [0, 170, 255], [0, 255, 255],
                         [0, 255, 170], [0, 255, 85], [0, 255, 0], [85, 255, 0], [170, 255, 0],
                         [255, 255, 0], [255, 170, 0], [255, 85, 0], [255, 0, 0], [170, 0, 255],
                         [255, 0, 170], [255, 0, 255], [255, 0, 85], [85, 255, 255], [170, 255, 255]]

        self.__paf_channels = 38
        self.__heatmap_channels = 19

        self.__model = self.__get_model()
        self.__load_model_weights('model.h5')

        self.__parameters = {}
        self.__model_parameters = {}
        self.__read_configurations('config.ini')

        self.draw = mp.solutions.drawing_utils
        self.pose = mp.solutions.pose.Pose()


    def __load_model_weights(self, weights_file):
        try:
            self.__model.load_weights(weights_file)
            print('Modelo carregado com sucesso')
        except Exception as e:
            print('Erro ao carregar o modelo: ', e)


    def __read_configurations(self, configurations_file):
        configurations = ConfigObj(configurations_file)

        model_configurations = configurations['model_parameters']
        self.__model_parameters['boxsize'] = int(model_configurations['boxsize'])
        self.__model_parameters['stride'] = int(model_configurations['stride'])
        self.__model_parameters['pad_value'] = int(model_configurations['pad_value'])

        meta_configurations = configurations['parameters']
        self.__parameters['scale_search'] = list(map(float, meta_configurations['scale_search']))
        self.__parameters['threshold_1'] = float(meta_configurations['threshold_1'])


    def __vgg_block(self, input_tensor, weight_decay):

        tensor = input_tensor

        # Bloco 1
        tensor = convolution(tensor, 64, 3, 'block_1_convolution_1', (weight_decay, 0))
        tensor = relu(tensor)
        tensor = convolution(tensor, 64, 3, 'block_1_convolution_2', (weight_decay, 0))
        tensor = relu(tensor)
        tensor = pooling(tensor, 2, 2, 'block_1_pooling_1')

        # Bloco 2
        tensor = convolution(tensor, 128, 3, 'block_2_convolution_1', (weight_decay, 0))
        tensor = relu(tensor)
        tensor = convolution(tensor, 128, 3, 'block_2_convolution_2', (weight_decay, 0))
        tensor = relu(tensor)
        tensor = pooling(tensor, 2, 2, 'block_2_pooling_1')

        # Bloco 3
        tensor = convolution(tensor, 256, 3, 'block_3_convolution_1', (weight_decay, 0))
        tensor = relu(tensor)
        tensor = convolution(tensor, 256, 3, 'block_3_convolution_2', (weight_decay, 0))
        tensor = relu(tensor)
        tensor = convolution(tensor, 256, 3, 'block_3_convolution_3', (weight_decay, 0))
        tensor = relu(tensor)
        tensor = convolution(tensor, 256, 3, 'block_3_convolution_4', (weight_decay, 0))
        tensor = relu(tensor)
        tensor = pooling(tensor, 2, 2, 'block_3_pooling_1')

        # Bloco 4
        tensor = convolution(tensor, 512, 3, 'block_4_convolution_1', (weight_decay, 0))
        tensor = relu(tensor)
        tensor = convolution(tensor, 512, 3, 'block_4_convolution_2', (weight_decay, 0))
        tensor = relu(tensor)

        # Camadas não-VGG adicionais
        tensor = convolution(tensor, 256, 3, 'block_4_convolution_3', (weight_decay, 0))
        tensor = relu(tensor)
        tensor = convolution(tensor, 128, 3, 'block_4_convolution_4', (weight_decay, 0))
        tensor = relu(tensor)

        return tensor


    def __stage_1_block(self, input_tensor, number_of_keypoints, branch, weight_decay):

        tensor = input_tensor

        tensor = convolution(tensor, 128, 3, f'{branch}_stage_1_convolution_1', (weight_decay, 0))
        tensor = relu(tensor)
        tensor = convolution(tensor, 128, 3, f'{branch}_stage_1_convolution_2', (weight_decay, 0))
        tensor = relu(tensor)
        tensor = convolution(tensor, 128, 3, f'{branch}_stage_1_convolution_3', (weight_decay, 0))
        tensor = relu(tensor)
        tensor = convolution(tensor, 512, 1, f'{branch}_stage_1_convolution_4', (weight_decay, 0))
        tensor = relu(tensor)
        tensor = convolution(tensor, number_of_keypoints, 1, f'{branch}_stage_1_convolution_5', (weight_decay, 0))

        return tensor


    def __stage_n_block(self, input_tensor, number_of_keypoints, stage, branch, weight_decay):

        tensor = input_tensor

        tensor = convolution(tensor, 128, 7, f'{branch}_stage_{stage}_convolution_1', (weight_decay, 0))
        tensor = relu(tensor)
        tensor = convolution(tensor, 128, 7, f'{branch}_stage_{stage}_convolution_2', (weight_decay, 0))
        tensor = relu(tensor)
        tensor = convolution(tensor, 128, 7, f'{branch}_stage_{stage}_convolution_3', (weight_decay, 0))
        tensor = relu(tensor)
        tensor = convolution(tensor, 128, 7, f'{branch}_stage_{stage}_convolution_4', (weight_decay, 0))
        tensor = relu(tensor)
        tensor = convolution(tensor, 128, 7, f'{branch}_stage_{stage}_convolution_5', (weight_decay, 0))
        tensor = relu(tensor)
        tensor = convolution(tensor, 128, 1, f'{branch}_stage_{stage}_convolution_6', (weight_decay, 0))
        tensor = relu(tensor)
        tensor = convolution(tensor, number_of_keypoints, 1, f'{branch}_stage_{stage}_convolution_7', (weight_decay, 0))

        return tensor


    def __get_model(self):
        stages = 6

        image_input_shape = (None, None, 3)

        image_input = Input(shape=image_input_shape)

        image_normalized = Lambda(lambda x: x / 255 - 0.5)(image_input)

        stage_0_output = self.__vgg_block(image_normalized, None)

        stage_1_paf_output = self.__stage_1_block(stage_0_output, self.__paf_channels, 'paf', None)
        stage_1_heatmap_output = self.__stage_1_block(stage_0_output, self.__heatmap_channels, 'heatmap', None)

        concatenated_features = Concatenate()([stage_1_paf_output, stage_1_heatmap_output, stage_0_output])

        stage_n_paf_output = None
        stage_n_heatmap_output = None
        for stage in range(2, stages + 1):
            stage_n_paf_output = self.__stage_n_block(concatenated_features, self.__paf_channels, stage, 'paf', None)
            stage_n_heatmap_output = self.__stage_n_block(concatenated_features, self.__heatmap_channels, stage, 'heatmap', None)

            if stage < stages:
                concatenated_features = Concatenate()([stage_n_paf_output, stage_n_heatmap_output, stage_0_output])

        model = Model(inputs=[image_input], outputs=[stage_n_paf_output, stage_n_heatmap_output])

        return model


    def __get_hand_marks(self, input_image):

        image = input_image.copy()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        results = self.pose.process(image)

        hand_marks = [[], []]
        if results.pose_landmarks:

            for id in range(17, 23):
                landmark = results.pose_landmarks.landmark[id]

                height, width, _ = image.shape

                coordinate_x, coordinate_y, visibility = int(landmark.x * width), int(landmark.y * height), landmark.visibility

                position = (coordinate_x, coordinate_y, visibility, id)

                if id % 2 == 1:
                    hand_marks[0].append(position)
                else:
                    hand_marks[1].append(position)

        return hand_marks


    def process_capture(self, input_image):

        # Imagem no formato BGR
        original_image = input_image.copy()

        multiplier = [x * self.__model_parameters['boxsize'] / original_image.shape[0] for x in self.__parameters['scale_search']]
        multiplier = [multiplier.pop(0)]

        paf_average = np.zeros((original_image.shape[0], original_image.shape[1], self.__paf_channels))
        heatmap_average = np.zeros((original_image.shape[0], original_image.shape[1], self.__heatmap_channels))

        for scale in multiplier:
            image = cv2.resize(original_image, (0, 0), fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
            image_padded, pad = pad_right_down_corner(image, self.__model_parameters['stride'], self.__model_parameters['pad_value'])

            image = np.transpose(np.float32(image_padded[:, :, :, np.newaxis]), (3, 0, 1, 2))
            output = self.__model.predict(image)

            paf = np.squeeze(output[0])
            paf = cv2.resize(paf, (0, 0), fx=self.__model_parameters['stride'], fy=self.__model_parameters['stride'], interpolation=cv2.INTER_CUBIC)
            paf = paf[: image_padded.shape[0] - pad[0] - pad[2], : image_padded.shape[1] - pad[1] - pad[3], :]
            paf = cv2.resize(paf, (original_image.shape[1], original_image.shape[0]), interpolation=cv2.INTER_CUBIC)
            paf_average += paf / len(multiplier)

            heatmap = np.squeeze(output[1])
            heatmap = cv2.resize(heatmap, (0, 0), fx=self.__model_parameters['stride'], fy=self.__model_parameters['stride'], interpolation=cv2.INTER_CUBIC)
            heatmap = heatmap[: image_padded.shape[0] - pad[0] - pad[2], : image_padded.shape[1] - pad[1] - pad[3], :]
            heatmap = cv2.resize(heatmap, (original_image.shape[1], original_image.shape[0]), interpolation=cv2.INTER_CUBIC)
            heatmap_average += heatmap / len(multiplier)

        number_of_detected_marks = 0
        
        mark_counter = 0
        body_marks = []
        for body_part in range(self.__heatmap_channels - 1):
            original_heatmap = heatmap_average[:, :, body_part].copy()
            heatmap = gaussian_filter(original_heatmap, sigma=3)

            heatmap_left = np.zeros(heatmap.shape)
            heatmap_left[1 :, :] = heatmap[: -1, :]
            heatmap_right = np.zeros(heatmap.shape)
            heatmap_right[: -1, :] = heatmap[1 :, :]
            heatmap_up = np.zeros(heatmap.shape)
            heatmap_up[:, 1 :] = heatmap[:, : -1]
            heatmap_down = np.zeros(heatmap.shape)
            heatmap_down[:, : -1] = heatmap[:, 1 :]

            marks_binary = np.logical_and.reduce(
                (heatmap >= heatmap_left, heatmap >= heatmap_right, heatmap >= heatmap_up, heatmap >= heatmap_down, heatmap > self.__parameters['threshold_1'])
            )

            marks = list(zip(np.nonzero(marks_binary)[1], np.nonzero(marks_binary)[0]))
            marks_with_score = [mark + (original_heatmap[mark[1], mark[0]], ) for mark in marks]

            mark_id = range(mark_counter, mark_counter + len(marks))
            marks_with_score_and_id = [marks_with_score[i] + (mark_id[i], ) for i in range(len(marks))]

            number_of_detected_marks += len(marks_with_score_and_id)
            body_marks.append(marks_with_score_and_id)
            mark_counter += 1
    
        hand_marks = self.__get_hand_marks(input_image)

        frame = input_image.copy()

        for i in range(self.__heatmap_channels - 1):
            for j in range(len(body_marks[i])):
                cv2.circle(frame, body_marks[i][j][0 : 2], 4, self.__colors[i], thickness=-1)

        for i in range(2):
            for j in range(3):
                try:
                    if hand_marks[i][j][2] > 0.7:
                        cv2.circle(frame, hand_marks[i][j][0 : 2], 4, self.__colors[self.__heatmap_channels - 1 + i], thickness=-1)
                except:
                    continue
        return frame, body_marks, hand_marks