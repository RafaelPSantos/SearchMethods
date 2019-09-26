class Element():
    def __init__(self, position, size):
        self.pos_x = position[0]
        self.pos_y = position[1]
        self.width = size[0]
        self.height = size[1]

    def position(self, centralized):
        if centralized:
            return self.center_point()
        else:
            return self.top_left_corner_point()

    def top_left_corner_point(self):
        return (self.pos_x, self.pos_y)

    def center_point(self):
        width, height = self.size()
        return (self.pos_x - width / 2, self.pos_y - height / 2)

    def size(self):
        return (self.width, self.height)

    def rec(self, centralized):
        if centralized:
            pos_x, pos_y = self.top_left_corner_point()
            width, height = self.size()
            pos_x -= width / 2
            pos_y -= height / 2
            return (pos_x, pos_y) + self.size()
        else:
            return self.top_left_corner_point() + self.size()

    def center_of_rec(self, centralized):
        rec_pos_x, rec_pos_y, rec_width, rec_height = self.rec(centralized)
        center_pos_x = rec_pos_x  + rec_width / 2
        center_pos_y = rec_pos_y  + rec_height / 2
        return (center_pos_x, center_pos_y)

    def update(self, dt):
        pass

    def draw(self, dt):
        pass
