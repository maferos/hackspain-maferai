"""Validate catalogue populations against the compiled rail camera scene."""
import json
import unittest

import mujoco
import numpy as np

from scene_patterns import CATALOGUE, PATTERNS, SIM, build_pattern


class ScenePatternsTest(unittest.TestCase):
    def test_catalogue_counts_and_world_poses(self):
        scene = SIM / 'models/minihannover_rail_scene.xml'
        original = scene.read_bytes()
        self.assertEqual(len(CATALOGUE), 10)
        for entry in CATALOGUE:
            with self.subTest(pattern=entry['pattern']):
                model, info = build_pattern(scene, entry['pattern'])
                data = mujoco.MjData(model)
                mujoco.mj_forward(model, data)
                population = json.loads((PATTERNS / entry['file']).read_text())
                roots = [model.body(i).name for i in range(model.nbody)
                         if model.body_parentid[i] == 0]
                self.assertFalse(any(name.startswith('loose_') for name in roots))
                self.assertEqual(sum(name.startswith('dyn_') for name in roots), info['count'])
                self.assertEqual(info['count'], sum(
                    item['container_ml'] != 10 for item in population['containers']))
                for item in population['containers']:
                    if item['container_ml'] == 10:
                        self.assertNotIn('dyn_' + item['sample_id'], roots)
                        continue
                    body = data.body('dyn_' + item['sample_id'])
                    np.testing.assert_allclose(body.xpos,
                                               [item['x'] - 1.5, item['y'] - .4, .9])
                self.assertGreaterEqual(model.camera('general').id, 0)
                self.assertGreaterEqual(model.camera('arm_eih').id, 0)
        self.assertEqual(scene.read_bytes(), original)


if __name__ == '__main__':
    unittest.main()
