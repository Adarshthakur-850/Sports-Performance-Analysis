import cv2
import numpy as np
import mediapipe as mp

class Visualizer:
    def __init__(self):
        pass
        
    def draw_overlay(self, frame, stats, trajectory):
        dist, speed = stats
        
        # Info Panel
        cv2.rectangle(frame, (10, 10), (250, 100), (0, 0, 0), -1)
        cv2.putText(frame, f"Dist: {dist:.2f} m", (20, 40), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"Speed: {speed:.2f} km/h", (20, 80), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                   
        # Trajectory
        if len(trajectory) > 1:
            # Ensure points are integers for OpenCV
            points = np.array(trajectory, dtype=np.int32)
            cv2.polylines(frame, [points], False, (0, 0, 255), 2)
                
        return frame
        
    def draw_landmarks(self, frame, landmarks, mp_pose):
        mp.solutions.drawing_utils.draw_landmarks(
            frame, landmarks, mp_pose.POSE_CONNECTIONS)
        return frame
