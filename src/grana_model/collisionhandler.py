from pyglet.text import Label
from math import pi
from pyglet.shapes import Circle

# notes:

# reindex_shape(shape: pymunk.shapes.Shape) → None[source]
#     Update the collision detection data for a specific shape in the space.
# This is a space function that reindexes a specific shape in the space, and updates
# its collision data. I can use this to check changes udring testing of program


# collision handler
class CollisionHandler:
    def __init__(self, space):
        self.collision_count = 0
        self.total_collision_count = 0
        self.overlap_distance = 0.0
        self.space = space
        self.collision_handler = self.space.add_collision_handler(1, 1)
        self.collision_handler.begin = self.__coll_begin
        self.collision_handler.pre_solve = self.__pre_solve
        self.collision_handler.post_solve = self.__post_solve
        self.collision_handler.separate = self.__separate

    def __pre_solve(self, arbiter, space, data):
        set_ = arbiter.contact_point_set
        overlap_distance = set_.points[0].distance
        self.log_collision(overlap_distance)
        return True

    def __coll_begin(self, arbiter, space, data):
        # set_ = arbiter.contact_point_set
        return True

    def __post_solve(self, arbiter, space, data):
        pass

    def __separate(self, arbiter, space, data):
        # print("coll_separate")
        pass

        # We want to update the collision normal to make the bounce direction
        # dependent of where on the paddle the ball hits. Note that this
        # calculation isn't perfect, but just a quick example.
        # set_ = arbiter.contact_point_set
        # if len(set_.points) > 0:
        #     player_shape = arbiter.shapes[0]
        #     width = (player_shape.b - player_shape.a).x
        #     delta = (player_shape.body.position - set_.points[0].point_a).x
        #     normal = Vec2d(0, 1).rotated(delta / width / 2)
        #     set_.normal = normal
        #     set_.points[0].distance = 0
        # arbiter.contact_point_set = set_
        # print(set_.points[0].distance)

    def log_collision(self, overlap_distance):
        self.collision_count += 1

        if overlap_distance < 0:
            self.overlap_distance += -1 * overlap_distance

    def reset_collision_count(self):
        self.total_collision_count += self.collision_count
        self.collision_count = 0
        self.overlap_distance = 0

    def draw_collision_label(self, label_pos):
        collision_text = f"collision count:{self.collision_count} overlap distance:{round(self.overlap_distance, 2)}"
        collision_label = Label(
            collision_text,
            font_name="Times New Roman",
            font_size=10,
            x=label_pos[0],
            y=label_pos[1],
        )

        collision_label.draw()

    def draw_area_label(self, label_pos):

        # draw the area label showing how much overlap there is
        area_text = f"object area/ grana area:{self.get_total_area()} / {round(pi * 200 **2, 2)} = {round(self.get_total_area() / (pi * 200 **2), 2)}"
        area_label = Label(
            area_text,
            font_name="Times New Roman",
            font_size=10,
            x=label_pos[0],
            y=label_pos[1],
        )
        area_label.draw()

    def draw_density_label(self, label_pos, num_objects, area: float = 1):

        # draw the area label showing how much overlap there is
        area_text = f"object area/ grana area:{self.get_total_area()} / {round(pi * 200 **2, 2)} = {round(self.get_total_area() / (pi * 200 **2), 2)}"
        area_label = Label(
            area_text,
            font_name="Times New Roman",
            font_size=10,
            x=label_pos[0],
            y=label_pos[1],
        )
        area_label.draw()


    def draw_grana_circle(self, x:int = 200, y:int = 200, r:int = 200, opacity:int = 10, color:tuple = (255, 0, 0)):
        # draw a red circle showing the grana area
        circle = Circle(x, y, r, color=color)
        circle.opacity = opacity  # of 255
        circle.draw()

    def get_total_area(self):
        """gets a list of all shapes in space, and gets their area. adds it to
        the a variable and returns it"""
        total_area = 0.0
        for shape in self.space.shapes:
            total_area += shape.area
        return total_area
