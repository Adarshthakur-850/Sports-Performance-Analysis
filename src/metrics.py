import numpy as np
import time

class PerformanceMetrics:
    def __init__(self, pixel_to_meter_ratio=0.01):
        self.pixel_to_meter = pixel_to_meter_ratio
        self.total_distance = 0.0
        self.current_speed = 0.0
        self.prev_pos = None
        self.prev_time = time.time()
        self.trajectory = []
        
    def update(self, current_pos_norm, frame_width, frame_height):
        """
        current_pos_norm: (x, y) normalized [0, 1]
        """
        if current_pos_norm is None:
            return self.total_distance, 0.0
            
        # Convert to pixels
        curr_x = current_pos_norm[0] * frame_width
        curr_y = current_pos_norm[1] * frame_height
        current_pos = np.array([curr_x, curr_y])
        
        current_time = time.time()
        
        if self.prev_pos is not None:
            # Time delta
            dt = current_time - self.prev_time
            
            # Reset if gap is too large (e.g. lost tracking for > 2 seconds)
            if dt > 2.0:
                self.prev_pos = current_pos
                self.prev_time = current_time
                return self.total_distance, 0.0
            
            # Distance in pixels
            dist_px = np.linalg.norm(current_pos - self.prev_pos)
            
            # Meters
            dist_m = dist_px * self.pixel_to_meter
            
            if dt > 0:
                self.current_speed = (dist_m / dt) * 3.6 # km/h
                
            self.total_distance += dist_m
            
        self.prev_pos = current_pos
        self.prev_time = current_time
        
        # Store trajectory
        self.trajectory.append((int(curr_x), int(curr_y)))
        if len(self.trajectory) > 100: # Keep last 100 points
            self.trajectory.pop(0)
            
        return self.total_distance, self.current_speed
        
    def get_heatmap_grid(self, width, height, grid_size=50):
        # Generate simple heatmap data (counts per grid cell)
        heatmap = np.zeros((height // grid_size, width // grid_size))
        for x, y in self.trajectory:
            grid_x = min(x // grid_size, heatmap.shape[1] - 1)
            grid_y = min(y // grid_size, heatmap.shape[0] - 1)
            heatmap[grid_y, grid_x] += 1
        return heatmap
