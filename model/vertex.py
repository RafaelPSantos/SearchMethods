from .edge import Edge

class Vertex:
    def __init__(self, name, pos_x, pos_y, line, column, radio):
        self.name = name
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.line = line
        self.column = column
        self.radio = radio
        self.edges = []
        self.selected = False
        self.entrace = False
        self.target = False

    def mark_as_target(self, is_target):
        self.target = is_target

    def mark_as_entrace(self, is_entrace):
        self.entrace = is_entrace

    def add_edge(self, new_edge):
        self.edges.append(new_edge)

    def remove_edge(self, new_edge):
        self.edges.remove(new_edge)

    def is_directly_neighbor_of(self, vertex):
        horizontal_diff = abs(self.line - vertex.line)
        vertical_diff = abs(self.column - vertex.column)
        horizontal_neighbor = horizontal_diff < 2
        vertical_neighbor = vertical_diff < 2
        return horizontal_neighbor and vertical_neighbor

    def comon_edge_with(self, vertex):
        for edge in self.edges:
            if (edge.first_vertex is vertex) or (edge.second_vertex is vertex):
                return edge
        return None

    def is_conected_to(self, vertex):
        return type(self.comon_edge_with(vertex)) is Edge

    def generate_a_name(alphabet, index):
        name = None
        extra_size = int(index / len(alphabet))
        if extra_size > 0:
            name = alphabet[index - len(alphabet)] + str(extra_size)
        else:
            name = alphabet[index]
        return name

    def all_ordened_vertex_connected(self):
        connected_vertices = []
        for edge in self.edges:
            connected_vertices.append(edge.other_point_of(self))

        ordened_connected_vertices = []
        for vertex in connected_vertices:
            if len(ordened_connected_vertices) == 0:
                ordened_connected_vertices.append(vertex)
                continue
            for i, old_vertex in enumerate(ordened_connected_vertices):

                old_cost = self.comon_edge_with(old_vertex).cost()
                new_cost = self.comon_edge_with(vertex).cost()

                cheaper = new_cost < old_cost
                same_price = new_cost == old_cost
                alphabetical_order_ahead = vertex.name < old_vertex.name

                if cheaper or (same_price and alphabetical_order_ahead):
                    ordened_connected_vertices.insert(i, vertex)
                    break
            if not vertex in ordened_connected_vertices:
                ordened_connected_vertices.append(vertex)

        return ordened_connected_vertices