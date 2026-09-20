"""Failure cases must leave the viewport responsive, without synthetic motion."""
import threading
import os
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

from live_scan import LiveScan, vp


class LiveScanTest(unittest.TestCase):
    def test_environment_cannot_override_pinned_model(self):
        weights = Path(__file__)
        with patch.dict(os.environ, {'VIEW_DETECTOR': 'rail', 'VIEW_DETECTOR_CONF': '0.10'}), \
             patch('live_scan.DETECTOR_WEIGHTS', weights), \
             patch('live_scan.ScanDetector') as detector, \
             patch('live_scan.ScanPerception'), patch.object(vp, 'controller'):
            scan = LiveScan(Mock(), SimpleNamespace(time=0), threading.Lock(), 3)
            self.assertIsNone(scan.error)
            detector.assert_called_once_with(weights, 0.41)

    def test_missing_weights_is_visible_without_falling_back(self):
        with patch('live_scan.DETECTOR_WEIGHTS', Path('/missing/yolo26n_full_1920_e25.pt')):
            scan = LiveScan(Mock(), SimpleNamespace(time=0), threading.Lock(), 3)
        self.assertEqual(scan.snapshot()['status'], 'error')
        self.assertIn('yolo26n_full_1920_e25.pt', scan.error)
        self.assertIsNone(scan.perception)
        scan.advance(1 / 15)
        scan.close()

    def test_original_controller_system_exit_becomes_scan_error(self):
        scan = LiveScan.__new__(LiveScan)
        scan.error = None
        scan.world = vp.World(auto=False)
        scan.world.cycles = 1
        scan.perception = Mock()
        scan.perception.finished.is_set.return_value = False
        scan.perception.ready.is_set.return_value = True
        scan.model = SimpleNamespace(opt=SimpleNamespace(timestep=0.002))

        def failed_controller():
            raise SystemExit('no carry pose the arm can reach')
            yield

        scan.controller = failed_controller()
        scan.advance(1 / 15)
        self.assertIn('no carry pose', scan.error)
        # An error must remain stable on later frames, not continue the generator.
        scan.advance(1 / 15)
        self.assertIn('no carry pose', scan.error)

    def test_perception_failure_stops_control(self):
        scan = LiveScan.__new__(LiveScan)
        scan.error = None
        scan.perception = Mock(error='YOLO worker stopped')
        scan.perception.finished.is_set.return_value = True
        scan.controller = Mock()
        scan.advance(1 / 15)
        self.assertEqual(scan.error, 'YOLO worker stopped')
        scan.controller.assert_not_called()


if __name__ == '__main__':
    unittest.main()
