# Body Parts Indexes:
#   nose -> [0]
#   neck -> [1]
#   right_shoulder -> [2]
#   right_elbow -> [3]
#   right_wrist -> [4]
#   left_shoulder -> [5]
#   left_elbow -> [6]
#   left_wrist -> [7]
#   right_hip -> [8]
#   right_knee -> [9]
#   right_ankle -> [10]
#   left_hip -> [11]
#   left_knee -> [12]
#   left_ankle -> [13]
#   right_eye -> [14]
#   left_eye -> [15]
#   right_ear -> [16]
#   left_ear -> [17]

import cv2

GREEN = (0, 255, 0)
RED = (0, 0, 255)

class PostureAnalyzer:
    def __init__(self, body_marks, shap_values: dict, image, is_incorrect: bool):
        self.body_marks = body_marks
        self.__set_body_parts_indexes()
        self.__set_body_parts_keys()

        self.shap = shap_values
        self.image = image.copy()

        self.colors = [GREEN for _ in range(18)]
        if is_incorrect:
            self.set_key_for_max_shap(shap_values)
            self.set_color_map()


    def __set_body_parts_indexes(self):
        self.head_indexes = [0, 1, 14, 15, 16, 17]
        self.neck_indexes = [1]
        self.upper_trunk_indexes = [2, 5]
        self.lower_trunk_indexes = [8, 11]
        self.right_arm_indexes = [2, 3, 4]
        self.left_arm_indexes = [5, 6, 7]
        self.right_leg_indexes = [8, 9, 10]
        self.left_leg_indexes = [11, 12, 13]

    def __set_body_parts_keys(self):
        self.neck_keys = ["trunk_neck_angle", "neck_rotated", "neck_angle"]
        self.trunk_keys = ["trunk_rotated", "trunk_angle"]
        self.right_arm_keys = ["right_upper_arm_angle", "right_elbow_lateral", "right_elbow_angle"]
        self.left_arm_keys = ["left_upper_arm_angle", "left_elbow_lateral", "left_elbow_angle"]
        self.leg_keys = ["right_thigh_horizontal", "right_thigh_angle", "right_knee_angle", "left_thigh_horizontal", "left_thigh_angle", "left_knee_angle"]


    
    def set_key_for_max_shap(self, shap: dict):
        key = max(self.shap, key=lambda k : shap[k])
        self.key_max_shap = key

    def set_color_map(self):
        if self.key_max_shap in self.neck_keys:
            self.__set_color_in_indexes(self.neck_indexes, RED)
            self.__set_color_in_indexes(self.upper_trunk_indexes, RED)
            self.__set_color_in_indexes(self.head_indexes, RED)
        
        if self.key_max_shap in self.trunk_keys:
            self.__set_color_in_indexes(self.upper_trunk_indexes, RED)
            self.__set_color_in_indexes(self.lower_trunk_indexes, RED)
            self.__set_color_in_indexes(self.neck_indexes, RED)
        
        if self.key_max_shap in self.right_arm_keys:
            self.__set_color_in_indexes(self.right_arm_indexes, RED)
        
        if self.key_max_shap in self.left_arm_keys:
            self.__set_color_in_indexes(self.left_arm_indexes, RED)
        
        if self.key_max_shap in self.leg_keys:
            self.__set_color_in_indexes(self.right_leg_indexes, RED)
            self.__set_color_in_indexes(self.left_leg_indexes, RED)

    
    def __set_color_in_indexes(self, indexes: list, color: tuple):
        self.colors = [color if i in indexes else self.colors[i] for i in range(len(self.colors))]
    

    def explain_image(self):
        for i, body_mark in enumerate(self.body_marks):
            if body_mark and self.colors[i]:
                cv2.circle(self.image, body_mark[0][0:2], 5, self.colors[i], -1)

        return self.image