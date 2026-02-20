import cv2
import mediapipe as mp
import numpy as np

mp_pose = mp.solutions.pose

def extract_body_features(image_path):
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    with mp_pose.Pose(static_image_mode=True) as pose:
        results = pose.process(image_rgb)

        if not results.pose_landmarks:
            return None

        landmarks = results.pose_landmarks.landmark

        shoulder_width = abs(
            landmarks[11].x - landmarks[12].x
        )

        hip_width = abs(
            landmarks[23].x - landmarks[24].x
        )

        body_ratio = shoulder_width / hip_width

        return {
            "shoulder_width": float(shoulder_width),
            "hip_width": float(hip_width),
            "body_ratio": float(body_ratio)
        }