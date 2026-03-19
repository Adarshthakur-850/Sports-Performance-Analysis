import sys
import os

print(f"Python Executable: {sys.executable}")
try:
    import mediapipe
    print(f"MediaPipe Version: {getattr(mediapipe, '__version__', 'Unknown')}")
    print(f"MediaPipe File: {mediapipe.__file__}")
    print(f"Dir(mediapipe): {dir(mediapipe)}")
    
    if hasattr(mediapipe, 'solutions'):
        print("mediapipe.solutions FOUND")
    else:
        print("mediapipe.solutions NOT FOUND")
        
        # Try direct import
        try:
            from mediapipe.python import solutions
            print("Successfully imported mediapipe.python.solutions")
        except ImportError as e:
            print(f"Failed to import mediapipe.python.solutions: {e}")

except ImportError as e:
    print(f"ImportError: {e}")
