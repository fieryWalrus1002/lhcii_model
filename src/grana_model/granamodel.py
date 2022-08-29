import pymunk
import pyglet
from collisionhandler import CollisionHandler
from simulationtimer import SimulationTimer
from scoreboard import Scoreboard
from diffusionhandler import DiffusionHandler
from spritehandler import SpriteHandler
from objectdata import ObjectData
from spawner import Spawner

# from grana_model.scale_test import Spawner
from simulationwindow import SimulationWindow

SIM_WIDTH = 500
SIM_HEIGHT = 500

# To control object movememnt, adjust the following:
# self.space.damping : determines the percenatage of velocity that is kept from previous step
# diffusion_factor : scalar for the thermal movement vector
# body.mass : the mass of the body affects how it responds to impulses
# attraction_factor: scalar for the attraction points vectors
#


def main():
    my_space = configure_space(
        threaded=True,
        damping=0.0,
    )
    my_batch = pyglet.graphics.Batch()
    my_spawner = Spawner(
        object_data=ObjectData(pos_csv_filename="082620_SEM_final_coordinates.csv"),
        spawn_type=3,
        # 0: "psii_secondary_noparticles",
        # 1: spawn_type="psii_only",
        # 2: spawn_type="full",
        # 3: LHCII only
        shape_type="simple",
        space=my_space,
        batch=my_batch,
        num_particles=0,
        num_psii=0,
        num_lhcii=1,
        section=(200, 200, 100, 100),
        structure_dict={
            "LHCII": {
                "simulation_limit": 1000,
                "distance_scalar": "well",
                "diffusion_scalar": 1000.0,
                "distance_threshold": 50.0,
                "mass": 1000.0,
                "mass_scalar": 1.0,
                "rotation_scalar": 0.01,
            }
        },
    )

    window = SimulationWindow(
        width=SIM_WIDTH,
        height=SIM_HEIGHT,
        resizable=True,
        window_offset=(int(0.25 * 3440), int(0.05 * 1440)),
        space=my_space,
        spawner=my_spawner,
        timer=SimulationTimer(),
        draw_shapes=True,
    )

    # fps_display = pyglet.window.FPSDisplay(window=window)
    pyglet.clock.schedule_interval(window.update, 1.0 / 60.0)
    pyglet.app.run()
    print("app done")
    window.close()


def configure_space(threaded: bool = False, damping: float = 0.1):
    space = pymunk.Space(threaded=threaded)
    space.damping = damping
    return space


if __name__ == "__main__":

    for i in range(10):

        print(f"iteration {i}")
        main()
