class Label():
    def __init__(self, text, position, font, font_size, centralized, text_color):
        self.text = text
        self.pos_x = position[0]
        self.pos_y = position[1]
        font = font.SysFont("arial", font_size)
        self.label = font.render(self.text, 1, text_color)
        self.centralized = centralized

    def draw(self, screen):
        position = [self.pos_x , self.pos_y]
        if self.centralized:
            position[0] -= (self.size().width / 2)
            position[1] -= (self.size().height / 2)
        screen.blit(self.label, position)

    def size(self):
        return self.label.get_rect()