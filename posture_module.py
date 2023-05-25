import numpy as np
from utils import get_angle, get_distance
'''
LÓGICA A SER IMPLEMENTADA:
- TD - INSTANCIAÇÃO DA CLASSE COM AS POSIÇÕES COMO ENTRADA
- TD - ÂNGULOS A SEREM ENCONTRADOS:
        (PESCOÇO) -> (8, 11) (1) (0, 14, 15)
        (COLUNA) -> (1 [RETA DA ALTURA EXTERNA]) (8, 11) (1)
        (COLUNA-BRAÇO) -> (8, 11) (2, 1, 5) (3, 6)
        (BRAÇO-ANTEBRAÇO) -> (2, 1, 5) (3, 6) (4, 7)
        (COLUNA-COXA) -> (1) (8, 11) (9, 12)
        (COXA-PANTURRILHA) -> (8, 11) (9, 12) (10, 13)
- TD - IMPLEMENTAR AS REGRAS DE CLASSIFICAÇÃO
- TD - ANALISAR SE A PESSOA ESTÁ REALMENTE SENTADA OU ESTÁ NUMA POSIÇÃO INCORRETA
- TD - CALIBRAR PARA DETERMINAR A DISTÂNCIA ENTRE O OMBRO E OS QUADRIS

# CONSIDERAR UM ÂNGULO PADRÃO PELA MÉDIA DAS POSTURAS CORRETAS
# DEPOIS DIFERENCIAR O ÂNGULO OBTIDO PELO PADRÃO
'''

class PostureClassifier():

    def __init__(self, body_marks, hand_marks):
        self.body_marks = body_marks
        self.hand_marks = hand_marks
        self.posture_condition = PostureCondition(self.body_marks, self.hand_marks)


class PostureCondition():

    def __init__(self, body_marks, hand_marks):
        self.body_marks = body_marks
        self.hand_marks = hand_marks

        self.nose = self.body_marks[0]
        self.neck = self.body_marks[1]
        self.right_elbow = self.body_marks[3]
        self.left_elbow = self.body_marks[6]
        self.right_shoulder = self.body_marks[2]
        self.left_shoulder = self.body_marks[5]
        self.right_wrist = self.body_marks[4]
        self.left_wrist = self.body_marks[7]
        self.right_knee = self.body_marks[9]
        self.left_knee = self.body_marks[12]
        self.right_ankle = self.body_marks[10]
        self.left_ankle = self.body_marks[13]
        self.right_hip = self.body_marks[8]
        self.left_hip = self.body_marks[11]
        self.right_eye = self.body_marks[14]
        self.left_eye = self.body_marks[15]
        self.right_ear = self.body_marks[16]
        self.left_ear = self.body_marks[17]

        self.get_trunk_condition()
        self.get_neck_condition()
        self.get_upper_arm_condition()
        self.get_elbow_condition()
        self.get_wrist_condition()
        self.get_thigh_condition()
        self.get_knee_condition()


    def __is_rotated_trunk(self):
        self.rotated_trunk = False

        if self.left_shoulder:
            left_shoulder_coordinates = self.left_shoulder[0][0 : 2]

        if self.right_shoulder:
            right_shoulder_coordinates = self.right_shoulder[0][0 : 2]

        shoulder_distance = get_distance(left_shoulder_coordinates, right_shoulder_coordinates)

        if not shoulder_distance:
            return

        if self.left_elbow:
            left_elbow_coordinates = self.left_elbow[0][0 : 2]

        if self.right_elbow:
            right_elbow_coordinates = self.right_elbow[0][0 : 2]

        left_shoulder_elbow_distance = get_distance(left_shoulder_coordinates, left_elbow_coordinates)
        right_shoulder_elbow_distance = get_distance(right_shoulder_coordinates, right_elbow_coordinates)

        if left_shoulder_elbow_distance and right_shoulder_elbow_distance:
            shoulder_elbow_distance = np.mean([left_shoulder_elbow_distance, right_shoulder_elbow_distance])
        elif not left_shoulder_elbow_distance:
            shoulder_elbow_distance = right_shoulder_elbow_distance
        elif not right_shoulder_elbow_distance:
            shoulder_elbow_distance = left_shoulder_elbow_distance
        else:
            return

        if shoulder_distance > 0.5 * shoulder_elbow_distance:
            self.rotated_trunk = True


    def __get_trunk_angle(self):
        self.trunk_angle = None

        if self.rotated_trunk:
            return

        if self.neck:
            neck_coordinates = self.neck[0][0 : 2]
        else:
            return

        mean_hip_coordinates = None

        if self.left_hip:
            left_hip_coordinates = self.left_hip[0][0 : 2]
            mean_hip_coordinates = left_hip_coordinates

        if self.right_hip:
            right_hip_coordinates = self.right_hip[0][0 : 2]

            if mean_hip_coordinates == None:
                mean_hip_coordinates = right_hip_coordinates
            else:
                mean_hip_coordinates = tuple((left_hip_coordinate + right_hip_coordinate) / 2 for left_hip_coordinate, right_hip_coordinate in zip(mean_hip_coordinates, right_hip_coordinates))

        if not mean_hip_coordinates:
            return

        self.trunk_angle = get_angle(mean_hip_coordinates, neck_coordinates) - 90

        mean_knee_coordinates = None

        if self.left_knee:
            left_knee_coordinates = self.left_knee[0][0 : 2]
            mean_knee_coordinates = left_knee_coordinates

        if self.right_knee:
            right_knee_coordinates = self.right_knee[0][0 : 2]

            if mean_knee_coordinates == None:
                mean_knee_coordinates = right_knee_coordinates
            else:
                mean_knee_coordinates = tuple((left_knee_coordinate + right_knee_coordinate) / 2 for left_knee_coordinate, right_knee_coordinate in zip(mean_knee_coordinates, right_knee_coordinates))

        if not mean_knee_coordinates:
            return

        if np.sign(mean_knee_coordinates[0] - mean_hip_coordinates[0]) != np.sign(mean_hip_coordinates[0] - neck_coordinates[0]):
            self.trunk_angle = -self.trunk_angle


    def __is_rotated_neck(self):
        self.rotated_neck = False

        if self.rotated_trunk:
            self.rotated_neck = True
            return

        if self.nose and self.left_eye and self.right_eye and self.left_ear and self.right_ear:
            self.rotated_neck = True

        if (not self.nose and not self.left_eye and not self.right_eye) or (self.left_ear and self.right_ear):
            self.rotated_neck = True


    def __get_neck_angle(self):
        self.neck_angle = None

        if self.rotated_neck:
            return

        if self.neck:
            neck_coordinates = self.neck[0][0 : 2]
        else:
            return

        mean_ear_coordinates = None

        if self.left_ear:
            left_ear_coordinates = self.left_ear[0][0 : 2]
            mean_ear_coordinates = left_ear_coordinates

        if self.right_ear:
            right_ear_coordinates = self.right_ear[0][0 : 2]

            if mean_ear_coordinates == None:
                mean_ear_coordinates = right_ear_coordinates
            else:
                mean_ear_coordinates = tuple(left_ear_coordinate + right_ear_coordinate for left_ear_coordinate, right_ear_coordinate in zip(mean_ear_coordinates, right_ear_coordinates))

        if not mean_ear_coordinates:
            return

        self.neck_angle = 90 - get_angle(mean_ear_coordinates, neck_coordinates)

        if self.nose:
            nose_coordinates = self.nose[0][0 : 2]

            if np.sign(nose_coordinates[0] - neck_coordinates[0]) != np.sign(mean_ear_coordinates[0] - neck_coordinates[0]):
                self.neck_angle = -self.neck_angle


    def __get_upper_arm_angle(self):
        self.left_upper_arm_angle = None
        self.right_upper_arm_angle = None

        if self.left_hip and self.left_shoulder and self.left_elbow:
            hip_coordinates = self.left_hip[0][0 : 2]
            shoulder_coordinates = self.left_shoulder[0][0 : 2]
            elbow_coordinates = self.left_elbow[0][0 : 2]

            self.left_upper_arm_angle = get_angle(hip_coordinates, shoulder_coordinates, elbow_coordinates)

        if self.right_hip and self.right_shoulder and self.right_elbow:
            hip_coordinates = self.right_hip[0][0 : 2]
            shoulder_coordinates = self.right_shoulder[0][0 : 2]
            elbow_coordinates = self.right_elbow[0][0 : 2]

            self.right_upper_arm_angle = get_angle(hip_coordinates, shoulder_coordinates, elbow_coordinates)


    def __get_elbow_angle(self):
        self.left_elbow_angle = None
        self.right_elbow_angle = None

        if self.left_shoulder and self.left_elbow and self.left_wrist:
            shoulder_coordinates = self.left_shoulder[0][0 : 2]
            elbow_coordinates = self.left_elbow[0][0 : 2]
            wrist_coordinates = self.left_wrist[0][0 : 2]

            self.left_elbow_angle = get_angle(shoulder_coordinates, elbow_coordinates, wrist_coordinates)

        if self.right_shoulder and self.right_elbow and self.right_wrist:
            shoulder_coordinates = self.right_shoulder[0][0 : 2]
            elbow_coordinates = self.right_elbow[0][0 : 2]
            wrist_coordinates = self.right_wrist[0][0 : 2]

            self.right_elbow_angle = get_angle(shoulder_coordinates, elbow_coordinates, wrist_coordinates)


    def __is_lateral_elbow(self):
        self.left_elbow_lateral = False
        self.right_elbow_lateral = False

        mean_hip_coordinates = None

        if self.left_hip:
            left_hip_coordinates = self.left_hip[0][0 : 2]
            mean_hip_coordinates = left_hip_coordinates

        if self.right_hip:
            right_hip_coordinates = self.right_hip[0][0 : 2]

            if mean_hip_coordinates == None:
                mean_hip_coordinates = right_hip_coordinates
            else:
                mean_hip_coordinates = tuple((left_hip_coordinate + right_hip_coordinate) / 2 for left_hip_coordinate, right_hip_coordinate in zip(mean_hip_coordinates, right_hip_coordinates))

        if not mean_hip_coordinates:
            return

        mean_shoulder_coordinates = None

        if self.left_shoulder:
            left_shoulder_coordinates = self.left_shoulder[0][0 : 2]
            mean_shoulder_coordinates = left_shoulder_coordinates

        if self.right_shoulder:
            right_shoulder_coordinates = self.right_shoulder[0][0 : 2]

            if mean_shoulder_coordinates == None:
                mean_shoulder_coordinates = right_shoulder_coordinates
            else:
                mean_shoulder_coordinates = tuple((left_shoulder_coordinate + right_shoulder_coordinate) / 2 for left_shoulder_coordinate, right_shoulder_coordinate in zip(mean_shoulder_coordinates, right_shoulder_coordinates))

        if not mean_shoulder_coordinates:
            return

        hip_shoulder_distance = get_distance(mean_shoulder_coordinates, mean_hip_coordinates, type='vertical')

        if self.left_shoulder and self.left_elbow:
            shoulder_coordinates = self.left_shoulder[0][0 : 2]
            elbow_coordinates = self.left_elbow[0][0 : 2]

            left_elbow_shoulder_distance = get_distance(shoulder_coordinates, elbow_coordinates, type='vertical')

            if left_elbow_shoulder_distance < 0.35 * hip_shoulder_distance:
                self.left_elbow_lateral = True

        if self.right_shoulder and self.right_elbow:
            shoulder_coordinates = self.right_shoulder[0][0 : 2]
            elbow_coordinates = self.right_elbow[0][0 : 2]

            right_elbow_shoulder_distance = get_distance(shoulder_coordinates, elbow_coordinates, type='vertical')

            if right_elbow_shoulder_distance < 0.35 * hip_shoulder_distance:
                self.right_elbow_lateral = True


    def __is_horizontal_thigh(self):
        self.thigh_lateral = False
        pass


    def __get_knee_angle(self):
        self.left_knee_angle = None
        self.right_knee_angle = None

        if self.left_hip and self.left_knee and self.left_ankle:
            hip_coordinates = self.left_hip[0][0 : 2]
            knee_coordinates = self.left_knee[0][0 : 2]
            ankle_coordinates = self.left_ankle[0][0 : 2]

            self.left_knee_angle = get_angle(hip_coordinates, knee_coordinates, ankle_coordinates)

        if self.right_hip and self.right_knee and self.right_ankle:
            hip_coordinates = self.right_hip[0][0 : 2]
            knee_coordinates = self.right_knee[0][0 : 2]
            ankle_coordinates = self.right_ankle[0][0 : 2]

            self.right_knee_angle = get_angle(hip_coordinates, knee_coordinates, ankle_coordinates)


    def __is_rotated_knee(self):
        self.rotated_left_knee = False
        self.rotated_right_knee = False
        pass


    def get_trunk_condition(self):
        self.__is_rotated_trunk()
        self.__get_trunk_angle()

        print('trunk rotated', self.rotated_trunk)
        print('trunk angle', self.trunk_angle)


    def get_neck_condition(self):
        self.__is_rotated_neck()
        self.__get_neck_angle()

        print('neck rotated', self.rotated_neck)
        print('neck angle', self.neck_angle)


    def get_upper_arm_condition(self):
        self.__get_upper_arm_angle()

        print('upper arm left angle', self.left_upper_arm_angle)
        print('upper arm right angle', self.right_upper_arm_angle)


    def get_elbow_condition(self):
        self.__is_lateral_elbow()
        self.__get_elbow_angle()

        print('elbow left lateral', self.left_elbow_lateral)
        print('elbow right lateral', self.right_elbow_lateral)
        print('elbow left angle', self.left_elbow_angle)
        print('elbow right angle', self.right_elbow_angle)


    def get_thigh_condition(self):
        self.__is_horizontal_thigh()

        print('thigh lateral', self.thigh_lateral)


    def get_knee_condition(self):
        self.__get_knee_angle()
        self.__is_rotated_knee()

        print('knee left angle', self.left_knee_angle)
        print('knee right angle', self.right_knee_angle)
        print('knee left rotated', self.rotated_left_knee)
        print('knee right rotated', self.rotated_right_knee)


if __name__ == '__main__':
    body_marks = [[(305, 234, 1.0145667791366577, 0)], [(191, 363, 0.7859399318695068, 1)], [(201, 373, 0.8623086214065552, 2)], [(303, 567, 0.9791483283042908, 3)], [(470, 541, 1.0466033220291138, 4)], [(180, 351, 0.6807049512863159, 5)], [(291, 530, 0.23234817385673523, 6)], [(460, 556, 0.2110515534877777, 7)], [(248, 668, 0.7607256770133972, 8)], [(534, 669, 0.9985352158546448, 9)], [(537, 970, 0.9268811345100403, 10)], [(245, 647, 0.5039076805114746, 11)], [(494, 628, 0.1877688765525818, 12)], [], [(293, 203, 0.9912337064743042, 14)], [], [(219, 204, 0.9412510991096497, 16)], []]
    fbody_marks = [[(371, 197, 0.9837018251419067, 0)], [(487, 325, 0.8218739628791809, 1)], [(497, 317, 0.7343981266021729, 2)], [(433, 478, 0.30569300055503845, 3)], [(380, 511, 0.4105113744735718, 4)], [(480, 339, 0.9554383158683777, 5)], [(426, 509, 0.7783028483390808, 6)], [(359, 532, 0.6890574097633362, 7)], [(459, 589, 0.6676409244537354, 8)], [(211, 628, 0.3895173668861389, 9)], [(267, 875, 0.5220837593078613, 10)], [(471, 601, 0.7519378662109375, 11)], [(190, 627, 0.9800930023193359, 12)], [(229, 898, 0.8995195031166077, 13)], [], [(392, 177, 0.9386535882949829, 15)], [], [(461, 190, 0.9597209692001343, 17)]]

    n = PostureClassifier(body_marks).debug()
    # f = PostureClassifier(fbody_marks).debug()