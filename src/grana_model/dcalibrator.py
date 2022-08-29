import numpy as np


class DCalibrator:
    """ 
    holds the code for calibrating the d values for diffusion and rotation. used
    by the psiistructure module. broken out into its own blass because it was getting
    hard to read psiistructure 
    """

    def __init__(self, structure_dict: dict):
        self.d = structure_dict["d"]
        self.d_rot = structure_dict["d_rot"]
        self.calibrate_diff_d = structure_dict["calibrate_diff_d"]
        self.calibrate_rot_d = structure_dict["calibrate_rot_d"]
        self.diffusion_scalar = structure_dict["diffusion_scalar"]
        self.mass = structure_dict["mass"]
        self.distance_scalar = structure_dict["distance_scalar"]
        self.rotation_scalar = structure_dict["rotation_scalar"]
        self.average_step_over = structure_dict["average_step_over"]

        self.d_ns = self.convert_d_from_cm2_s_to_nm2_ns(self.d)
        self.step_nm = self.calc_step(self.d_ns)

        self.d_rot_ns = self.convert_d_from_rads2_s_to_rads2_ns(self.d_rot)
        self.step_rads = self.calc_step_rads(self.d_rot_ns)

    def calc_step(self, d):
        return np.sqrt(4 * d * 2)

    def calc_step_rads(self, d):
        return np.sqrt(2 * d * 2)

    def convert_d_from_nm2_ns_to_cm2_s(self, d: float):
        return d * 1e-14 / 1e-9

    def convert_d_from_cm2_s_to_nm2_ns(self, d: float):
        return d * 1e-9 / 1e-14

    def convert_d_from_rads2_s_to_rads2_ns(self, d: float):
        """converts time scale from s to ns"""
        return d * 1e-9

    def convert_d_from_rads2_ns_to_rads2_s(self, d: float):
        """converts time scale from s to ns"""
        return d / 1e-9

    def calculate_step_from_history(self, t: int, step, step_history):
        """Take the data from the last t steps, and calculate mean step distance for
        that time period. Compare to the d generated step distance. Return a
        new diffusion scalar to use for the next iteration.
        Also return the step for display
        """
        mean_step = 0
        new_scalar = 1.0

        if len(step_history) > t:

            mean_step = np.mean(step_history[-t:])

            if (step / mean_step) > 1.01:
                new_scalar = 1.001

            if (step / mean_step) < 0.99:
                new_scalar = 0.999

        return new_scalar, mean_step

    def calc_d_from_step(self, step):
        """calculates the d value based on the step nm distance"""
        return (step**2) / (4 * 2)

    def calc_rot_d_from_step(self, step):
        """calculate the d value for rotation based on the rotation mean in radians
        Rotation diffusion coefficient: D = rad^2 / (2*t)
        """
        return (step**2) / (2 * 2)

    def calibrate_d(self, diffusion_scalar, rotation_scalar, step_history, rot_history):
        if self.calibrate_diff_d:
            old_diff_scalar = self.diffusion_scalar
            diff_scalar_mod, step = self.calculate_step_from_history(
                t=self.average_step_over, step=self.step_nm, step_history=step_history
            )
            self.diffusion_scalar = self.diffusion_scalar * diff_scalar_mod
            print(
                f"d: {self.d:.2e}, d': {self.convert_d_from_nm2_ns_to_cm2_s(self.calc_d_from_step(step)):.2e}, df_s: {self.diffusion_scalar}"
            )

        if self.calibrate_rot_d:
            old_rot_scalar = self.rotation_scalar
            rot_scalar_mod, rot_step = self.calculate_step_from_history(
                t=self.average_step_over, step=self.step_rads, step_history=rot_history
            )
            self.rotation_scalar = self.rotation_scalar * rot_scalar_mod
            print(
                f"d_rot: {self.d_rot:.2e}, d_rot': {self.convert_d_from_rads2_ns_to_rads2_s(self.calc_rot_d_from_step(rot_step)):.2e}, rot_s: {self.rotation_scalar}"
            )

        return self.diffusion_scalar, self.rotation_scalar
