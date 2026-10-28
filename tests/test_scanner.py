import math
import unittest

from pi_scan_radar.models import ScanSample
from pi_scan_radar.scanner import cluster_detections, median_filter, sweep_angles
from pi_scan_radar.simulation import CircleObstacle, ray_circle_distance


class ScannerTests(unittest.TestCase):
    def test_sweep_includes_endpoints(self):
        self.assertEqual(sweep_angles(-5, 5, 4), [-5, -1, 3, 5])
        self.assertEqual(sweep_angles(-5, 5, 5, reverse=True), [5, 0, -5])

    def test_ray_hits_centered_obstacle(self):
        distance = ray_circle_distance(0, CircleObstacle(0, 2, 0.25))
        self.assertTrue(math.isclose(distance or 0, 1.75))
        self.assertIsNone(ray_circle_distance(45, CircleObstacle(0, 2, 0.25)))

    def test_median_filter_rejects_spike(self):
        values = [1.0, 8.0, 1.1]
        samples = [ScanSample(index, value, index) for index, value in enumerate(values)]
        self.assertEqual(median_filter(samples)[1].distance_m, 1.1)

    def test_clusters_adjacent_returns(self):
        samples = [
            ScanSample(-20, 1.2, 0), ScanSample(-17, 1.1, 1),
            ScanSample(10, 0.8, 2), ScanSample(13, 0.9, 3),
            ScanSample(50, None, 4, False),
        ]
        detections = cluster_detections(samples, 2.0, 4.0)
        self.assertEqual(len(detections), 2)
        self.assertEqual(detections[0].sample_count, 2)
        self.assertEqual(detections[1].nearest_distance_m, 0.8)


if __name__ == "__main__":
    unittest.main()
