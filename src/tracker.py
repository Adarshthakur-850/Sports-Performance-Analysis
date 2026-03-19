import mediapipe as mp
import cv2
import numpy as np

class PlayerTracker:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
            model_complexity=1
        )
        self.prev_landmarks = None

    def detect(self, frame):
        # Convert BGR to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(frame_rgb)
        
        if results.pose_landmarks:
            # Extract center of mass (Approximate using hips)
            left_hip = results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_HIP]
            right_hip = results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_HIP]
            
            # Average hip position as player center
            cx = (left_hip.x + right_hip.x) / 2
            cy = (left_hip.y + right_hip.y) / 2
            
            return (cx, cy), results.pose_landmarks
            
        return None, None
