import math

class Edge: #aresta
    def __init__(self, first_vertex, second_vertex):
        self.first_vertex = first_vertex
        self.first_vertex.add_edge(self)
        self.second_vertex = second_vertex
        self.second_vertex.add_edge(self)

    def start(self):
        return (self.first_vertex.pos_x, self.first_vertex.pos_y)

    def end(self):
        return (self.second_vertex.pos_x, self.second_vertex.pos_y)

    def cost(self):
        if self.first_vertex.line == self.second_vertex.line or self.first_vertex.column == self.second_vertex.column:
            return 1
        else:
            return math.sqrt(2)

    def other_point_of(self, vertex):
        if self.first_vertex is vertex:
            return self.second_vertex
        else:
            return self.first_vertex

