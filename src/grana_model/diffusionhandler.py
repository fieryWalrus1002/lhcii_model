from src.grana_model.particle import Particle
import itertools
import numpy as np
from sklearn.utils.extmath import cartesian
import pandas as pd
import time


class DiffusionHandler:
    def __init__(self):
        self.diffusion_state = False

    def toggle_diffusion_state(self):
        if self.diffusion_state is False:
            print("diffusion_state = true")
            self.diffusion_state = True
        else:
            print("diffusion_state = false")
            self.diffusion_state = False

    def handle_diffusion(self, object_list: list[Particle]):
        if self.diffusion_state is False or len(object_list) < 1:
            return

        for object in object_list:
            object.diffusion_move(object.diffusion_distance)


class LHCIIAttractionHandler:
    """
    handles the calculation of attraction vectors between objects and their
    attraction points

    distance_threshold : determines the maximum distance between two objects before
                        their attraction vectors will no longer possibly affect each other.
    """

    def __init__(self, distance_threshold: float = 1000.0):
        self.distance_threshold = distance_threshold
        self.points_to_draw = []
        self.enabled = False

    def reset_vectors_for_all_objects(self, object_list):
        for o in object_list:
            o.vector_list = []

    def toggle_attraction_forces(self):
        if self.enabled == False:
            self.enabled = True
        else:
            self.enabled = False

    def get_points_to_draw(self, object_list: list):
        """ go through the object list and calculate the world coordinates for each
        of the attraction points. return the list of coordinates so they can be drawn
        """

        points_to_draw = []

        for o in object_list:
            o_points = o.get_attraction_points()
    
            for p in o_points:
                points_to_draw.append(p.get_world_coords())

        return points_to_draw

    def calculate_attraction_forces(self, object_list):
        """
        get a list of all combinations of objects, and calculate the forces between
        each of them that are within a certain distance threshold
        """

        # create list of all combinations of objects that can attract each other
        all_combinations = itertools.combinations(object_list, 2)

        # filter by distance_threshold
        for o1, o2 in all_combinations:
            # check to see if they objects are within a certain distance threshold. if
            # they are outside, we won't bother calculating attraction vectors
            dist = o1.body.position.get_distance(o2.body.position)

            if dist < self.distance_threshold:
                # calculate all the vectors for object 1 toward object 2
                o1.calculate_attraction_to_object(o2)

                # then calculate all vectors for object 2 toward object
                o2.calculate_attraction_to_object(o1)

    def apply_all_vectors(self, object_list, rotation_scalar: float = 1.0, attraction_enabled: bool = False):
        for o in object_list:
            o.apply_vectors(attraction_enabled)
            o.thermal_rotation(rotation_scalar=rotation_scalar)


