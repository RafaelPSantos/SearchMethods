class Label():
    def __init__(self, text, position, pyfontfont, font_size, centralized, text_color):
        self.text = text
        self.pos_x = position[0]
        self.pos_y = position[1]
        self.font = pyfontfont.SysFont("arial", font_size)
        self.text_color = text_color
        self.label = self.font.render("", 1, text_color)
        self.centralized = centralized
        self.last_text = ""

    def draw(self, screen):
        text = ""
        if isinstance(self.text, str):
            text = self.text
        else:
            text = self.text()
            if text != self.last_text:
                self.label = self.font.render(text, 1, self.text_color)
        position = [self.pos_x , self.pos_y]
        if self.centralized:
            position[0] -= (self.size().width / 2)
            position[1] -= (self.size().height / 2)
        screen.blit(self.label, position)

    def size(self):
        return self.label.get_rect()