from .default_screen import Screen

class InstructionsScreen(Screen):
    def __init__(self, pygame, screen_size, settings):
        super().__init__(pygame)
        center = screen_size[0] / 2
        pos = [center, 200]

        def start_game():
            settings["current_screen"] += 1

        def quit_game():
            settings["running"] = False

        self.add_label("SEARCH METHODS TD", Screen.TITLE_SIZE, pos)
        self.add_button("Começar", start_game, pos)
        self.add_button("Configurações", 1, pos)
        self.add_button("Sair", quit_game, pos)
        self.add_label("Criado por Caio Santos, Daniel e Rafael Pereira", 12, [0, screen_size[1] - 14], False)


    def update(self, event):
        left_mouse_clicked = event.type == self.mouse_button_up and event.button == Screen.MOUSE_LEFT_BUTTON
        self.gui.update(left_mouse_clicked)

    def draw(self, screen):
        self.gui.draw(screen)