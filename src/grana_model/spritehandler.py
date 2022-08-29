class SpriteHandler:
    """draws the sprites for all objects with updated position, rotation and
    scale each draw step"""

    def __init__(self):
        self.sprite_scale_factor = 0.03750000000000002
        self.rotation_factor = 0.0000000
        # self.debug_draw = 0
        

    # def toggle_debug_draw(self):
    #     self.debug_draw += 1

    #     if self.debug_draw > 2:
    #         self.debug_draw = 0

    #     print(f"debug_draw: {self.debug_draw}")

    def change_scale_factor(self, value):
        """modifies the sprite scale factor used for sprite drawing"""
        self.sprite_scale_factor += value
        if self.sprite_scale_factor < 0.02:
            self.sprite_scale_factor = 0.02
        if self.sprite_scale_factor > 0.06:
            self.sprite_scale_factor = 0.06
        print(f"scale_factor: {self.sprite_scale_factor}")

    def change_rotation_factor(self, value):
        """modifies the sprite rotation factor used for sprite drawing"""
        self.rotation_factor += value
        print(f"rotation_factor: {self.rotation_factor}")

    def draw(self, object_list, batch):
        # update all the sprite values and then draw them as a batch
        if self.debug_draw == 1:
            for object in object_list:
                object.update_sprite(
                    self.sprite_scale_factor, self.rotation_factor
                )
            batch.draw()
