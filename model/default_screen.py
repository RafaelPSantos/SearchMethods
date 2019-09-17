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
        label = self.gui.add_label(text, (pos[0], pos[1]), font_size, centralized, text_color)
        pos[1] += label.size().height

    def add_button(self, text, action, pos, active_clause = None, font_size = 16):
        button_width = 120
        button_height = 40
        pos[1] += button_height / 2
        button =  self.gui.add_button(text, (pos[0], pos[1]), (button_width, button_height), action, active_clause, font_size)
        pos[1] += button.height