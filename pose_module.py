import cv2
import mediapipe as mp
import numpy as np

class PoseDetector():

    def __init__(self, static_image_mode=False, model_complexity=1, smooth_landmarks=True, enable_segmentation=True, smooth_segmentation=True, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.static_image_mode = static_image_mode
        self.model_complexity = model_complexity
        self.smooth_landmarks = smooth_landmarks
        self.enable_segmentation = enable_segmentation
        self.smooth_segmentation = smooth_segmentation
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.static_image_mode, self.model_complexity, self.smooth_landmarks,
                                     self.enable_segmentation, self.smooth_segmentation,
                                     self.min_detection_confidence, self.min_tracking_confidence)

    def get_pose(self, frame, draw=True):
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(frameRGB)

        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(frame, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS,
                                        connection_drawing_spec=self.mpDraw.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2))

        return frame


    def get_position(self, frame, draw=True):
        self.landmarks = []

        if self.results.pose_landmarks:
            for id, landmark in enumerate(self.results.pose_landmarks.landmark):
                height, width, _ = frame.shape
                cx, cy, z, visibility = int(landmark.x * width), int(landmark.y * height), landmark.z, landmark.visibility
                self.landmarks.append({'id': id, 'cx': cx, 'cy': cy, 'z': z, 'visibility': visibility})
                if draw:
                    cv2.circle(frame, (cx, cy), 5, (255, 0, 0), cv2.FILLED)

        return self.landmarks


    def get_segmentation_mask(self, frame):
        segmentation_mask = self.results.segmentation_mask
        segmentation_mask = np.repeat(segmentation_mask[:, :, np.newaxis], 3, axis=2) * 255
        segmentation_mask = cv2.cvtColor(segmentation_mask, cv2.COLOR_BGR2GRAY)
        segmentation_mask = segmentation_mask.astype(np.uint8)

        kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (25, 25))
        dilated_mask = cv2.dilate(segmentation_mask, kernel, iterations=1)

        return dilated_mask