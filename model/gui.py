from .button import Button

class Gui():
    def __init__(self, pygame, screen):
        self.pygame = pygame
        self.screen = screen
        self.buttons = []

    def add_button(self, text, position, size, on_click):
        self.buttons.append(Button(text, position, size, on_click, self.pygame.draw, self.pygame.font))

    def update(self, left_mouse_button_down):
        for button in self.buttons:
            pos_x, pos_y = self.pygame.mouse.get_pos()
            button.bellow_mouse = button.point_inside_area(pos_x, pos_y)
            if left_mouse_button_down and button.bellow_mouse:
                button.click()

    def draw(self):
        for button in self.buttons:
            button.draw(self.screen)

