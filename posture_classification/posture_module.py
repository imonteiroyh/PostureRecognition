import warnings
warnings.filterwarnings('ignore')

import shap
import pickle
import numpy as np
import pandas as pd
from posture_classification.utils import get_angle, get_distance

class WaterfallData():
    def __init__(self, shap_test):
        self.values = shap_test[0].values
        self.base_values = shap_test[0].base_values
        self.data = shap_test[0].data
        self.display_data = None
        self.feature_names = shap_test.feature_names


class PostureClassifier():
    def __init__(self, body_marks):
        self.body_marks = body_marks
        self.posture_condition = PostureCondition(self.body_marks)
        self.info = self.posture_condition.get_info()
        self.info_dataframe = pd.DataFrame.from_dict(self.info, orient='index').T

        self.__directory = 'posture_classification/'

        self.pipeline = pickle.load(open(self.__directory + 'pipeline.pkl', 'rb'))
        self.classifier = pickle.load(open(self.__directory + 'classifier.pkl', 'rb'))


    def get_info(self):
        return self.info


    def __preprocess(self):
        X = self.pipeline.transform(self.info_dataframe)
        self.info_dataframe = pd.DataFrame(X, columns=self.info_dataframe.columns)


    def __explain_classification(self):
        self.explainer = shap.Explainer(self.classifier)
        self.shap_test = self.explainer(self.info_dataframe)

        self.shap_dict = {}
        for feature, shap_value in zip(self.shap_test.feature_names, self.shap_test[0].values):
            self.shap_dict[feature] = shap_value


    def __plot_shap_values(self):
        shap.plots.waterfall(WaterfallData(self.shap_test))


    def make_classification(self):
        self.__preprocess()
        self.__explain_classification()
        predicted_class = self.classifier.predict(self.info_dataframe)

        return predicted_class, self.shap_dict


class PostureCondition():
    def __init__(self, body_marks):
        self.body_marks = body_marks

        self.nose = self.body_marks[0]
        self.neck = self.body_marks[1]
        self.left_elbow = self.body_marks[6]
        self.right_elbow = self.body_marks[3]
        self.left_shoulder = self.body_marks[5]
        self.right_shoulder = self.body_marks[2]
        self.left_wrist = self.body_marks[7]
        self.right_wrist = self.body_marks[4]
        self.left_knee = self.body_marks[12]
        self.right_knee = self.body_marks[9]
        self.left_ankle = self.body_marks[13]
        self.right_ankle = self.body_marks[10]
        self.left_hip = self.body_marks[11]
        self.right_hip = self.body_marks[8]
        self.left_eye = self.body_marks[15]
        self.right_eye = self.body_marks[14]
        self.left_ear = self.body_marks[17]
        self.right_ear = self.body_marks[16]

        self.initialize()
        self.get_trunk_condition()
        self.get_neck_condition()
        self.get_upper_arm_condition()
        self.get_elbow_condition()
        self.get_thigh_condition()
        self.get_knee_condition()


    def initialize(self):
        self.info = {}

        if self.nose:
            self.nose_coordinates = self.nose[0][0 : 2]

        if self.neck:
            self.neck_coordinates = self.neck[0][0 : 2]

        if self.left_elbow:
            self.left_elbow_coordinates = self.left_elbow[0][0 : 2]

        if self.right_elbow:
            self.right_elbow_coordinates = self.right_elbow[0][0 : 2]

        if self.left_shoulder:
            self.left_shoulder_coordinates = self.left_shoulder[0][0 : 2]

        if self.right_shoulder:
            self.right_shoulder_coordinates = self.right_shoulder[0][0 : 2]

        if self.left_wrist:
            self.left_wrist_coordinates = self.left_wrist[0][0 : 2]

        if self.right_wrist:
            self.right_wrist_coordinates = self.right_wrist[0][0 : 2]

        if self.left_knee:
            self.left_knee_coordinates = self.left_knee[0][0 : 2]

        if self.right_knee:
            self.right_knee_coordinates = self.right_knee[0][0 : 2]

        if self.left_ankle:
            self.left_ankle_coordinates = self.left_ankle[0][0 : 2]

        if self.right_ankle:
            self.right_ankle_coordinates = self.right_ankle[0][0 : 2]

        self.mean_shoulder_coordinates = None

        if self.left_shoulder:
            self.left_shoulder_coordinates = self.left_shoulder[0][0 : 2]
            self.mean_shoulder_coordinates = self.left_shoulder_coordinates

        if self.right_shoulder:
            self.right_shoulder_coordinates = self.right_shoulder[0][0 : 2]

            if self.mean_shoulder_coordinates == None:
                self.mean_shoulder_coordinates = self.right_shoulder_coordinates
            else:
                self.mean_shoulder_coordinates = tuple(left_shoulder_coordinate + right_shoulder_coordinate for left_shoulder_coordinate, right_shoulder_coordinate in zip(self.mean_shoulder_coordinates, self.right_shoulder_coordinates))

        self.mean_hip_coordinates = None

        if self.left_hip:
            self.left_hip_coordinates = self.left_hip[0][0 : 2]
            self.mean_hip_coordinates = self.left_hip_coordinates

        if self.right_hip:
            self.right_hip_coordinates = self.right_hip[0][0 : 2]

            if self.mean_hip_coordinates == None:
                self.mean_hip_coordinates = self.right_hip_coordinates
            else:
                self.mean_hip_coordinates = tuple((left_hip_coordinate + right_hip_coordinate) / 2 for left_hip_coordinate, right_hip_coordinate in zip(self.mean_hip_coordinates, self.right_hip_coordinates))

        self.mean_knee_coordinates = None

        if self.left_knee:
            self.left_knee_coordinates = self.left_knee[0][0 : 2]
            self.mean_knee_coordinates = self.left_knee_coordinates

        if self.right_knee:
            self.right_knee_coordinates = self.right_knee[0][0 : 2]

            if self.mean_knee_coordinates == None:
                self.mean_knee_coordinates = self.right_knee_coordinates
            else:
                self.mean_knee_coordinates = tuple((left_knee_coordinate + right_knee_coordinate) / 2 for left_knee_coordinate, right_knee_coordinate in zip(self.mean_knee_coordinates, self.right_knee_coordinates))

        self.mean_ear_coordinates = None

        if self.left_ear:
            self.left_ear_coordinates = self.left_ear[0][0 : 2]
            self.mean_ear_coordinates = self.left_ear_coordinates

        if self.right_ear:
            self.right_ear_coordinates = self.right_ear[0][0 : 2]

            if self.mean_ear_coordinates == None:
                self.mean_ear_coordinates = self.right_ear_coordinates
            else:
                self.mean_ear_coordinates = tuple(left_ear_coordinate + right_ear_coordinate for left_ear_coordinate, right_ear_coordinate in zip(self.mean_ear_coordinates, self.right_ear_coordinates))


    def __is_rotated_trunk(self):
        self.rotated_trunk = False

        multiplier = 0.5

        if not self.left_shoulder or not self.right_shoulder:
            return

        shoulder_distance = get_distance(self.left_shoulder_coordinates, self.right_shoulder_coordinates)

        if not shoulder_distance or not self.left_elbow or not self.right_elbow:
            return

        left_shoulder_elbow_distance = get_distance(self.left_shoulder_coordinates, self.left_elbow_coordinates)
        right_shoulder_elbow_distance = get_distance(self.right_shoulder_coordinates, self.right_elbow_coordinates)

        if left_shoulder_elbow_distance and right_shoulder_elbow_distance:
            shoulder_elbow_distance = np.mean([left_shoulder_elbow_distance, right_shoulder_elbow_distance])
        elif not left_shoulder_elbow_distance:
            shoulder_elbow_distance = right_shoulder_elbow_distance
        elif not right_shoulder_elbow_distance:
            shoulder_elbow_distance = left_shoulder_elbow_distance
        else:
            return

        if shoulder_distance > multiplier * shoulder_elbow_distance:
            self.rotated_trunk = True


    def __get_trunk_angle(self):
        self.trunk_angle = None

        if self.rotated_trunk or not self.neck or not self.mean_hip_coordinates:
            return

        self.trunk_angle = get_angle(self.mean_hip_coordinates, self.neck_coordinates) - 90

        if not self.mean_knee_coordinates or not self.trunk_angle:
            return

        if np.sign(self.mean_knee_coordinates[0] - self.mean_hip_coordinates[0]) != np.sign(self.mean_hip_coordinates[0] - self.neck_coordinates[0]):
            self.trunk_angle = -self.trunk_angle


    def __get_trunk_neck_angle(self):
        self.trunk_neck_angle = None

        if not self.neck or not self.mean_ear_coordinates or not self.mean_hip_coordinates:
            return

        self.trunk_neck_angle = get_angle(self.mean_hip_coordinates, self.neck_coordinates, self.mean_ear_coordinates)


    def __is_rotated_neck(self):
        self.rotated_neck = False

        if self.rotated_trunk:
            self.rotated_neck = True

        if self.nose and self.left_eye and self.right_eye and self.left_ear and self.right_ear:
            self.rotated_neck = True

        if (not self.nose and not self.left_eye and not self.right_eye) or (self.left_ear and self.right_ear):
            self.rotated_neck = True


    def __get_neck_angle(self):
        self.neck_angle = None

        if self.rotated_neck or not self.neck or not self.mean_ear_coordinates:
            return

        self.neck_angle = get_angle(self.mean_ear_coordinates, self.neck_coordinates)

        if not self.neck_angle:
            return

        self.neck_angle = 90 - self.neck_angle

        if not self.nose:
            return

        if np.sign(self.nose_coordinates[0] - self.neck_coordinates[0]) != np.sign(self.mean_ear_coordinates[0] - self.neck_coordinates[0]):
            self.neck_angle = -self.neck_angle


    def __get_upper_arm_angle(self):
        self.left_upper_arm_angle = None
        self.right_upper_arm_angle = None

        if self.left_hip and self.left_shoulder and self.left_elbow:
            hip_coordinates = self.left_hip_coordinates
            shoulder_coordinates = self.left_shoulder_coordinates
            elbow_coordinates = self.left_elbow_coordinates

            self.left_upper_arm_angle = get_angle(hip_coordinates, shoulder_coordinates, elbow_coordinates)

        if self.right_hip and self.right_shoulder and self.right_elbow:
            hip_coordinates = self.right_hip_coordinates
            shoulder_coordinates = self.right_shoulder_coordinates
            elbow_coordinates = self.right_elbow_coordinates

            self.right_upper_arm_angle = get_angle(hip_coordinates, shoulder_coordinates, elbow_coordinates)


    def __get_elbow_angle(self):
        self.left_elbow_angle = None
        self.right_elbow_angle = None

        if self.left_shoulder and self.left_elbow and self.left_wrist:
            shoulder_coordinates = self.left_shoulder_coordinates
            elbow_coordinates = self.left_elbow_coordinates
            wrist_coordinates = self.left_wrist_coordinates

            self.left_elbow_angle = get_angle(shoulder_coordinates, elbow_coordinates, wrist_coordinates)

        if self.right_shoulder and self.right_elbow and self.right_wrist:
            shoulder_coordinates = self.right_shoulder_coordinates
            elbow_coordinates = self.right_elbow_coordinates
            wrist_coordinates = self.right_wrist_coordinates

            self.right_elbow_angle = get_angle(shoulder_coordinates, elbow_coordinates, wrist_coordinates)


    def __is_lateral_elbow(self):
        self.left_elbow_lateral = False
        self.right_elbow_lateral = False

        multiplier = 0.35

        if not self.mean_hip_coordinates or not self.mean_shoulder_coordinates:
            return

        hip_shoulder_distance = get_distance(self.mean_shoulder_coordinates, self.mean_hip_coordinates, type='vertical')

        if not hip_shoulder_distance:
            return

        if self.left_shoulder and self.left_elbow:
            shoulder_coordinates = self.left_shoulder_coordinates
            elbow_coordinates = self.left_elbow_coordinates

            left_elbow_shoulder_distance = get_distance(shoulder_coordinates, elbow_coordinates, type='vertical')

            if not left_elbow_shoulder_distance:
                return

            if left_elbow_shoulder_distance < multiplier * hip_shoulder_distance:
                self.left_elbow_lateral = True

        if self.right_shoulder and self.right_elbow:
            shoulder_coordinates = self.right_shoulder_coordinates
            elbow_coordinates = self.right_elbow_coordinates

            right_elbow_shoulder_distance = get_distance(shoulder_coordinates, elbow_coordinates, type='vertical')

            if not right_elbow_shoulder_distance:
                return

            if right_elbow_shoulder_distance < multiplier * hip_shoulder_distance:
                self.right_elbow_lateral = True


    def __is_horizontal_thigh(self):
        self.left_thigh_horizontal = True
        self.right_thigh_horizontal = True

        self.left_thigh_angle = None
        self.right_thigh_angle = None

        lower_angle_limit = 70
        upper_angle_limit = 110

        if self.left_shoulder and self.left_hip and self.left_knee:
            shoulder_coordinates = self.left_shoulder_coordinates
            hip_coordinates = self.left_hip_coordinates
            knee_coordinates = self.left_knee_coordinates

            self.left_thigh_angle = get_angle(shoulder_coordinates, hip_coordinates, knee_coordinates)

            if not self.left_thigh_angle:
                return

            if self.left_thigh_angle < upper_angle_limit or self.left_thigh_angle < lower_angle_limit:
                self.left_thigh_horizontal = False

        if self.right_shoulder and self.right_hip and self.right_knee:
            shoulder_coordinates = self.right_shoulder_coordinates
            hip_coordinates = self.right_hip_coordinates
            knee_coordinates = self.right_knee_coordinates

            self.right_thigh_angle = get_angle(shoulder_coordinates, hip_coordinates, knee_coordinates)

            if not self.right_thigh_angle:
                return

            if self.right_thigh_angle < upper_angle_limit or self.right_thigh_angle < lower_angle_limit:
                self.right_thigh_horizontal = False


    def __get_knee_angle(self):
        self.left_knee_angle = None
        self.right_knee_angle = None

        if self.left_hip and self.left_knee and self.left_ankle:
            hip_coordinates = self.left_hip_coordinates
            knee_coordinates = self.left_knee_coordinates
            ankle_coordinates = self.left_ankle_coordinates

            self.left_knee_angle = get_angle(hip_coordinates, knee_coordinates, ankle_coordinates)

        if self.right_hip and self.right_knee and self.right_ankle:
            hip_coordinates = self.right_hip_coordinates
            knee_coordinates = self.right_knee_coordinates
            ankle_coordinates = self.right_ankle_coordinates

            self.right_knee_angle = get_angle(hip_coordinates, knee_coordinates, ankle_coordinates)


    def get_trunk_condition(self):
        self.__is_rotated_trunk()
        self.__get_trunk_angle()
        self.__get_trunk_neck_angle()

        self.info['trunk_rotated'] = self.rotated_trunk
        self.info['trunk_angle'] = self.trunk_angle
        self.info['trunk_neck_angle'] = self.trunk_neck_angle


    def get_neck_condition(self):
        self.__is_rotated_neck()
        self.__get_neck_angle()

        self.info['neck_rotated'] = self.rotated_neck
        self.info['neck_angle'] = self.neck_angle


    def get_upper_arm_condition(self):
        self.__get_upper_arm_angle()

        self.info['left_upper_arm_angle'] = self.left_upper_arm_angle
        self.info['right_upper_arm_angle'] = self.right_upper_arm_angle


    def get_elbow_condition(self):
        self.__is_lateral_elbow()
        self.__get_elbow_angle()

        self.info['left_elbow_lateral'] = self.left_elbow_lateral
        self.info['right_elbow_lateral'] = self.right_elbow_lateral
        self.info['left_elbow_angle'] = self.left_elbow_angle
        self.info['right_elbow_angle'] = self.right_elbow_angle


    def get_thigh_condition(self):
        self.__is_horizontal_thigh()

        self.info['left_thigh_horizontal'] = self.left_thigh_horizontal
        self.info['right_thigh_horizontal'] = self.right_thigh_horizontal
        self.info['left_thigh_angle'] = self.left_thigh_angle
        self.info['right_thigh_angle'] = self.right_thigh_angle


    def get_knee_condition(self):
        self.__get_knee_angle()

        self.info['left_knee_angle'] = self.left_knee_angle
        self.info['right_knee_angle'] = self.right_knee_angle


    def get_info(self):
        return self.info