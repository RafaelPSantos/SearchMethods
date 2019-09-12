class Button():
    def __init__(self, text, pos, size, action, drawable, font):
        self.drawable = drawable
        self.text = text
        self.pos_x = pos[0]
        self.pos_y = pos[1]
        self.width = size[0]
        self.height = size[1]
        self.action = action
        self.font = font.SysFont("arial", 16)
        self.bellow_mouse = False

    def click(self):
        self.bellow_mouse = False
        self.action()

    def draw(self, screen):
        white = (255, 255, 255)
        black = (0, 0, 0)
        rec = (self.left_margin(), self.top_margin(), self.width, self.height)

        text_color = None
        if self.bellow_mouse:
            text_color = black
            self.drawable.rect(screen, white, rec)
        else:
            text_color = white
            self.drawable.rect(screen, white, rec, 1)

        label = self.font.render(self.text, 1, text_color)
        text_size = label.get_rect()
        text_pos = (self.pos_x - text_size.width / 2, self.pos_y - text_size.height / 2)
        screen.blit(label, text_pos)

    def left_margin(self):
        return self.pos_x - self.width / 2

    def right_margin(self):
        return self.pos_x + self.width / 2

    def top_margin(self):
        return self.pos_y - self.height / 2

    def bottom_margin(self):
        return self.pos_y + self.height / 2

    def point_inside_area(self, pos_x, pos_y):
        inside_width = pos_x > self.left_margin() and pos_x < self.right_margin()
        inside_height = pos_y < self.bottom_margin() and pos_y > self.top_margin()
        return inside_width and inside_height