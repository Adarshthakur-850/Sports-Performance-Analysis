import unittest
from src.metrics import PerformanceMetrics
import time

class TestMetricsFix(unittest.TestCase):
    def test_tracking_lost_persistence(self):
        """Test that distance persists when tracking is lost (input is None)"""
        metrics = PerformanceMetrics()
        
        # 1. Initial movement
        metrics.update((0.5, 0.5), 1000, 1000)
        time.sleep(0.01)
        dist, _ = metrics.update((0.6, 0.5), 1000, 1000)
        
        self.assertGreater(dist, 0, "Distance should be accumulating")
        
        # 2. Lost tracking
        dist_lost, speed_lost = metrics.update(None, 1000, 1000)
        
        self.assertEqual(dist_lost, dist, "Distance should remain constant when tracking is lost")
        self.assertEqual(speed_lost, 0.0, "Speed should be 0 when tracking is lost")
        
    def test_time_gap_reset(self):
        """Test that large time gaps reset speed calculation prevents spikes"""
        metrics = PerformanceMetrics()
        
        # 1. Normal movement
        metrics.update((0.5, 0.5), 1000, 1000)
        time.sleep(0.1)
        metrics.update((0.51, 0.5), 1000, 1000)
        
        # 2. Simulate large gap (> 2.0s)
        # We manually mod prev_time to simulate delay without waiting 2s
        metrics.prev_time = time.time() - 3.0 
        
        # Update with movement
        current_dist = metrics.total_distance
        dist, speed = metrics.update((0.6, 0.5), 1000, 1000)
        
        self.assertEqual(speed, 0.0, "Speed should be 0 after large time gap")
        self.assertEqual(dist, current_dist, "Distance should not increment on the reset frame")
        
        # 3. Next frame should be normal
        time.sleep(0.1)
        dist_next, speed_next = metrics.update((0.61, 0.5), 1000, 1000)
        self.assertGreater(speed_next, 0, "Speed should resume normally after reset")

if __name__ == '__main__':
    unittest.main()
