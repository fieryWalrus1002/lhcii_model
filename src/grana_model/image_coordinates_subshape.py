# import pymunkoptions
# pymunkoptions.options["debug"] = False
from datetime import datetime
import random
import pyglet
from pyglet.window import FPSDisplay, key
import pymunk
from pymunk.pyglet_util import DrawOptions
import csv
from pathlib import Path

NUM_LISTS = 1000
PX_TO_NM_CONVERSION = 25 / 695
NM_TO_PX_CONVERSION = 695 / 25
print(f"25 nm is {NM_TO_PX_CONVERSION * 25} pixels")

diffusion_state = False

collision_types = {
    "pc": 1,
    "obstacle": 2,
    "boundary": 3,
    "bottom": 4,
    "ball": 5,
    "particle": 6,
}


# gamewindow dimensions
window_width = 1070
window_height = 1070


# create the lists that we will populate during the program run
particle_list = []
obstacle_list = []
sprite_list = []

# set global variables
batch = pyglet.graphics.Batch()

# random colors for the subshapes
def random_color():
    return (
        int(random.random() * 255),
        int(random.random() * 255),
        int(random.random() * 255),
    )


# def random_pos_in_circle(max_radius, center):
#     # random angle
#     alpha = 2 * pi * random.random()

#     # random radius
#     # radius = random.random() * max_radius

#     # radius should be biased towards the outside.
#     # the further you get from center, the more points it should have, so things aren't crushed
#     # into the center

#     rand_roll = random.random() + random.random()

#     if rand_roll > 1:
#         r = (2 - rand_roll) * max_radius
#     else:
#         r = rand_roll * max_radius

#     t = 2 * pi * random.random()

#     return [(r*cos(t)) + center[0], center[1] + (r*sin(t))]


# def import_coord(filename):
#     my_list = []
#     obstacle_x = filename["x"].tolist()
#     obstacle_y = filename["y"].tolist()
#     for i in range(0, len(obstacle_x)):
#         my_list.append([obstacle_x[i], obstacle_y[i]])
#     return my_list


# def import_pos_data(filename):
#     imported_csv = pd.read_csv(filename)
#     obstacle_x = imported_csv["x"].tolist()
#     obstacle_y = imported_csv["y"].tolist()
#     pos_coord = []

#     for i in range(0, len(obstacle_x)):
#         pos_coord.append([obstacle_x[i], obstacle_y[i]])

#     output_dict = dict(obstacle_angle=imported_csv["angle"].tolist(),
#                        pos_xy=pos_coord)

#     return output_dict


# # XY coordinates of supercomplexes
# pos_dict = import_pos_data('082620_SEM_final_coordinates.csv')
# # pos_xy = import_coord(pd.read_csv('082620_SEM_final_coordinates.csv'))

# # ratio of psii subspecies
# subspecies_ratio = dict(C2S2M2=0.57,
#                         C2S2M=0.17,
#                         C2S2=0.12,
#                         C2S=0.01,
#                         C2=0.09,
#                         C1=0.03,
#                         CP43=0.00)

# # create a list of subspecies and their probability of appearing
# objects = ["SC1", "SC2", "CP43"]
# probability = [.6, .3, .2]

# result = [(objects[i], probability[i]) for i in range(0, len(objects))]

# # TODO: implement the pop list at some point, right now its an appendix
# pop_list = [result_pop[0] for result_pop in result for i in range(0, int(obstacle_count * result_pop[1]))]

# # import the obstacle coordinate lists as csv files via pandas, and convert them to lists
# c2_dict = dict(sprite_img=pyglet.image.load("res/sc1.png"),
#                shape_coordinates=dict(
#                    shape0=pd.read_csv('res/psii_vertices/C2_mid_piece.csv').values.tolist(),
#                    shape1=pd.read_csv('res/psii_vertices/part1_C2.csv').values.tolist(),
#                    shape2=pd.read_csv('res/psii_vertices/part2_C2.csv').values.tolist(),
#                    shape3=pd.read_csv('res/psii_vertices/part3_C2.csv').values.tolist(),
#                    shape4=pd.read_csv('res/psii_vertices/part4_C2.csv').values.tolist(),
#                    shape5=pd.read_csv('res/psii_vertices/part5_C2.csv').values.tolist(),
#                    shape6=pd.read_csv('res/psii_vertices/part6_C2.csv').values.tolist(),
#                    shape7=pd.read_csv('res/psii_vertices/part7_C2.csv').values.tolist(),
#                    shape8=pd.read_csv('res/psii_vertices/part8_C2.csv').values.tolist(),
#                    shape9=pd.read_csv('res/psii_vertices/part9_C2.csv').values.tolist(),
#                    shape10=pd.read_csv('res/psii_vertices/part10_C2.csv').values.tolist()
#                ),
#                shape_color=(255, 0, 0, 255),  # red for roma
#                sprite_list=sprite_list,
#                obstacle_list=obstacle_list,
#                batch=batch)

# cp26_dict = dict(sprite_img=pyglet.image.load("res/sc1.png"),
#                shape_coordinates=dict(
#                    shape0=pd.read_csv('res/psii_vertices/CP26_part1.csv').values.tolist(),
#                    shape1=pd.read_csv('res/psii_vertices/CP26_part2.csv').values.tolist(),
#                    shape2=pd.read_csv('res/psii_vertices/CP26_part3.csv').values.tolist(),
#                    shape3=pd.read_csv('res/psii_vertices/CP26_part4.csv').values.tolist(),
#                    shape4=pd.read_csv('res/psii_vertices/CP26_part5.csv').values.tolist()),
#                shape_color=(255, 0, 255, 255),  # red for roma
#                sprite_list=sprite_list,
#                obstacle_list=obstacle_list,
#                batch=batch)

# lhc_dict = dict(sprite_img=pyglet.image.load("res/sc1.png"),
#                shape_coordinates=dict(
#                    shape0=pd.read_csv('res/psii_vertices/lhc_trimer.csv').values.tolist()
#                    ),
#                shape_color=(0, 255, 0, 255),
#                sprite_list=sprite_list,
#                obstacle_list=obstacle_list,
#                batch=batch)
# class PointList():
#     def __init__(self, object_type):
#         self.object_type = object_type
#         self.points_list = []

#     @property
#     def points(self, list_num):
#         return self.points_list[list_num]


class SimulationWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_location(300, 50)
        self.fps = FPSDisplay(self)
        self.space = pymunk.Space()
        self.options = DrawOptions()
        self.mouse_xy = (0, 0)
        self.center_xy = (window_width / 2, window_height / 2)
        self.current_subshape = 0
        self.points = []

        # label for mouse coordinates in nm
        self.current_mouse_coords_name_label = pyglet.text.Label(
            text="mouse coords: ",
            font_name="Times New Roman",
            font_size=16,
            x=150,
            y=window_height - 70,
            anchor_x="right",
            anchor_y="center",
            color=(0, 0, 0, 255),
            batch=batch,
        )

        self.current_mouse_coords_label = pyglet.text.Label(
            text="0, 0",
            font_name="Times New Roman",
            font_size=16,
            x=150,
            y=window_height - 70,
            anchor_x="left",
            anchor_y="center",
            color=(0, 0, 0, 255),
            batch=batch,
        )

        # label for a 25nm scale bar
        self.scale_bar = pyglet.shapes.Rectangle(
            192, 30, 695, 20, color=(0, 0, 255), batch=batch
        )

        self.scale_bar_label = pyglet.text.Label(
            str(695 * PX_TO_NM_CONVERSION) + " nm",
            font_name="Times New Roman",
            font_size=16,
            x=window_width / 2,
            y=40,
            anchor_x="center",
            anchor_y="center",
            color=(255, 255, 255, 255),
            batch=batch,
        )

        # label for what subshape we are on right now
        subshape_label = pyglet.text.Label(
            text="subshape: ",
            font_name="Times New Roman",
            font_size=16,
            x=150,
            y=window_height - 90,
            anchor_x="right",
            anchor_y="center",
            color=(0, 0, 0, 255),
            batch=batch,
        )

        self.subshape_variable_label = pyglet.text.Label(
            text="0",
            font_name="Times New Roman",
            font_size=16,
            x=150,
            y=window_height - 90,
            anchor_x="left",
            anchor_y="center",
            color=(0, 0, 0, 255),
            batch=batch,
        )
        # area label
        area_label = pyglet.text.Label(
            text=f"area:",
            font_name="Times New Roman",
            font_size=16,
            x=window_width / 2,
            y=window_height - 90,
            anchor_x="right",
            anchor_y="center",
            color=(0, 0, 0, 255),
            batch=batch,
        )

        self.area_value_label = pyglet.text.Label(
            text=self.calc_shape_area(),
            font_name="Times New Roman",
            font_size=16,
            x=window_width / 2 + 50,
            y=window_height - 90,
            anchor_x="left",
            anchor_y="center",
            color=(0, 0, 0, 255),
            batch=batch,
        )

        # label for instructions
        instructions_label = pyglet.text.Label(
            "wind counter clockwise",
            font_name="Times New Roman",
            font_size=16,
            x=window_width / 2,
            y=1040,
            anchor_x="center",
            anchor_y="center",
            color=(0, 0, 0, 255),
            batch=batch,
        )

        # # center point and coord label
        # self.center_point = pyglet.shapes.Circle(x=self.center_xy[0], y=self.center_xy[1], radius=5, color=(255,0,0))
        # self.center_point_label = pyglet.text.Label(text="0, 0",
        #                                             font_name='Times New Roman',
        #                                             font_size=10,
        #                                             x=self.center_xy[0], y=self.center_xy[1] - 20,
        #                                             anchor_x='center', anchor_y='center',
        #                                             color=(0, 0, 0, 255),
        #                                             batch=batch)

        # shape stuff and images
        def create_list_of_lists(num_lists):
            new_list = [[] for x in range(0, num_lists)]
            return new_list

        # sc_types_list = ['C2S2M2', 'C2S2M', 'C2S2', 'C2S', 'C2', 'C1', 'CP43-freecore', 'LHCII', 'LHCII-monomer']
        self.sc_types = [
            {
                "name": "C2S2M2",
                "points": create_list_of_lists(NUM_LISTS),
                "circles": create_list_of_lists(NUM_LISTS),
                "pygpoints": create_list_of_lists(NUM_LISTS),
            },
            {
                "name": "C2S2M",
                "points": create_list_of_lists(NUM_LISTS),
                "circles": create_list_of_lists(NUM_LISTS),
                "pygpoints": create_list_of_lists(NUM_LISTS),
            },
            {
                "name": "C2S2",
                "points": create_list_of_lists(NUM_LISTS),
                "circles": create_list_of_lists(NUM_LISTS),
                "pygpoints": create_list_of_lists(NUM_LISTS),
            },
            {
                "name": "C2S",
                "points": create_list_of_lists(NUM_LISTS),
                "circles": create_list_of_lists(NUM_LISTS),
                "pygpoints": create_list_of_lists(NUM_LISTS),
            },
            {
                "name": "C2",
                "points": create_list_of_lists(NUM_LISTS),
                "circles": create_list_of_lists(NUM_LISTS),
                "pygpoints": create_list_of_lists(NUM_LISTS),
            },
            {
                "name": "C1",
                "points": create_list_of_lists(NUM_LISTS),
                "circles": create_list_of_lists(NUM_LISTS),
                "pygpoints": create_list_of_lists(NUM_LISTS),
            },
            {
                "name": "CP43-freecore",
                "points": create_list_of_lists(NUM_LISTS),
                "circles": create_list_of_lists(NUM_LISTS),
                "pygpoints": create_list_of_lists(NUM_LISTS),
            },
            {
                "name": "LHCII",
                "points": create_list_of_lists(NUM_LISTS),
                "circles": create_list_of_lists(NUM_LISTS),
                "pygpoints": create_list_of_lists(NUM_LISTS),
            },
            {
                "name": "LHCII-monomer",
                "points": create_list_of_lists(NUM_LISTS),
                "circles": create_list_of_lists(NUM_LISTS),
                "pygpoints": create_list_of_lists(NUM_LISTS),
            },
            {
                "name": "cytb6f",
                "points": create_list_of_lists(NUM_LISTS),
                "circles": create_list_of_lists(NUM_LISTS),
                "pygpoints": create_list_of_lists(NUM_LISTS),
            },
        ]

        # self.sc_types = [{'name':sc_type, 'points':[],'labels':[], 'circles':[]} for sc_type in sc_types_list]

        self.current_type = 0

        # draw the image
        self.sc_type = self.sc_types[self.current_type]
        # C:\data\grana_model\src\grana_model\res\scale_sprites
        self.img = pyglet.image.load(
            str(Path.cwd())
            + "/src/grana_model/res/scale_sprites/"
            + self.sc_type["name"]
            + ".png"
        )
        self.sprite = pyglet.sprite.Sprite(self.img, x=0, y=0)

        self.points = self.sc_type["points"]
        self.circles = self.sc_type["circles"]
        self.pygpoints = self.sc_type["pygpoints"]
        # self.labels = self.sc_type["labels"]
        self.subshape_colors = [random_color() for x in range(0, NUM_LISTS)]

    def change_subshape(self, subshape_change):
        self.current_subshape += subshape_change

        if self.current_subshape > len(self.points) - 1:
            self.current_subshape = 0

        if self.current_subshape == -1:
            self.current_subshape = len(self.points) - 1

    def change_type(self, new_type):
        # save the existing points, circles, and labels
        self.sc_type["points"] = self.points
        self.sc_type["circles"] = self.circles
        self.sc_type["pygpoints"] = self.pygpoints
        # self.sc_type['labels'] = self.labels

        # now swich the current type
        self.current_type += new_type

        if self.current_type > len(self.sc_types) - 1:
            self.current_type = 0

        if self.current_type == -1:
            self.current_type = len(self.sc_types) - 1

        # reset to subshape 0
        self.current_subshape = 0

        # draw the new image
        self.sc_type = self.sc_types[self.current_type]
        self.img = pyglet.image.load(
            str(Path.cwd()) + "/src/grana_model/res/scale_sprites/" + self.sc_type["name"] + ".png"
        )
        self.sprite = pyglet.sprite.Sprite(self.img, x=0, y=0)

        # load the new lists

        self.points = self.sc_type["points"]
        self.circles = self.sc_type["circles"]
        self.pygpoints = self.sc_type["pygpoints"]
        self.labels = self.sc_type["labels"]

    def on_key_press(self, symbol, modifiers):
        if symbol == key.N:
            # previous image in list
            self.change_type(-1)
        if symbol == key.M:
            # next image in list
            self.change_type(1)
        if symbol == key.E:
            # export the list
            self.export_points(self.sc_type)
        if symbol == key.SPACE:
            self.add_coord(x=self.mouse_xy[0], y=self.mouse_xy[1])
        if symbol == key.K:
            self.change_subshape(1)
        if symbol == key.J:
            self.change_subshape(-1)
        # if symbol == key.I:
        #     glTranslatef(0, -20, 0)
        # if symbol == key.L:
        #     glTranslatef(-20, 0, 0)

        # if symbol == key.Z:
        #     glScalef(1.1, 1.1, 0)
        # if symbol == key.X:
        #     glScalef(.89, .89, 0)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            self.add_coord(x, y)

        if button == pyglet.window.mouse.RIGHT:
            self.remove_coord()

    def on_mouse_motion(self, x, y, dx, dy):
        # log real coordinates for placing points
        self.mouse_xy = (x, y)

        # and display the nm coordinates in the upper left
        x1 = str(round(((x - window_height / 2) * PX_TO_NM_CONVERSION), 2))
        y1 = str(round(((y - window_height / 2) * PX_TO_NM_CONVERSION), 2))

        self.current_mouse_coords_label.text = x1 + ", " + y1

    def remove_coord(self):
        # remove last point
        self.circles[self.current_subshape].pop()
        self.points[self.current_subshape].pop()

        # self.labels.pop()

    def add_coord(self, x, y):
        # add a point
        chosen_color = self.subshape_colors[self.current_subshape]
        circle = pyglet.shapes.Circle(x=x, y=y, radius=3, color=chosen_color)
        circle.opacity = 100

        # convert coordinates to nm
        x1 = round(((x - window_height / 2) * PX_TO_NM_CONVERSION), 2)
        y1 = round(((y - window_height / 2) * PX_TO_NM_CONVERSION), 2)

        coord_text = str(str(x1) + ", " + str(y1))
        # print(coord_text)
        self.circles[self.current_subshape].append(circle)
        self.points[self.current_subshape].append((x, y))

    def calc_shape_area(self):
        total_area = 0.0
        if self.points is not None:
            for subshape in self.points:
                scaled_points = self.convert_coords(subshape)
                poly = pymunk.shapes.Poly(None, scaled_points)
                total_area += poly.area

        return str(total_area)

    def convert_coords(self, subshape):
        # convert each set of coordinates into NM values, centered around the mid point of the window as origin
        new_shape = []
        for x, y in subshape:
            x1 = (x - window_height / 2) * PX_TO_NM_CONVERSION
            y1 = (y - window_height / 2) * PX_TO_NM_CONVERSION
            new_shape.append((x1, y1))
        return new_shape

    def export_points(self, sc_type):
        now = datetime.now()
        dt_string = now.strftime("%d%m%Y_%H%M")

        for subshape_num, subshape in enumerate(self.points):
            if len(subshape) > 0:
                filename = str(
                    f"{dt_string}_{str(sc_type['name'])}_subshape_{subshape_num}_points.csv"
                )
                print(filename)
                with open(filename, "w", newline="") as f:
                    write = csv.writer(f)
                    # write the headers
                    write.writerow(["X", "Y"])
                    # convert each set of coordinates into NM values, centered around the mid point of the window as origin
                    for x, y in subshape:
                        x1 = (x - window_height / 2) * PX_TO_NM_CONVERSION
                        y1 = (y - window_height / 2) * PX_TO_NM_CONVERSION
                        write.writerow((x1, y1))

    # def update_center_point(self):
    #     if len(self.points) > 0:
    #         self.center_xy = tuple(map(operator.truediv, reduce(lambda x, y: map(operator.add, x, y), self.points), [len(self.points)] * 2))
    #         self.center_point.x = self.center_xy[0]
    #         self.center_point.y = self.center_xy[1]

    #         # and display the nm coordinates in the upper left
    #         x1 = str(round(((self.center_xy[0] - window_height / 2) * PX_TO_NM_CONVERSION), 2))
    #         y1 = str(round(((self.center_xy[1] - window_height / 2) * PX_TO_NM_CONVERSION), 2))

    #         self.center_point_label.text = x1 + ", " + y1
    #         # self.center_point_label.x = self.center_xy[0]
    #         # self.center_point_label.y = self.center_xy[1] + 8

    def on_draw(self):
        self.clear()
        self.space.debug_draw(self.options)

        # draw thw background image
        self.sprite.draw()

        # update the current subshape text label
        self.subshape_variable_label.text = str(self.current_subshape)

        # draw the labels
        # for label in self.labels:
        #     label.draw()

        # draw the points
        # in the circle bin, we have subshapes, and each subshape has its own circles
        for subshape in self.circles:
            for circle in subshape:
                circle.draw()

        # for shape in self.points:
        #     polygon = Polygon(shape, True, facecolor='blue', alpha=.6)
        for subshape_num, subshape in enumerate(self.points):
            if len(subshape) > 2:
                col = self.subshape_colors[subshape_num]
                gl_col = (col[0], col[1], col[2], 124)
                point_seq = []

                for coord_pair in subshape:
                    point_seq.append(coord_pair[0])
                    point_seq.append(coord_pair[1])

                pyglet.graphics.draw(
                    len(subshape),
                    pyglet.gl.GL_POLYGON,
                    ("v2i", point_seq),
                    ("c4B", gl_col * len(subshape)),
                )

        self.area_value_label.text = self.calc_shape_area()

        # draw the scale bar, label, mouse xy etc
        batch.draw()

        # draw the center point
        # self.update_center_point()
        # self.center_point.draw()

    def update(self, dt):
        # global PQ_diffusion_force
        pass

        # if diffusion_state == True:
        #     for particle in particle_list:

        #         particle.diffusion(force_multiplier=PQ_diffusion_force)

        #     for obstacle in obstacle_list:
        #         # print("test")
        #         obstacle.diffusion(force_multiplier=25)
        #         obstacle.sprite.rotation = degrees(-obstacle.body.angle)
        #         obstacle.sprite.position = (obstacle.body.position.x, obstacle.body.position.y)

        # PQ_diffusion_force = move_cal.update_force(particle_list, PQ_diffusion_force)


if __name__ == "__main__":
    window = SimulationWindow(width=window_width, height=window_height, resizable=True)
    pyglet.clock.schedule_interval(window.update, 1 / 1000.0)
    pyglet.app.run()
