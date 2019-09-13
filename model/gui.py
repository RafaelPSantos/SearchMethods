from .button import Button
from .label import Label

class Gui():
    def __init__(self, drawable, font, mouse, screen_bounds = [(0, 0), (600, 600)]):
        self.drawable = drawable
        self.font = font
        self.mouse = mouse
        self.buttons = []
        self.labels = []
        self.screen_bounds = screen_bounds

    def add_button(self, text, position, size, on_click, active_clause):
        new_button = Button(text, position, size, on_click, self.drawable, self.font, active_clause)
        self.buttons.append(new_button)
        return(new_button)

    def add_label(self, text, position, font_size = 16, centralized = False, text_color = None):
        new_label = Label(text, position, self.font, font_size, centralized, text_color)
        self.labels.append(new_label)
        return(new_label)

    def update(self, left_mouse_button_down):
        for button in self.buttons:
            pos_x, pos_y = self.mouse.get_pos()
            button.bellow_mouse = button.point_inside_area(pos_x, pos_y)
            if left_mouse_button_down and button.bellow_mouse:
                button.click()

    def draw(self, screen):
        for button in self.buttons:
            button.draw(screen)
        for label in self.labels:
            label.draw(screen)

