import unittest

from grana_model.objectdata import ObjectData


class TestObjectData(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.obj_data = ObjectData(
            pos_csv_filename="082620_SEM_final_coordinates.csv"
        )

    def test_object_data_length(self):
        self.assertEqual(len(self.obj_data.pos_list), 211)

    def test_object_generation(self):
        next_obj = next(self.obj_data.object_list)
        self.assertIsNotNone(next_obj)

    def test_object_value_types(self):
        obj = next(self.obj_data.object_list)
        self.assertIsInstance(obj["obj_type"], str)
        self.assertIsInstance(obj["pos"], list)


unittest.main()
