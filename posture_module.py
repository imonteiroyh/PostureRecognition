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
'''

class PostureClassifier():

    def __init__(self, marks):
        self.marks = marks
        self.decision_rules_classifier = DecisionRulesClassifier(self.marks)

    def debug(self):
        neck_angle = self.decision_rules_classifier.get_neck_condition()
        print('Neck:', neck_angle)

        trunk_angle = self.decision_rules_classifier.get_trunk_condition()
        print('Trunk:', trunk_angle)


class DecisionRulesClassifier():

    def __init__(self, marks):
        self.marks = marks
        self.nose = self.marks[0]
        self.neck = self.marks[1]
        self.right_elbow = self.marks[3]
        self.left_elbow = self.marks[6]
        self.right_shoulder = self.marks[2]
        self.left_shoulder = self.marks[5]
        self.right_wrist = self.marks[4]
        self.left_wrist = self.marks[7]
        self.right_knee = self.marks[9]
        self.left_knee = self.marks[12]
        self.right_ankle = self.marks[10]
        self.left_ankle = self.marks[13]
        self.right_hip = self.marks[8]
        self.left_hip = self.marks[11]
        self.right_eye = self.marks[14]
        self.left_eye = self.marks[15]
        self.right_ear = self.marks[16]
        self.left_ear = self.marks[17]


    def get_neck_condition(self):
        # CONSIDERAR UM ÂNGULO PADRÃO PELA MÉDIA DAS POSTURAS CORRETAS

        # OBTER ÂNGULO DO PESCOÇO A PARTIR DOS PONTOS 1 E 16,17
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

        if mean_ear_coordinates == None:
            return []

        neck_angle = 90 - get_angle(mean_ear_coordinates, neck_coordinates)

        # VERIFICAR A DIFERENÇA EM MÓDULO PARA O ÂNGULO PADRÃO

        return [neck_angle]


    def get_trunk_condition(self):
        # CONSIDERAR UM ÂNGULO PADRÃO PELA MÉDIA DAS POSTURAS CORRETAS

        # OBTER ÂNGULO DO TRONCO A PARTIR DOS PONTOS 1 E 16,17
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

        if mean_hip_coordinates == None:
            return []

        trunk_angle = 90 - get_angle(mean_hip_coordinates, neck_coordinates)

        # VERIFICAR A DIFERENÇA EM MÓDULO PARA O ÂNGULO PADRÃO

        return [trunk_angle]


    def get_shoulder_condition(self):
        # 2 E 5 DEVEM ESTAR EM UMA ALTURA RELATIVA A 8 E 11, DEVEM SER ANALISADAS AS MEDIDAS ANTERIORES DA PESSOA PARA VERIFICAR SE ELA ESTÁ
        # LEVANTANDO O OMBRO (CALIBRAGEM)
        pass


    def get_upper_arm_condition(self):
        pass


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


if __name__ == '__main__':
    marks = [[(305, 234, 1.0145667791366577, 0)], [(191, 363, 0.7859399318695068, 1)], [(201, 373, 0.8623086214065552, 2)], [(303, 567, 0.9791483283042908, 3)], [(470, 541, 1.0466033220291138, 4)], [(180, 351, 0.6807049512863159, 5)], [(291, 530, 0.23234817385673523, 6)], [(460, 556, 0.2110515534877777, 7)], [(248, 668, 0.7607256770133972, 8)], [(534, 669, 0.9985352158546448, 9)], [(537, 970, 0.9268811345100403, 10)], [(245, 647, 0.5039076805114746, 11)], [(494, 628, 0.1877688765525818, 12)], [], [(293, 203, 0.9912337064743042, 14)], [], [(219, 204, 0.9412510991096497, 16)], []]

    classifier = PostureClassifier(marks)
    classifier.debug()
