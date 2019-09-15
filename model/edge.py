import math

class Edge:
    def __init__(self, first_vertex, second_vertex):
        self.first_vertex = first_vertex
        self.first_vertex.add_edge(self)
        self.second_vertex = second_vertex
        self.second_vertex.add_edge(self)

        if self.first_vertex.diagonal_neighbors(self.second_vertex):
            self.cost = math.sqrt(2)
        else:
            self.cost = 1

    def start(self):
        return (self.first_vertex.pos_x, self.first_vertex.pos_y)

    def end(self):
        return (self.second_vertex.pos_x, self.second_vertex.pos_y)

    def other_point_of(self, vertex):
        if self.first_vertex is vertex:
            return self.second_vertex
        else:
            return self.first_vertex

