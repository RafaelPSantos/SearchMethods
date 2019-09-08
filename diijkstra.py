import numbers
from search_method import SearchMethod
from diijkstra_vertex_map import DiijkstraVertexMap
from vertex import Vertex

class Diijkstra(SearchMethod):
    def __init__(self, entrance, target, vertices):
        super().__init__(entrance, target, vertices)
        self.vertex_maps = []
        for vertex in self.vertices:
            new_map = DiijkstraVertexMap(vertex)
            self.vertex_maps.append(new_map)
            if vertex is self.entrance:
                new_map.estimation = 0
                new_map.prescient = new_map

    def search_path(self):
        map_to_search = self.map_of_vertex(self.entrance)
        while type(map_to_search) is DiijkstraVertexMap:
            self.search_paths_of_map(map_to_search)
            map_to_search = self.next_search()

    def search_paths_of_map(self, vertex_map):
        vertex_map.lock()
        vertex = vertex_map.vertex
        for vertex_connected in vertex.all_ordened_vertex_connected():
            vertex_connected_map = self.map_of_vertex(vertex_connected)
            if not vertex_connected_map.locked:
                new_esmation = vertex_map.estimation + vertex.comon_edge_with(vertex_connected).cost()
                current_estimation = vertex_connected_map.estimation
                if not isinstance(current_estimation, numbers.Real) or new_esmation < current_estimation:
                    vertex_connected_map.estimation = new_esmation
                    vertex_connected_map.prescient = vertex_map
                    vertex_connected_map.locked = False

    def next_search(self):
        first_map = None
        for vertex_map in self.vertex_maps:
            if vertex_map.locked or not type(vertex_map.prescient) is DiijkstraVertexMap:
                continue
            if not type(first_map) is DiijkstraVertexMap:
                first_map = vertex_map
                continue
            cheaper = vertex_map.estimation < first_map.estimation
            same_price = vertex_map.estimation == first_map.estimation
            alphabetical_order_ahead = vertex_map.vertex.name < first_map.vertex.name
            if cheaper or (same_price and alphabetical_order_ahead):
                first_map = vertex_map
        return first_map

    def select_path_to_target(self):
        map_of_target = self.map_of_vertex(self.target)
        if not isinstance(map_of_target.prescient, DiijkstraVertexMap):
            print("NO PATH")
        else:
            self.select_prescient_of(map_of_target)


    def select_prescient_of(self, vertex_map):
        vertex_map.vertex.selected = True
        if not vertex_map.prescient is vertex_map:
            self.select_prescient_of(vertex_map.prescient)

    def map_of_vertex(self, vertex):
        for vertex_map in self.vertex_maps:
            if vertex_map.vertex is vertex:
                return vertex_map

    def print_table(self):
        for vertex_map in self.vertex_maps:
            if vertex_map.locked:
                print("---------------------")
                print("vetice:", vertex_map.vertex.name)
                print("estimativa:", vertex_map.estimation)
                print("precedente:", vertex_map.prescient.vertex.name)
                print("fechado:", vertex_map.locked)



