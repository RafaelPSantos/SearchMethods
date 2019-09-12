import string
import math

from .vertex import Vertex
from .edge import Edge
from .color import Color

class Matrix():

    VERTEX_DISTANCE = 80
    VERTEX_NAME_SIZE = 20
    VERTEX_RADIO = 18

    def __init__(self, line_count, column_count, pygame):
        self.pygame = pygame
        self.vertices = []
        self.edges = []
        self.line_count = line_count
        self.column_count = column_count

        self.initialize_vertex(line_count, column_count)

    def initialize_vertex(self, line_count, column_count, with_name = False):
        self.vertices = []
        for line in range(line_count):
            new_line = []
            for column in range(column_count):
                name = ""
                if with_name:
                    name = Vertex.generate_a_name(string.ascii_uppercase, line + column * line_count)
                pos_x = (1 + line) * Matrix.VERTEX_DISTANCE
                pos_y = (1 + column) * Matrix.VERTEX_DISTANCE
                new_line.append(Vertex(name, pos_x, pos_y, line, column, Matrix.VERTEX_RADIO))
            self.vertices.append(new_line)

    def draw_vertex(self, screen):
        monospace_font = self.pygame.font.SysFont("arial", Matrix.VERTEX_NAME_SIZE)

        first_selected = None
        for vertex in self.flat_vertices():
            if vertex.selected:
                first_selected = vertex
                break

        for vertex in self.flat_vertices():
            color = Color.NORMAL_COLOR
            if vertex.selected:
                color = Color.SELECTED_COLOR
            elif vertex.is_entrace():
                color = Color.ENTRACE_COLOR
            elif vertex.is_target():
                color = Color.TARGET_COLOR
            elif vertex.is_part_of_path():
                color = Color.PATH_COLOR
            elif type(first_selected) is Vertex:
                if not self.are_neighbors(first_selected, vertex):
                    color = Color.DISABLED_COLOR
                elif vertex.is_conected_to(first_selected):
                    color = Color.CONNECTED_COLOR
            vertex_pos = (vertex.pos_x, vertex.pos_y)
            self.pygame.draw.circle(screen, color, vertex_pos, vertex.radio)

            label = monospace_font.render(vertex.name, 1, Color.NAME_COLOR)
            text_size = label.get_rect()
            text_pos = (vertex.pos_x - text_size.width/2, vertex.pos_y - text_size.height/2)
            screen.blit(label, text_pos)

    def draw_edges(self, screen):
        for edge in self.edges:
            color = Color.NORMAL_COLOR
            if edge.first_vertex.selected or edge.second_vertex.selected:
                color = Color.CONNECTED_COLOR
            elif edge.first_vertex.is_part_of_path() and edge.second_vertex.is_part_of_path():
                color = Color.PATH_COLOR
            self.pygame.draw.line(screen, color, edge.start(), edge.end(), 5)

    def find_target_vertice(self):
        for vertex in self.flat_vertices():
            if vertex.is_target():
                return vertex

    def is_target_defined(self):
        return isinstance(self.find_target_vertice(), Vertex)

    def find_entrace_vertice(self):
        for vertex in self.flat_vertices():
            if vertex.is_entrace():
                return vertex
        return None

    def is_entrace_defined(self):
        return isinstance(self.find_entrace_vertice(), Vertex)

    def any_vertex_bellow_mouse(self, mouse_pos_x, mouse_pos_y):
        return isinstance(self.vertex_bellow_mouse(mouse_pos_x, mouse_pos_y), Vertex)

    def vertex_bellow_mouse(self, mouse_pos_x, mouse_pos_y):
        for vertex in self.flat_vertices():
            distance = math.sqrt((mouse_pos_x - vertex.pos_x) ** 2 + (mouse_pos_y - vertex.pos_y) ** 2)
            if distance <= vertex.radio:
                return vertex

    def flat_vertices(self, with_removed = False):
        flatted_list = []
        for column in range(len(self.vertices)):
            for line in range(len(self.vertices[column])):
                flatted_list.append(self.vertices[line][column])
        return flatted_list

    def define_edges(self, pos_x, pos_y):
        selected_vertices = []
        vertex = self.flat_vertices()[0]
        distance = math.sqrt((pos_x - vertex.pos_x) ** 2 + (pos_y - vertex.pos_y) ** 2)

        for vertex in self.flat_vertices():
            distance = math.sqrt((pos_x - vertex.pos_x) ** 2 + (pos_y - vertex.pos_y) ** 2)
            if distance <= vertex.radio:
                vertex.selected = not vertex.selected
            if vertex.selected:
                selected_vertices.append(vertex)
        if len(selected_vertices) >= 2:
            first_vertex, second_vertex = selected_vertices
            if self.are_neighbors(first_vertex, second_vertex):
                comon_edge = first_vertex.comon_edge_with(second_vertex)
                if type(comon_edge) is Edge:
                    first_vertex.remove_edge(comon_edge)
                    second_vertex.remove_edge(comon_edge)
                    self.edges.remove(comon_edge)
                else:
                    self.edges.append(Edge(first_vertex, second_vertex))
            for vertex in self.flat_vertices():
                vertex.selected = False

    def select_targets(self, pos_x, pos_y):
        if not self.any_vertex_bellow_mouse(pos_x, pos_y):
            return

        if self.is_entrace_defined():
            entrace = self.find_entrace_vertice()
            if entrace is self.vertex_bellow_mouse(pos_x, pos_y):
                entrace.unmark_as_entrace()
                return
        else:
            vertex = self.vertex_bellow_mouse(pos_x, pos_y)
            if not vertex.is_target():
                vertex.mark_as_entrace()
                return

        if self.is_target_defined():
            target = self.find_target_vertice()
            if target is self.vertex_bellow_mouse(pos_x, pos_y):
                target.unmark_as_target()
                return
        else :
            vertex = self.vertex_bellow_mouse(pos_x, pos_y)
            if not vertex.is_entrace():
                vertex.mark_as_target()
                return

    def reset(self):
        self.vertices = []
        self.initialize_vertex(self.line_count, self.column_count)
        self.edges = []

    def are_neighbors(self, vertex01, vertex02):
        horizontal_diff = abs(vertex01.line - vertex02.line)
        vertical_diff = abs(vertex01.column - vertex02.column)
        horizontal_neighbor = horizontal_diff < 2
        vertical_neighbor = vertical_diff < 2
        return horizontal_neighbor and vertical_neighbor