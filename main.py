import cv2
import pandas as pd
import time
import os
from src.tracker import PlayerTracker
from src.metrics import PerformanceMetrics
from src.visualizer import Visualizer

def main():
    print("Starting Sports Performance Analysis...")
    print("Opening Webcam... (Press 'q' to exit)")
    
    cap = cv2.VideoCapture(0)
    tracker = PlayerTracker()
    metrics = PerformanceMetrics(pixel_to_meter_ratio=0.005) # Adjust scale as needed
    visualizer = Visualizer()
    
    # Data Logging
    if not os.path.exists("data"): os.makedirs("data")
    log_file = "data/logs.csv"
    logs = []
    
    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
                
            frame = cv2.flip(frame, 1) # Mirror view for webcam
            h, w, _ = frame.shape
            
            # 1. Track
            pos_norm, landmarks = tracker.detect(frame)
            
            # 2. Metrics
            dist, speed = metrics.update(pos_norm, w, h)
            
            # 3. Visualize
            if landmarks:
                frame = visualizer.draw_landmarks(frame, landmarks, tracker.mp_pose)
                
            frame = visualizer.draw_overlay(frame, (dist, speed), metrics.trajectory)
            
            # 4. Log
            logs.append({
                'timestamp': time.time(),
                'distance': dist,
                'speed': speed
            })
            
            cv2.imshow('Sports Performance Analytics', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        
        # Save Logs
        df = pd.DataFrame(logs)
        df.to_csv(log_file, index=False)
        print(f"Session saved to {log_file}")

if __name__ == "__main__":
    main()
