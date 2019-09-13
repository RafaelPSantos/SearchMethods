from .default_screen import Screen

class GameScreen(Screen):
    def __init__(self, pygame, screen_size, matrix, settings):
        super().__init__(pygame)

    def update(self, event):
        left_mouse_clicked = event.type == self.mouse_button_up and event.button == Screen.MOUSE_LEFT_BUTTON
        self.gui.update(left_mouse_clicked)

    def draw(self, screen):
        self.gui.draw(screen)