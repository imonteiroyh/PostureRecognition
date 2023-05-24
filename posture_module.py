import numpy as np
from utils import get_angle
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

    def __init__(self, body_marks):
        self.body_marks = body_marks
        self.posture_condition = PostureCondition(self.body_marks)

    def debug(self):
        neck_angle = self.posture_condition.get_neck_condition()
        print('Neck:', neck_angle)

        trunk_angle = self.posture_condition.get_trunk_condition()
        print('Trunk:', trunk_angle)


class PostureCondition():

    def __init__(self, body_marks):
        self.body_marks = body_marks
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


    def get_neck_condition(self):
        if self.neck:
            neck_coordinates = self.neck[0][0 : 2]

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

        neck_angle = 90 - get_angle(mean_ear_coordinates, neck_coordinates)

        if self.nose:
            nose_coordinates = self.nose[0][0 : 2]
    
        if np.sign(nose_coordinates[0] - neck_coordinates[0]) != np.sign(mean_ear_coordinates[0] - neck_coordinates[0]):
            neck_angle = -neck_angle

        return [neck_angle]


    def get_trunk_condition(self):
        if self.neck:
            neck_coordinates = self.neck[0][0 : 2]

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

        trunk_angle = 90 - get_angle(mean_hip_coordinates, neck_coordinates)

        if self.nose:
            nose_coordinates = self.nose[0][0 : 2]
    
        if np.sign(nose_coordinates[0] - neck_coordinates[0]) != np.sign(mean_hip_coordinates[0] - neck_coordinates[0]):
            trunk_angle = -trunk_angle

        return [trunk_angle]
    
    def get_shoulder_condition(self):
        # DISTÂNCIA OMBRO OUVIDO OLHAR INFORMAÇÕES PASSADAS
        pass
    

    def get_upper_arm_condition(self):
        
    
        return [upper_arm_angle]


    def get_elbow_condition(self):
        pass


    def get_wrist_condition(self):
        pass


    def get_knee_condition(self):
        pass


class ClassicalClassifier():

    def __init__(self):
        pass


class NeuralNetworkClassifier():

    def __init__(self):
        pass


from utils import get_angle
if __name__ == '__main__':
    body_marks = [[(305, 234, 1.0145667791366577, 0)], [(191, 363, 0.7859399318695068, 1)], [(201, 373, 0.8623086214065552, 2)], [(303, 567, 0.9791483283042908, 3)], [(470, 541, 1.0466033220291138, 4)], [(180, 351, 0.6807049512863159, 5)], [(291, 530, 0.23234817385673523, 6)], [(460, 556, 0.2110515534877777, 7)], [(248, 668, 0.7607256770133972, 8)], [(534, 669, 0.9985352158546448, 9)], [(537, 970, 0.9268811345100403, 10)], [(245, 647, 0.5039076805114746, 11)], [(494, 628, 0.1877688765525818, 12)], [], [(293, 203, 0.9912337064743042, 14)], [], [(219, 204, 0.9412510991096497, 16)], []]
    fbody_marks = [[(371, 197, 0.9837018251419067, 0)], [(487, 325, 0.8218739628791809, 1)], [(497, 317, 0.7343981266021729, 2)], [(433, 478, 0.30569300055503845, 3)], [(380, 511, 0.4105113744735718, 4)], [(480, 339, 0.9554383158683777, 5)], [(426, 509, 0.7783028483390808, 6)], [(359, 532, 0.6890574097633362, 7)], [(459, 589, 0.6676409244537354, 8)], [(211, 628, 0.3895173668861389, 9)], [(267, 875, 0.5220837593078613, 10)], [(471, 601, 0.7519378662109375, 11)], [(190, 627, 0.9800930023193359, 12)], [(229, 898, 0.8995195031166077, 13)], [], [(392, 177, 0.9386535882949829, 15)], [], [(461, 190, 0.9597209692001343, 17)]]

    n = PostureClassifier(body_marks).debug()
    # f = PostureClassifier(fbody_marks).debug()