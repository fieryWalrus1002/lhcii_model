from pyglet.text import Label
from math import pi
from pyglet.shapes import Circle, Rectangle
import pymunk

# colors for objects in sim window
out_color = (
    250,
    0,
    0,
    50,
)
in_color = (0, 51, 0, 255)  # usual LHCII color


class DensityHandler:
    def __init__(
        self,
        space,
        x: float = 150.0,
        y: float = 150.0,
        width: int = 100,
        height: int = 100,
    ):
        self.space = space
        self.num_objects = 0
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.area_counter = 0
        self.internal_area = 0
        self.total_area = 0
        self.ensemble_area = width * height
        self.in_color = in_color
        self.out_color = out_color

    def draw_density_label(self, label_pos: tuple = (200, 300)):
        area_text = (
            f"ensemble density: {self.internal_area / (self.ensemble_area)}"
        )
        area_label = Label(
            area_text,
            font_name="Times New Roman",
            font_size=5,
            x=label_pos[0],
            y=label_pos[1],
        )
        area_label.draw()
        print(f"ensemble density = {self.internal_area / (self.ensemble_area)}")

    def draw_rectangle(self, opacity: int = 75, color: tuple = (255, 0, 0)):
        rectangle = Rectangle(self.x, self.y, self.width, self.height, color=color)
        rectangle.opacity = opacity
        rectangle.draw()

    def update_area_calculations(self, obstacle_list):
        self.area_counter += 1

        total_area = 0.0
        internal_area = 0.0

        for o in obstacle_list:

            for s in o.shape_list:
                total_area += s.area

                if s.color != self.out_color:
                    internal_area += s.area

        self.internal_area = internal_area
        self.total_area = total_area
        return internal_area, total_area

    def create_ensemble_area_sensor(self):
        """ create a sensor box for the ensemble, that will be used to detect what 
        shapes are within the 100x100nm box when determing area """

        boundary_color = (0, 1, 1, 0)
        body = pymunk.Body(pymunk.Body.STATIC)
        body.position = (250, 250)
        shape = pymunk.Poly.create_box(body, (100, 100), radius=1)
        shape.color = boundary_color
        # shape.mass = 1000000
        shape.collision_type = 3  # boundary
        shape.sensor = True
        # shape.elasticity = 1.0
        # shape.friction = 0.0
        self.space.add(body, shape)
        return body
        # return Box(self.space)

    def spawn_boundaries(self):
        left = self.create_rectangle_static(100, 0, 200, 1000)
        right = self.create_rectangle_static(400, 0, 200, 1000)
        up = self.create_rectangle_static(250, 400, 1000, 200)
        down = self.create_rectangle_static(250, 100, 1000, 200)
        return [left, right, up, down]

    def create_rectangle_static(self, pos_x, pos_y, width, height):
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = (pos_x, pos_y)
        shape = pymunk.Poly.create_box(body, (width, height))
        shape.sensor = True
        shape.collision_type = 3
        shape.color = (0, 0, 0, 0)
        self.space.add(body, shape)
        return shape
