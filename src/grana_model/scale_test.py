from pyglet.graphics import Batch
from grana_model.objectdata import ObjectData
from random import random
from math import cos, sin, pi
from pymunk import Body, Poly, Space


class TestObject:
    def __init__(
        self,
        space: Space,
        batch: Batch,
        position: tuple,
        coordinates: list,
        color: tuple,
        type: str,
    ):

        self.body = Body(mass=100, moment=100, body_type=Body.KINEMATIC)

        self.body.position = position  # given pos
        self.shape = Poly(self.body, vertices=coordinates)
        self.angle = 0.0
        self.shape.color = color
        self.type = type
        self.shape.collision_type = 1

        space.add(self.body, self.shape)

    def update_sprite(self, sprite_scale_factor, rotation_factor):
        # take these and throw them in the trash
        trash_can = []
        trash_can.append(sprite_scale_factor)
        trash_can.append(rotation_factor)

    @property
    def area(self):
        """gets the total area of the object, by adding up the area of
        all of its indiviudal shapes. called as a property"""
        total_area = 0.0

        for shape in self.body.shapes:
            total_area += shape.area
        return total_area


class Spawner:
    """handles instantiation of objects into the simulation window, and for now
    has a random_pos_in_circle function because where else should it go"""

    def __init__(
        self,
        object_data: ObjectData,
        shape_type: str,
        space: Space,
        batch: Batch,
        spawn_type: str,
    ):
        self.object_data = object_data
        self.particle_count = 1000
        self.ratio_free_LHC = 2.00  # Helmut says "Assuming that you have 212 PSII (dimer =C2) particles then LHCII should be 424 (2xPSII)"
        self.num_cytb6f = 70  # 083021: Helmut says cyt b6f 70 (1/3 x PSII)
        self.shape_type = shape_type
        self.spawn_type = spawn_type
        self.space = space
        self.batch = batch

    def random_pos_in_circle(self, max_radius, center):
        rand_roll = random() + random()

        if rand_roll > 1:
            r = (2 - rand_roll) * max_radius
        else:
            r = rand_roll * max_radius

        t = 2 * pi * random()

        return [(r * cos(t)) + center[0], center[1] + (r * sin(t))]

    def setup_model(self, num_particles=0):
        # sets up the simulation with a certain test set of objects

        position_list = [
            (100.0, 100.0),
            (300.0, 100.0),
            (100.0, 300.0),
            (200.0, 200.0),
        ]

        color_list = [
            (255, 255, 255, 255),
            (255, 0, 0, 255),
            (0, 255, 0, 255),
            (0, 0, 255, 255),
        ]

        shape_list = [
            [
                (9.856115108, -0.071942446),
                (6.007194245, 12.51798561),
                (-10.89928058, 13.66906475),
                (-11.43884892, 1.834532374),
                (-6.18705036, -12.55395683),
                (8.309352518, -13.48920863),
                (11.47482014, -8.129496403),
            ],  # super simple c2s2m2
            [
                (12.51798561, 1.007194245),
                (-12.48201439, 1.007194245),
                (-12.48201439, 0),
                (12.51798561, 0),
            ],  # 25nm scale bar
            [(5.0, 0.0), (5.0, 5.0), (0.0, 5.0), (0.0, 0.0)],  # 25nm square
            [(50.0, 0), (50.0, 10.0), (-50.0, 10.0), (-50.0, 0.0),],  # 100nm scale bar
        ]
        type_list = ["c2s2m2", "25nm_scalebar", "5nm_square", "100nm_scalebar"]
        # object_list = [
        #     TestObject(
        #         space=self.space,
        #         batch=self.batch,
        #         type=obj_type,
        #         position=position,
        #         coordinates=coordinate_list,
        #         color=color,
        #     )
        #     for coordinate_list, color, position, obj_type in zip(
        #         shape_list, color_list, position_list, type_list
        #     )
        # ]

        object_list = [
            TestObject(
                space=self.space,
                batch=self.batch,
                type=type_list[0],
                position=self.random_pos_in_circle(max_radius=200, center=(200, 200)),
                coordinates=shape_list[0],
                color=color_list[0],
            )
            for _ in range(0, 211)
        ]
        return object_list, []
