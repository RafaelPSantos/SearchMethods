import math

from .default_screen import Screen
from .color import Color
from model.diijkstra import Diijkstra
from model.manhattan_distance import ManhattanDistance

class DefineEdgesScreen(Screen):

    VERTEX_DISTANCE = 60
    VERTEX_NAME_SIZE = 20
    VERTEX_RADIO = 18

    def __init__(self, pygame, screen_size, matrix, settings, matrix_pos = (150, 200)):
        super().__init__(pygame)
        self.matrix = matrix
        self.matrix_pos = matrix_pos
        self.vertices_join = []
        self.search = None
        posisition = [screen_size[0] / 2, 20]
        self.add_label("Criação de arestas", Screen.TITLE_SIZE, posisition)
        posisition[0] = 10
        self.add_label("Clique sobre os vertices com o botão esquerdo para definir as arestas:", \
            Screen.BODY_SIZE, posisition, False, Color.NORMAL_COLOR)
        self.add_label("Clique sobre os vertices com o botão direito para definir os vertices inicial e final:", \
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
            self.search = None

        def can_search_path():
            entrace_marked = self.matrix.find_entrace_vertice() is not None
            target_marked = self.matrix.find_target_vertice() is not None
            return entrace_marked and target_marked

        def can_play():
            return True

        bottom = screen_size[1] - 50
        self.add_button("Voltar", back_to_edit_size, [70, bottom])
        use_diijkistra_button = self.add_button("Usar Diijkstra", self.start_search, [screen_size[0] / 2, bottom])
        use_diijkistra_button.active_if(can_search_path)

    def mouse_event_handler(self, event):
        left_button_click = False
        if event.type == self.mouse_button_up:
            left_button_click = event.button == Screen.MOUSE_LEFT_BUTTON
            vertex = self.vertex_bellow_mouse(event.pos[0], event.pos[1])
            if left_button_click and vertex is not None:
                if len(self.vertices_join) == 0 or self.matrix.are_neighbors(self.vertices_join[0], vertex) or \
                    vertex is self.vertices_join[0]:
                    vertex.selected = not vertex.selected
                    if vertex.selected:
                        self.vertices_join.append(vertex)
                        if len(self.vertices_join) == 2:
                            common_edge = self.vertices_join[0].comon_edge_with(self.vertices_join[1])
                            if common_edge is None:
                                self.matrix.create_edge(self.vertices_join)
                            else:
                                self.matrix.edges.remove(common_edge)
                                self.vertices_join[0].remove_edge(common_edge)
                                self.vertices_join[1].remove_edge(common_edge)
                            self.vertices_join[0].selected = False
                            self.vertices_join[1].selected = False
                            self.vertices_join = []
                    else:
                        self.vertices_join = []
            elif event.button == Screen.MOUSE_RIGHT_BUTTON and vertex is not None:
                self.matrix.select_targets(vertex)
        self.gui.mouse_handler(left_button_click)

    def draw(self, screen):
        self.draw_edges(screen)
        self.draw_vertex(screen)
        self.gui.draw(screen)

    def draw_vertex(self, screen):
        monospace_font = self.gui.font.SysFont("arial", DefineEdgesScreen.VERTEX_NAME_SIZE)

        first_selected = None
        for vertex in self.matrix.flat_vertices():
            if vertex.selected:
                first_selected = vertex
                break
        for vertex in self.matrix.flat_vertices():
            color = Color.NORMAL_COLOR
            if vertex.selected:
                color = Color.SELECTED_COLOR
            elif vertex.is_entrace():
                color = Color.ENTRACE_COLOR
            elif vertex.is_target():
                color = Color.TARGET_COLOR
            elif vertex.is_part_of_path():
                color = Color.PATH_COLOR
            elif not first_selected is None:
                if not self.matrix.are_neighbors(first_selected, vertex):
                    color = Color.DISABLED_COLOR
                elif vertex.is_conected_to(first_selected):
                    color = Color.CONNECTED_COLOR
            # vertex_pos = (vertex.pos_x, vertex.pos_y)
            position = self.vertex_pos(vertex)
            self.gui.drawable.circle(screen, color, position, vertex.radio)

            label = monospace_font.render(vertex.name, 1, Color.NAME_COLOR)
            text_size = label.get_rect()
            text_pos = (position[0] - text_size.width/2, position[1] - text_size.height/2)
            screen.blit(label, text_pos)

    def draw_edges(self, screen):
        for edge in self.matrix.edges:
            color = Color.NORMAL_COLOR
            if edge.first_vertex.selected or edge.second_vertex.selected:
                color = Color.CONNECTED_COLOR
            elif edge.first_vertex.is_part_of_path() and edge.second_vertex.is_part_of_path():
                color = Color.PATH_COLOR
            start = self.vertex_pos(edge.first_vertex)
            end = self.vertex_pos(edge.second_vertex)
            self.gui.drawable.line(screen, color, start, end, 5)

    def vertex_pos(self, vertex):
        pos_x = self.matrix_pos[0] + vertex.line * DefineEdgesScreen.VERTEX_DISTANCE
        pos_y = self.matrix_pos[1] + vertex.column * DefineEdgesScreen.VERTEX_DISTANCE
        return (pos_x, pos_y)

    def vertex_bellow_mouse(self, mouse_pos_x, mouse_pos_y):
        for vertex in self.matrix.flat_vertices():
            position = self.vertex_pos(vertex)
            distance = math.sqrt((mouse_pos_x - position[0]) ** 2 + (mouse_pos_y - position[1]) ** 2)
            if distance <= vertex.radio:
                return vertex
        return None

    def start_search(self, method = 0):
        for vertex in self.matrix.flat_vertices():
            vertex.unmark_as_part_of_path()
        self.search = Diijkstra(self.matrix.find_entrace_vertice(), self.matrix.find_target_vertice(), self.matrix.flat_vertices())
        self.search.search_path()
        self.search.select_path_to_target()
        manhattan = ManhattanDistance(self.matrix.find_entrace_vertice(), self.matrix.find_target_vertice(), self.matrix.flat_vertices())
        self.print_adjacent_matrix(self.search.vertices)
        print(" ")
        self.print_manhatthan_distance(manhattan.calculate())
        print(" ")
        print("DISTÂNCIA TOTAL PERCORRIDA: " + str(self.search.distante_to_target()))
        print(" ")
        self.print_path(self.search.path_to_target())

    def print_adjacent_matrix(self, vertices):
        print("MATRIZ DE ADJACENTES:")
        header = "  "
        max_space = 3
        for vertex in vertices:
            blank_space = max_space - len(vertex.name)
            header += "|" + vertex.name + " " * blank_space
        header += "|"
        print(header)
        for vertex_index, vertex in enumerate(vertices):
            print("-" * len(header))
            line = ""
            blank_space = max_space - len(vertex.name) - 1
            line += vertex.name + " " * blank_space
            for other_vertex_index, other_vertex in enumerate(vertices):
                line += "|"
                if vertex_index <= other_vertex_index:
                    if other_vertex is vertex:
                        line += " 0 "
                    else:
                        if vertex.is_conected_to(other_vertex):
                            cost = vertex.comon_edge_with(other_vertex).cost
                            if isinstance(cost, int):
                                line += " " + str(cost) + " "
                            else:
                                line += "%.1f" % cost
                        else:
                            line += " 0 "
                else:
                    line += "   "
            line += "|"
            print(line)

    def print_manhatthan_distance(self, distance):
        print("DISTÂNCIA MANHATTHAN: " + str(distance))

    def print_path(self, vertices):
        print("CAMINHO DO COMEÇO AO FIM:")
        line = ""
        for vertex in vertices:
            line += " -> " + vertex.name
        print(line)
