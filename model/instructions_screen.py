class InstructionsScreen():

    TITLE_SIZE = 20
    BODY_SIZE = 15

    def __init__(self, font, screen, text_color = (255, 255, 255)):
        self.font = font
        self.title = ""
        self.paragraphs = []
        self.text_color = text_color
        self.screen = screen

    def update(self):
        pass

    def draw(self):
        title_font = self.font.SysFont("arial", InstructionsScreen.TITLE_SIZE)
        body_font = self.font.SysFont("arial", InstructionsScreen.BODY_SIZE)

        width, height = self.screen.get_size()

        margim = 20
        current_height = margim

        current_height += self.draw_text(self.title, title_font, margim, current_height)[1] + margim

        for paragraph in self.paragraphs:
            current_height += self.draw_text(paragraph, body_font, margim, current_height)[1] + margim

    def draw_text(self, text, font, pos_x, pos_y):
        max_width = self.screen.get_size()[1]
        label = font.render(text, 1, self.text_color)
        text_pos = (pos_x, pos_y)

        bigger_than_screen = max_width < label.get_rect()[1]

        self.screen.blit(label, text_pos)
        return label.get_rect()


    def key_handler(self, event):
        pass

    def add_text(self, title, paragraphs):
        self.title = title
        self.paragraphs = paragraphs
