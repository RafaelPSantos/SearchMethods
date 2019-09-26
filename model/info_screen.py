from .default_screen import Screen

class InfoScreen(Screen):
    def __init__(self, pygame, screen_size, settings, texts):
        super().__init__(pygame)
        center = screen_size[0] / 2
        pos = [10, 100]

        def back_to_main_menu():
            settings["current_screen"] = 0

        def play():
            settings["current_screen"] = 4


        self.add_label(texts[0], Screen.TITLE_SIZE, pos, False)
        texts.pop(0)
        for text in texts:
            self.add_label(text, Screen.BODY_SIZE, pos, False)

        bottom = screen_size[1] - 50
        self.add_button("Menu", back_to_main_menu, [70, bottom])
        self.add_button("Começar", play, [screen_size[0] - 70, bottom])


    def event_handler(self, event):
        left_mouse_clicked = event.type == self.mouse_button_up and event.button == Screen.MOUSE_LEFT_BUTTON
        self.gui.mouse_handler(left_mouse_clicked)

    def draw(self, screen):
        self.gui.draw(screen)