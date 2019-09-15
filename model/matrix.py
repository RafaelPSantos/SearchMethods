import string
import math

from .vertex import Vertex
from .edge import Edge
from .color import Color

class Matrix():

    VERTEX_DISTANCE = 60
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
        for line in self.vertices:
            for vertex in line:
                flatted_list.append(vertex)
        return flatted_list

    def create_edge(self, vertices):
        self.edges.append(Edge(vertices[0], vertices[1]))

    def select_targets(self, vertex):
        if self.is_entrace_defined():
            entrace = self.find_entrace_vertice()
            if entrace is vertex:
                entrace.unmark_as_entrace()
                return
        else:
            if not vertex.is_target():
                vertex.mark_as_entrace()
                return

        if self.is_target_defined():
            target = self.find_target_vertice()
            if target is vertex:
                target.unmark_as_target()
                return
        else :
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

    def connect_all_vertices(self, only_manhattan = False):
        for vertex in self.flat_vertices():
            self.connect_vertex_to_all_neighbors(vertex)

    def connect_vertex_to_all_neighbors(self, vertex):
        for other_vertex in self.flat_vertices():
            are_not_same = vertex is not other_vertex
            are_neighbors = self.are_neighbors(vertex, other_vertex)
            not_connected = not vertex.is_conected_to(other_vertex)
            if are_not_same and are_neighbors and not_connected:
                self.create_edge([vertex, other_vertex])

    def desconnect_vertex_from_everyone(self, vertex):
        for vertex_connected in vertex.all_ordened_vertex_connected():
            edge = vertex_connected.comon_edge_with(vertex)
            vertex_connected.remove_edge(edge)
            vertex.remove_edge(edge)
            self.edges.remove(edge)
