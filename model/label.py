from .element import Element

class Label(Element):
    def __init__(self, text, position, pyfontfont, font_size, text_color, centralized_position = False):
        self.font = pyfontfont.SysFont("arial", font_size)
        self.label = self.font.render("", 1, text_color)
        super().__init__(position, self.label.get_rect())
        self.text = text
        self.text_color = text_color
        self.last_text = "a"
        self.centralized = centralized_position

    def draw(self, screen):
        text = ""
        if isinstance(self.text, str):
            text = self.text
        else:
            text = self.text()
        if text != self.last_text:
            self.label = self.font.render(text, 1, self.text_color)
        position = self.top_left_corner_point()
        if self.centralized:
            position = self.center_point()
        screen.blit(self.label, position)

    def size(self):
        size = self.label.get_rect()
        return (size.width, size.height)