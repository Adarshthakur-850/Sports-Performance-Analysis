# Real-Time Sports Performance Analysis

Computer Vision system to track player movement and calculate metrics like speed and distance covered.

## Features
- **Pose Tracking**: Uses MediaPipe to track player center of mass.
- **Metrics**: Real-time calculation of Distance (m) and Speed (km/h).
- **Visualization**: Trajectory overlay and live stats dashboard on video.
- **Logging**: Saves session data to CSV.

## Dependencies
```bash
pip install -r requirements.txt
```

## Usage
1. Connect a webcam.
2. Run the analyzer:
   ```bash
   python main.py
   ```
3. Stand in front of the camera. The system will track your hip movement.
4. Press `q` to stop.
