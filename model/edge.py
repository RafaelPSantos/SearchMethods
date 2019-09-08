import math

class Edge:
    def __init__(self, first_vertex, second_vertex):
        self.first_vertex = first_vertex
        self.first_vertex.add_edge(self)
        self.second_vertex = second_vertex
        self.second_vertex.add_edge(self)

        vertices_on_same_line = self.first_vertex.line == self.second_vertex.line
        vertices_on_same_column = self.first_vertex.column == self.second_vertex.column

        if vertices_on_same_line or vertices_on_same_column:
            self.cost = 1
        else:
            self.cost = math.sqrt(2)

    def start(self):
        return (self.first_vertex.pos_x, self.first_vertex.pos_y)

    def end(self):
        return (self.second_vertex.pos_x, self.second_vertex.pos_y)

    def other_point_of(self, vertex):
        if self.first_vertex is vertex:
            return self.second_vertex
        else:
            return self.first_vertex

