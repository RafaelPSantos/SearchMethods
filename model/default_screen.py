from .gui import Gui
from .color import Color

class Screen():
    TITLE_SIZE = 25
    BODY_SIZE = 16
    MOUSE_LEFT_BUTTON = 1
    MOUSE_RIGHT_BUTTON = 3
    def __init__(self, pygame):
        self.gui = Gui(pygame.draw, pygame.font, pygame.mouse)
        self.mouse_button_up = pygame.MOUSEBUTTONUP

    def add_label(self, text, font_size, pos = [0, 0], centralized = True, text_color = Color.NORMAL_COLOR):
        label = self.gui.add_label(text, pos, font_size, centralized, text_color)
        pos[1] += label.size().height
        return label

    def add_button(self, text, action, pos, font_size = 16, size = (120, 40)):
        button =  self.gui.add_button(text, pos, size, action, font_size)
        return button

    def draw(self, screen):
        pass

    def update(self, dt):
        pass

    def event_handler(self, event):
        pass