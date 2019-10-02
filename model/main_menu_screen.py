from .default_screen import Screen

class MainMenuScreen(Screen):
    def __init__(self, pygame, screen_size, settings):
        super().__init__(pygame)
        center = screen_size[0] / 2
        pos = [center, 200]

        def start_game():
            settings["current_screen"] = 3

        def go_to_diikjistra():
            settings["current_screen"] = 1

        def quit_game():
            settings["running"] = False

        def disabled_button():
            return False

        self.add_label("SEARCH METHODS TD", Screen.TITLE_SIZE, pos)
        pos[1] += 50
        self.add_button("Jogar", start_game, pos)
        pos[1] += 50
        self.add_button("Testar Diijkstra", go_to_diikjistra, pos)
        pos[1] += 50
        self.add_button("Configurações", 1, pos).active_if(disabled_button)
        pos[1] += 50
        self.add_button("Sair", quit_game, pos)
        pos[1] += 50
        self.add_label("Criado por Caio Santos e Rafael Pereira", 12, [0, screen_size[1] - 14], False)


    def mouse_event_handler(self, event):
        left_mouse_clicked = event.type == self.mouse_button_up and event.button == Screen.MOUSE_LEFT_BUTTON
        self.gui.mouse_handler(left_mouse_clicked)

    def draw(self, screen):
        self.gui.draw(screen)