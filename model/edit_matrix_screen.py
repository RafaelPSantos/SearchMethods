from .default_screen import Screen
from .color import Color

class EditMatrixScreen(Screen):
    def __init__(self, matrix, pygame, screen_size, settings, table_size = (300, 300)):
        super().__init__(pygame)
        self.matrix = matrix
        self.settings = settings
        self.table_size = table_size
        self.drawable = pygame.draw
        self.screen_size = screen_size
        self.mouse = pygame.mouse
        self.current_matrix_size = 0

        def back_to_main_menu():
            settings["current_screen"] = 0
        posisition = [screen_size[0] / 2, 20]
        self.add_label("Definição do tamanho da matriz", Screen.TITLE_SIZE, posisition)
        posisition[0] = 10
        self.add_label("Arraste o mouse para definir o tamanho desejado da matriz.", Screen.BODY_SIZE, posisition, False)
        self.add_label("Clique com o botão direito do mouse para definir o tamanho.", Screen.BODY_SIZE, posisition, False)
        self.add_label("É permitido apenas matrizes quadradas.", Screen.BODY_SIZE, posisition, False)
        self.add_label("A matrix deve ser no minimo: 2x2 e, no maximo: 6x6.", Screen.BODY_SIZE, posisition, False)
        self.add_button("Voltar", back_to_main_menu, [70, screen_size[1] - 50])

    def mouse_event_handler(self, event):
        left_button_click = False
        if event.type == self.mouse_button_up:
            left_button_click = event.button == Screen.MOUSE_LEFT_BUTTON
            if not left_button_click:
                self.matrix.initialize_vertex(self.current_matrix_size, self.current_matrix_size, True)
                self.settings["current_screen"] += 1
        self.gui.mouse_handler(left_button_click)

    def draw(self, screen):
        self.gui.draw(screen)
        self.draw_matrix(screen)

    def draw_matrix(self, screen):
        margin = self.screen_size[0] - self.table_size[0]
        square_size = self.table_size[0] / 6
        for vertex in self.matrix.flat_vertices():
            line = vertex.line
            column = vertex.column
            pos_x = line * square_size + margin / 2
            pos_y = column * square_size + margin / 2
            rec_border = (pos_x, pos_y, square_size, square_size)
            self.drawable.rect(screen, Color.NORMAL_COLOR, rec_border, 1)
            mouse_pos_x, mouse_pos_y = self.mouse.get_pos()
            min_pos = min(mouse_pos_x, mouse_pos_y)
            if pos_x < min_pos and pos_y < min_pos or line < 2 and column < 2:
                rec_inside = (pos_x + 1, pos_y + 1, square_size - 2, square_size - 2)
                self.drawable.rect(screen, Color.SELECTED_COLOR, rec_inside)
                self.current_matrix_size = vertex.line + 1

