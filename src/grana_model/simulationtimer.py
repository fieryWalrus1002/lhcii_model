from time import time
from pyglet.text import Label


class SimulationTimer:
    def __init__(self):
        self.time = 0.0  # in nanoseconds, total time elapsed in simulation
        self.time_nanoseconds = 0
        self.time_microseconds = 0
        self.time_milliseconds = 0
        self.time_seconds = 0
        self.ticks = 0  # holds the ticks since simulation began
        self.last_time = round(
            time() * 1000
        )  # holds the last ms elapsed in real time
        self.last_tick_we_checked = 0

    def tick(self, print_ms_per_tick=False):
        # if we're at an increment of 100 for steps since beginning, update our stats
        self.ticks += 1
        if self.ticks % 100 == 0 and print_ms_per_tick:
            print(f"tick: {self.ticks}, ms/tick: {self.elapsed_time / 100} ms")

    def advance_nanoseconds(self, nanoseconds):
        # increment the provided number of nanoseconds, usually 12.5 for one step
        self.time += nanoseconds

        # show nanoseconds but don't let them go above 1000, this is only for display
        self.time_nanoseconds += nanoseconds
        if self.time_nanoseconds >= 1000:
            self.time_nanoseconds -= 1000

        self.time_microseconds = int(self.time // 1000)
        self.time_milliseconds = int(self.time // 1000000)
        self.time_seconds = int(self.time // 1000000000)

    def get_time(self):
        return self.time

    def draw_elapsed_time(self, label_pos):
        # draw a label on the screen with

        # get the current time formatted as an f string
        str_current_time = f"Time elapsed: {self.time_milliseconds}ms, {self.time_microseconds}us, {self.time_nanoseconds}ns"

        # time elapsed timer
        time_label = Label(
            str_current_time,
            font_name="Times New Roman",
            font_size=10,
            x=label_pos[0],
            y=label_pos[1],
        )
        time_label.draw()

    @property
    def elapsed_time(self):
        current_time_ms = round(time() * 1000)  # time in ms
        time_elapsed = current_time_ms - self.last_time  # time elapsed, in ms
        self.last_time = current_time_ms  # set the value for future comparison
        return time_elapsed

    def draw_ms_per_tick(self, label_pos):
        # how many ticks since we last checked?
        if self.ticks == 0:
            ticks = 1
        else:
            ticks = self.ticks - self.last_tick_we_checked

        # update for next time
        self.last_tick_we_checked = self.ticks

        # draw a label on the screen with the ms/tick constantly updating so we can see performance
        str_ms_per_tick = f"{round(self.elapsed_time / ticks)} ms/tick"

        # time elapsed timer
        time_label = Label(
            str_ms_per_tick,
            font_name="Times New Roman",
            font_size=10,
            x=label_pos[0],
            y=label_pos[1],
        )
        time_label.draw()
