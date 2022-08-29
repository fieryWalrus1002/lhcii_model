from pyglet.text import Label


class Scoreboard:
    def __init__(self):
        self.score = 0
        self.overlap_score = 0
        self.max_collisions = 1000
        self.norm_overlap_score = 1

    def update_score(self, obj_list):
        # if len(obj_list) > self.max_collisions:
        #     self.max_collisions = len(obj_list)
        self.score = 500 - len(obj_list)

    def update_overlap_score(self, score_sum, area):
        self.overlap_score = score_sum
        if area > 0:
            self.norm_overlap_score = score_sum / area * 1000
        else:
            self.norm_overlap_score = 0

    def draw(self, label_pos):
        current_score = f"500 - # of colliding objects: {self.score}"
        current_overlap_score = f"total overlap: {round(self.overlap_score, 2)}"
        norm_overlap = f"norm_overlap: {round(self.norm_overlap_score, 4)}"
        # label for displaying the score
        score_label = Label(
            current_score,
            font_name="Times New Roman",
            font_size=10,
            x=label_pos[0],
            y=label_pos[1],
        )

        score_label.draw()

        overlap_score_label = Label(
            current_overlap_score,
            font_name="Times New Roman",
            font_size=10,
            x=label_pos[0],
            y=label_pos[1] - 15,
        )
        overlap_score_label.draw()

        norm_overlap_label = Label(
            norm_overlap,
            font_name="Times New Roman",
            font_size=10,
            x=label_pos[0],
            y=label_pos[1] - 30,
        )
        norm_overlap_label.draw()
