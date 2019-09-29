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

    def add_button(self, text, position, size, on_click, font_size, centralized_position = True):
        new_button = Button(text, position, size, font_size, centralized_position)
        new_button.on_click(on_click)
        self.buttons.append(new_button)
        return(new_button)

    def add_label(self, text, position, font_size = 16, text_color = None, centralized = False):
        new_label = Label(text, position, self.font, font_size, text_color, centralized)
        self.labels.append(new_label)
        return(new_label)

    def update(self, dt):
        pass

    def mouse_handler(self, left_mouse_button_down):
        for button in self.buttons:
            if button.is_visible():
                pos_x, pos_y = self.mouse.get_pos()
                button.bellow_mouse = button.point_inside_area(pos_x, pos_y)
                if left_mouse_button_down and button.bellow_mouse:
                    button.click()
                    break

    def draw(self, screen):
        for button in self.buttons:
            if button.is_visible():
                button.draw(screen, self.drawable, self.font)
        for label in self.labels:
            label.draw(screen)

