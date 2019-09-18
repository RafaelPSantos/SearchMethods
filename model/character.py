class Character:
    def __init__(self, sprite, position, side_size):
        self.sprite = sprite
        self.pos_x = position[0]
        self.pos_y = position[1]
        self.side_size = side_size

    def sprite_position(self):
        return (self.pos_x - self.side_size / 2, self.pos_y - self.side_size / 2)

    def position(self):
        return (self.pos_x, self.pos_y)