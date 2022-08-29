import unittest
import sys
from grana_model.spawner import Spawner
from grana_model.objectdata import ObjectData
import pymunk
import pyglet


class TestSpawner(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        obj_data = ObjectData(
            pos_csv_filename="082620_SEM_final_coordinates.csv"
        )
        cls.spawner = Spawner(object_data=obj_data)
        cls.space = pymunk.Space()
        cls.batch = pyglet.graphics.Batch()
        cls.structure_list = cls.spawner.spawn_psii(
            space=cls.space, batch=cls.batch
        )

    def test_spawner_return_type(self):
        self.assertIsInstance(
            self.spawner.spawn_psii(space=self.space, batch=self.batch), list
        )

    def test_spawner_has_object_data_attached(self):
        self.assertEqual(len(self.spawner.object_data.pos_list), 211)

    def test_spawn_particle_number(self):
        particle_list = self.spawner.spawn_particles(
            space=self.space, k=10, batch=self.batch
        )
        self.assertEqual(len(particle_list), 10)

    def test_spawn_psii_number(self):
        self.assertEqual(len(self.structure_list), 211)


unittest.main()
