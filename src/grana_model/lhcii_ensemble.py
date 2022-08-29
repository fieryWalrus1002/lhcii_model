import pymunk

class LHCIIEnsemble:

    def __init__(self, space, attraction_handler, density_handler, spawner, env):
        self.attraction_handler = attraction_handler
        self.density_handler = density_handler
        self.spawner = spawner
        self.env = env
        self.space = space

    def run_sim(self, rep: int = 0, steps: int = 1000, note: str = None):
        """run a simulation environment without gui until a step timout,
        then export coordinates.
        
        steps: number of simulation steps before exit
        rep: rep number, added to end of filename for exported coordinates
        note: note to add to filename 
        """
        filename = self.env.run(steps=steps, rep=rep, note=note)
        return filename
