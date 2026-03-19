import unittest
from src.metrics import PerformanceMetrics
import time

class TestPerformanceMetrics(unittest.TestCase):
    def test_tracking_lost_returns_zero(self):
        metrics = PerformanceMetrics()
        
        # Frame 1: Valid position
        metrics.update((0.5, 0.5), 1000, 1000)
        
        # Frame 2: Valid position (moved)
        time.sleep(0.1)
        dist, speed = metrics.update((0.6, 0.5), 1000, 1000)
        self.assertGreater(dist, 0)
        
        # Frame 3: Tracking lost
        dist_lost, speed_lost = metrics.update(None, 1000, 1000)
        
        print(f"Distance when tracking lost: {dist_lost}")
        
        # Expectation: Should return total distance, not 0
        self.assertEqual(dist_lost, dist, "Distance should persist when tracking is lost")

if __name__ == '__main__':
    unittest.main()
