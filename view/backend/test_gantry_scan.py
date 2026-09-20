"""Cartesian limits and path clearance must fail before the live state moves."""
import unittest
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

import mujoco
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'simulation/scripts'))
from gantry_motion import move_to, SITE
from gantry_scan import CAMERA_CLEAR, path
from scene_patterns import pattern_scene
from generate_gantry_scene import OUT


class GantryScanTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root, _ = pattern_scene(OUT, 'p01')
        # Place an obstacle at a destination that is otherwise within XYZ travel.
        ET.SubElement(root.find('worldbody'), 'geom', name='test_obstacle',
                      type='box', pos='-.5 -.4 1.50', size='.15 .15 .25')
        cls.model = mujoco.MjModel.from_xml_string(ET.tostring(root, encoding='unicode'))

    def setUp(self):
        self.data = mujoco.MjData(self.model)
        mujoco.mj_forward(self.model, self.data)

    def test_upper_limit_roundoff_does_not_block_a_raised_move(self):
        goal = self.data.site(SITE).xpos.copy()
        goal[2] += 1e-12
        move_to(self.model, self.data, goal)
        self.assertAlmostEqual(self.data.qpos[self.model.joint('gantry_z').qposadr[0]], 0)

    def test_unreachable_target_preserves_live_state(self):
        before = self.data.qpos.copy()
        with self.assertRaises(ValueError):
            path(self.model, self.data, np.array([20, 0, 1.4]))
        np.testing.assert_array_equal(self.data.qpos, before)

    def test_obstacle_rejects_the_entire_move_before_execution(self):
        before = self.data.qpos.copy()
        with self.assertRaisesRegex(ValueError, 'blocked'):
            path(self.model, self.data, np.array([-.5, -.4, 1.3251]))
        np.testing.assert_array_equal(self.data.qpos, before)

    def test_the_lens_is_what_stops_the_hand_going_lower(self):
        """The cage could go around a flask; the camera under it could not.

        The lens hangs further below the pinch site than the cage reaches, so
        planting at the arm's grasp height would put it through the worktop and
        the path check refuses the whole move. On this machine the hand stands
        on the vessel instead, and this is the number that says how high.
        """
        import vision_pick as vp
        camera = self.data.cam_xpos[self.model.camera('arm_eih').id]
        drop = float(self.data.site(SITE).xpos[2] - camera[2])
        floor = vp.rk.BENCH_TOP + drop + CAMERA_CLEAR
        grasp = vp.rk.BENCH_TOP + vp.grasp_height(self.model, 0.14)
        self.assertGreater(floor, grasp)                # the lens, not the cage, decides
        self.assertGreater(floor - CAMERA_CLEAR, vp.rk.BENCH_TOP)

    def test_clear_path_raises_before_translating(self):
        move_to(self.model, self.data, np.array([-3, -.4, 1.3251]))
        points = path(self.model, self.data, np.array([-2.5, -.2, 1.3251]))
        np.testing.assert_allclose(points[0][:2], points[1][:2])
        self.assertGreater(points[1][2], points[0][2])
        self.assertEqual(points[1][2], points[2][2])
        np.testing.assert_allclose(points[2][:2], points[3][:2])


    def test_level_scan_leg_does_not_raise_between_vessels(self):
        move_to(self.model, self.data, np.array([-3, -.4, 1.3251]))
        points = path(self.model, self.data, np.array([-2.5, -.2, 1.3251]), level=True)
        self.assertEqual(len(points), 2)
        np.testing.assert_allclose([p[2] for p in points], [1.3251, 1.3251])

    def test_level_scan_rejects_a_vertical_change(self):
        move_to(self.model, self.data, np.array([-3, -.4, 1.3251]))
        with self.assertRaisesRegex(ValueError, 'change height'):
            path(self.model, self.data, np.array([-2.5, -.2, 1.5]), level=True)


if __name__ == '__main__':
    unittest.main()
