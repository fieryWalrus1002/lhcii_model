import csv
from datetime import datetime
import pyglet
from pyglet.gl import glTranslatef, glScalef
from pyglet.window import key
from math import sqrt
from math import pi
import pymunk
import pymunk.pyglet_util


class SimulationWindow(pyglet.window.Window):
    def __init__(
        self,
        window_offset,
        timer,
        draw_shapes,
        env,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.env = env
        self.draw_shapes = draw_shapes
        self.timer = timer
        self.sensor = None
        self.batch = pyglet.graphics.Batch()

        self.fps_display = pyglet.window.FPSDisplay(window=self)

        self.set_location(window_offset[0], window_offset[1])

        self.window_width, self.window_height = self.get_size()
        # self.options = DrawOptions(batch = my_batch)
        self.grana_radius = 200.0
        self.grana_origin = (200.0, 200.0)

        # openGL translation variables
        self.scale_factor = (1.0, 1.0, 0.0)
        self.delta_pos = (0.0, 0.0, 0.0)

        self.collision_list = []  # holds body objects that are currently colliding
        self.sum_overlap_dist = 0.0

        self.selected_objects = []  # holds the current selected objects
        self.selection_area = 1.0  # hodls the current selection area in square nm

        self.configure_draw_options()

        self.cursor_xy = (
            100.0,
            100.0,
        )  # holds the current selected coordinates for our object sublist.
        self.sel_radius = (
            0.0  # holds the current radius selected for exporting a subset of objects
        )

        # zoom in to the ensemble area
        self.zoom_to_center()

    def configure_draw_options(self):
        self.draw_options = pymunk.pyglet_util.DrawOptions()
        self.draw_options.collision_point_color = (10, 20, 30, 0)
        self.draw_options.constraint_color = (0, 0, 0, 0)
        self.draw_options.flags = self.draw_options.DRAW_SHAPES

    def get_nm_coordinates(self, pyg_pos: tuple[float, float]):

        # pyg_pos is the pyglet coordinates in the window
        # x / get_window_size = a normalized number which you then multiply by the original window_height
        x1, y1 = pyg_pos
        cur_window_width, cur_window_height = self.get_size()

        x0 = (x1 / cur_window_width * self.window_width) - self.delta_pos[
            0
        ]  # gives coordinates in original window size, so it is nm
        y0 = (y1 / cur_window_height * self.window_height) - self.delta_pos[1]

        return (x0, y0)
  #self.export_coordinates(ob_list=self.env.obstacle_list)
    def export_coordinates(self, ob_list):
        now = datetime.now()
        dt_string = now.strftime("%d%m%Y_%H%M")
        filename = str(f"{dt_string}_object_data.csv")
        print(filename + " has been exported.")

        with open(filename, "w", newline="") as f:
            write = csv.writer(f)
            # write the headers
            write.writerow(["type", "x", "y", "angle", "area"])

            for obstacle in ob_list:
                write.writerow(
                    (
                        obstacle.type,
                        obstacle.body.position[0],
                        obstacle.body.position[1],
                        obstacle.body.angle,
                        obstacle.area,
                    )
                )

    def shape_exchange(self):
        """exchange all simple shapes for complex shapes"""
        for o in self.env.obstacle_list:
            o.exchange_simple_for_complex()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.A:
            self.env.get_ensemble_area()
        if symbol == key.B:
            # activate shape exchange
            self.shape_exchange()
        if symbol == key.C:
            # center the grana in the screen and scale it up a bit
            self.set_size(self.window_width * 2, self.window_height * 2)
            glTranslatef(0.5 * self.window_width, 0.5 * self.window_height, 0)
            glScalef(3, 3, 0)
        if symbol == key.D:
            # turn on or off the diffusion. currently not function.
            self.diffusion_handler.toggle_diffusion_state()
        if symbol == key.E:
            # export the coordinates for all objects in the obstacle list
            self.export_coordinates(ob_list=self.env.obstacle_list)
        if symbol == key.I:
            self.window_move(axis=1, dist=-20)
            # glTranslatef(0, -20, 0)
        if symbol == key.K:
            self.window_move(axis=1, dist=20)
            # glTranslatef(0, 20, 0)
        if symbol == key.L:
            self.window_move(axis=0, dist=-20)
            # glTranslatef(-20, 0, 0)
        if symbol == key.J:
            self.window_move(axis=0, dist=20)
            # glTranslatef(20, 0, 0)
        if symbol == key.Q:
            # export coordinates for only selected shapes
            self.export_subset()
        if symbol == key.S:
            self.sprite_handler.toggle_debug_draw()
            pass
        if symbol == key.V:
            self.env.attractionhandler.toggle_attraction_forces()
        if symbol == key.W:
            self.query_shapes_in_section()
        if symbol == key.X:
            # zoom out
            glScalef(0.89, 0.89, 0)
        if symbol == key.Z:
            # zoom in
            glScalef(1.1, 1.1, 0)
        if symbol == key.MINUS:
            self.sprite_handler.change_scale_factor(value=-0.0005)
        if symbol == key.EQUAL:
            self.sprite_handler.change_scale_factor(value=0.0005)
        if symbol == key.BRACKETLEFT:
            self.sprite_handler.change_rotation_factor(value=-0.1)
        if symbol == key.BRACKETRIGHT:
            self.sprite_handler.change_rotation_factor(value=0.1)

    # def query_shapes_in_section(self):

    #     num_objects, objects_list = self.get_shapes_in_rectangle(
    #         self.env.densityhandler.x,
    #         self.env.densityhandler.y,
    #         self.env.densityhandler.width,
    #         self.env.densityhandler.height,
    #     )

        # self.densityhandler.print_shapes_in_section(objects_list)

    def window_move(self, axis: int, dist: int):
        if axis == 0:
            # move on x axis
            glTranslatef(dist, 0, 0)
            x, y, z = self.delta_pos
            self.delta_pos = (x + dist, y, z)
        else:
            # move on y axis
            glTranslatef(0, dist, 0)
            x, y, z = self.delta_pos
            self.delta_pos = (x, y + dist, z)
        print(self.delta_pos)

    def window_scale(self, factor: float):
        self.scale_factor = (
            self.scale_factor[0] + factor,
            self.scale_factor[1] + factor,
            0.0,
        )
        glScalef(factor, factor, 0.0)

    def export_subset(self):
        obj_subset = self.find_objects_in_zone(
            origin=self.cursor_xy, radius=self.sel_radius
        )

        print(
            f"There are {len(obj_subset)} within {self.sel_radius} nm of the point {self.cursor_xy}."
        )

        if len(obj_subset) > 0:
            self.export_coordinates(obj_subset)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            self.cursor_xy = self.get_nm_coordinates((x, y))

    def on_mouse_release(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            x1, y1 = self.cursor_xy
            x2, y2 = self.get_nm_coordinates((x, y))
            self.sel_radius = sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

            # calculate selection area
            self.selection_area = pi * self.sel_radius**2
            print(f"unadjusted coords: {x}, {y}")
            print(
                f"coordinates {self.cursor_xy} selected as origin, radius = {self.sel_radius}, area = {self.selection_area}"
            )

            self.selected_objects = self.find_objects_in_zone(
                origin=self.cursor_xy, radius=self.sel_radius
            )
            print(f"we selected {len(self.selected_objects)} objects.")

    def find_objects_in_zone(self, origin, radius):
        x, y = origin
        sel_obj = []
        for obstacle in self.env.obstacle_list:
            x1, y1 = obstacle.body.position

            # calculate distance from given point
            euc_dist = sqrt((x1 - x) ** 2 + (y1 - y) ** 2)

            # if the distance is less than the radius
            # add it to the selected obj list
            if euc_dist <= radius:
                sel_obj.append(obstacle)

        return sel_obj

    def get_arb_shapes(self, arb):
        return arb.shapes

    def zoom_to_center(self):
        self.set_size(self.window_width * 2, self.window_height * 2)

        glScalef(5, 5, 0)

        glTranslatef(self.window_width * -0.3, self.window_height * -0.3, 0)

    def get_shapes_in_rectangle(self, x, y, width, height):
        num_objects = 0
        objects_list = []

        for o in self.env.obstacle_list:
            x1, y1 = o.body.position

            if x < x1 < x + width and y < y1 < y + height:
                num_objects += 1
                objects_list.append(o)

        return num_objects, objects_list

    # def set_shape_color(self, obstacle):

    #     xmin = self.densityhandler.x
    #     xmax = self.densityhandler.x + self.densityhandler.width
    #     ymin = self.densityhandler.y
    #     ymax = self.densityhandler.y + self.densityhandler.height

    #     # get body position
    #     x, y = obstacle.body.position
    #     # print(f"{i} body.position = {x}, {y}")

    #     for j, s in enumerate(obstacle.shape_list):

    #         # reindex shape
    #         self.env.space.reindex_shape(s)

    #         # get transform for shape attached to body
    #         x1, y1 = s.center_of_gravity

    #         # calculate shape position
    #         x2 = x + x1
    #         y2 = y + y1

    #         if x2 < xmin:
    #             s.color = out_color
    #         elif x2 > xmax:
    #             s.color = out_color
    #         elif y2 < ymin:
    #             s.color = out_color
    #         elif y2 > ymax:
    #             s.color = out_color
    #         else:
    #             s.color = in_color

    def update(self, dt):
        # # update simulation one step
        self.env.step()

        

    def on_draw(self):
        self.clear()

        self.fps_display.draw()

        if self.draw_shapes:
            self.env.space.debug_draw(self.draw_options)

            # list comprehension to draw all the attraction points
            yay_dots = [
                pyglet.shapes.Circle(
                    dot[0], dot[1], radius=0.25, color=(250, 250, 230), batch=self.batch
                )
                for dot in self.env.attraction_point_coords
            ]

            self.batch.draw()
        
        # calculate the ensemble area
        area_dict = self.env.get_ensemble_area()
        print(
            f'ensemble density = {round(area_dict["internal_area"] / (area_dict["ensemble_area"]), 2)}, interior_shape_area: {area_dict["internal_area"]}, total_shape_area: {area_dict["total_area"]}, ensemble_area: {area_dict["ensemble_area"]}'
        )
