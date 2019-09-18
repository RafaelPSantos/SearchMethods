from .character import Character

class Floor(Character):
    def __init__(self, sprite, vertex, side_size, position):
        super().__init__(sprite, position, side_size)
        self.vertex = vertex
        self.tower = None

    def area(self):
        pos_x, pos_y = self.sprite_position()
        return (pos_x, pos_y, pos_x + self.side_size, pos_y + self.side_size)

    def rec(self):
        pos_x, pos_y = self.sprite_position()
        return (pos_x, pos_y, self.side_size, self.side_size)
