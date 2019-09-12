from .default_screen import Screen
from .color import Color

class DefineEdgesScreen(Screen):
    def __init__(self, pygame, screen_size, matrix, settings):
        super().__init__(pygame)
        self.matrix = matrix
        posisition = [screen_size[0] / 2, 20]
        self.add_label("Criação de arestas", Screen.TITLE_SIZE, posisition)
        posisition[0] = 10
        self.add_label("Clique sobre os vertices com o botão esquerdo para definir as arestas:", \
            Screen.BODY_SIZE, posisition, False, Color.NORMAL_COLOR)
        self.add_label("Clique sobre os vertices com o botão direito para definir a aresta inicial e final:", \
            Screen.BODY_SIZE, posisition, False, Color.NORMAL_COLOR)
        self.add_label("LEGENDA DE CORES:", 12, posisition, False, Color.NORMAL_COLOR)
        self.add_label("1-Vertice inicial", 12, posisition, False, Color.ENTRACE_COLOR)
        self.add_label("2-Vertice Final", 12, posisition, False, Color.TARGET_COLOR)
        self.add_label("3-Vertice não selecionado", 12, posisition, False, Color.NORMAL_COLOR)
        self.add_label("4-Vertice selecionado", 12, posisition, False, Color.SELECTED_COLOR)
        self.add_label("5-Vertice desabilitado", 12, posisition, False, Color.DISABLED_COLOR)
        self.add_label("6-Vertice conectado", 12, posisition, False, Color.CONNECTED_COLOR)
        self.add_label("7-Vertice caminho", 12, posisition, False, Color.PATH_COLOR)

        def back_to_edit_size():
            settings["current_screen"] = 1
            self.matrix.reset()

        self.add_button("Voltar", back_to_edit_size, [70, screen_size[1] - 50])


    def update(self, event):
        left_button_click = False
        if event.type == self.mouse_button_up:
            left_button_click = event.button == Screen.MOUSE_LEFT_BUTTON
            if left_button_click:
                if self.matrix.any_vertex_bellow_mouse(event.pos[0], event.pos[1]):
                    self.matrix.define_edges(event.pos[0], event.pos[1])
            elif event.button == Screen.MOUSE_RIGHT_BUTTON:
                self.matrix.select_targets(event.pos[0], event.pos[1])
        self.gui.update(left_button_click)

    def draw(self, screen):
        self.matrix.draw_edges(screen)
        self.matrix.draw_vertex(screen)
        self.gui.draw(screen)
