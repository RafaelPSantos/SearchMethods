import numbers

from .search_method import SearchMethod
from .diijkstra_vertex_map import DiijkstraVertexMap
from .vertex import Vertex

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

    # this method start to search for the shorter path from entrace to target vertex
    def search_path(self):
        map_to_search = self.map_of_vertex(self.entrance)
        while type(map_to_search) is DiijkstraVertexMap:
            self.search_paths_of_map(map_to_search)
            map_to_search = self.next_search()

    # this method search for all other vertex conected to the param vertex_map and estimate their paths
    # if the current path is lower that the new estimation, it will keep the old one,
    # other wise will change for the new current estimation for the new one

    # Esse metodo procura por todos os vertices conectados a dado vertice e estima o seu caminho
    # se o caminho encotrado para esses vertices for menor que o anterior ele troca pelo novo
    # caso contrario, mantem o antigo
    def search_paths_of_map(self, vertex_map):
        vertex_map.lock()
        vertex = vertex_map.vertex
        for vertex_connected in vertex.all_ordened_vertex_connected():
            vertex_connected_map = self.map_of_vertex(vertex_connected)
            if not vertex_connected_map.locked:
                new_esmation = vertex_map.estimation + vertex.comon_edge_with(vertex_connected).cost
                current_estimation = vertex_connected_map.estimation
                if not isinstance(current_estimation, numbers.Real) or new_esmation < current_estimation:
                    vertex_connected_map.estimation = new_esmation
                    vertex_connected_map.prescient = vertex_map
                    vertex_connected_map.locked = False

    # this method look after the next vertex with the lowest estimation and not locked yet
    # return None in case there is not

    # Esse metodo procura um novo vertice, com menor caminho para travar e procurar seus filhos
    def next_search(self):
        first_map = None
        for vertex_map in self.vertex_maps:
            if vertex_map.locked or not isinstance(vertex_map.prescient, DiijkstraVertexMap):
                continue
            if not isinstance(first_map, DiijkstraVertexMap):
                first_map = vertex_map
                continue
            cheaper = vertex_map.estimation < first_map.estimation
            same_price = vertex_map.estimation == first_map.estimation
            alphabetical_order_ahead = vertex_map.vertex.name < first_map.vertex.name
            if cheaper or (same_price and alphabetical_order_ahead):
                first_map = vertex_map
        return first_map

    # this method start to track the path starting from the target to the entrace if a path exists
    def select_path_to_target(self):
        map_of_target = self.map_of_vertex(self.target)
        if not isinstance(map_of_target.prescient, DiijkstraVertexMap):
            print("NO PATH")
        else:
            self.select_prescient_of(map_of_target)

    # this is a recursive method, it marks a vertex as part of the path and try to find the prescient of it
    # in order to repeat the process all over again until the prescient of any vertex is himself
    # usually this happens with the entrace, then it stops the recursion

    # Esse metodo recursivo, marca os vertices que fazem parte do caminho dês do target até a entrace
    def select_prescient_of(self, vertex_map):
        vertex_map.vertex.mark_as_part_of_path()
        if vertex_map.prescient is not vertex_map:
            self.select_prescient_of(vertex_map.prescient)

    def map_of_vertex(self, vertex):
        for vertex_map in self.vertex_maps:
            if vertex_map.vertex is vertex:
                return vertex_map

    def distante_to_target(self):
        return self.map_of_vertex(self.target).estimation

    def path_to_target(self):
        path_to_target = []
        def add_vertex_to_path(vertex_map):
            if vertex_map.prescient is not vertex_map:
                add_vertex_to_path(vertex_map.prescient)
            path_to_target.append(vertex_map.vertex)
        target_map = self.map_of_vertex(self.target)
        if target_map.prescient is not None:
            add_vertex_to_path(target_map)
        return path_to_target

    def path_to_target_exist(self):
        return len(self.path_to_target()) > 0



