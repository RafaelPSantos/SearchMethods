from .color import Color
from .matrix import Matrix
from .diijkstra import Diijkstra
from .floor import Floor
from .tower import Tower
from .enemy import Enemy

class TowerDefense():
    def __init__(self, square_size):
        self.enemies = []
        self.floors = []
        self.towers = []
        self.player_money = 200
        self.player_lifes = 10
        self.square_size = square_size

        self.matrix = Matrix(12, 10)
        self.matrix.connect_all_vertices()
        vertices = self.matrix.flat_vertices()
        self.matrix.select_targets(vertices[0])
        self.matrix.select_targets(vertices[len(vertices)-1])

        self.define_road()

        for vertex in self.matrix.flat_vertices():
            self.floors.append(Floor(14, vertex, self.square_size, self.vertex_pos(vertex)))

    def update(self, dt):
        for tower in self.towers:
            tower.update(dt)
            if not tower.has_target():
                for enemy in self.enemies:
                    if tower.on_range_of(enemy):
                        tower.target = enemy
        new_enemy_list = []
        for enemy in self.enemies:
            if enemy.arrived:
                self.player_lifes -= 1
            else:
                if enemy.is_alive():
                    enemy.update(dt)
                    new_enemy_list.append(enemy)
                else:
                    self.player_money += enemy.value
        self.enemies = new_enemy_list

    def spawn_enemy(self):
        path_to_target = self.search.path_to_target()
        start_position = self.vertex_pos(self.matrix.find_entrace_vertice())
        floors_to_target = []
        for vertex in path_to_target:
            floor = self.floor_of_vertex(vertex)
            if floor is not None:
                floors_to_target.append(floor)
        new_enemy = Enemy(1, start_position, self.sheet.cellWidth, floors_to_target)
        self.enemies.append(new_enemy)

    def can_add_anything(self):
        return self.selected_floor is not None

    def can_add_anything(self):
        return self.selected_floor is not None

    def add_cannon_to_selected_floor(self):
        vertex = self.selected_floor.vertex
        self.matrix.desconnect_vertex_from_everyone(vertex)
        self.define_road()
        if self.search.path_to_target_exist():
            floor = self.selected_floor
            position = (floor.pos_x, floor.pos_y)
            new_cannon = Tower(12, position, self.sheet.cellWidth)
            if self.player_money - new_cannon.cost >= 0:
                self.player_money -= new_cannon.cost
                floor.tower = new_cannon
                self.towers.append(new_cannon)
        else:
            self.matrix.connect_vertex_to_all_neighbors(vertex)
            self.define_road()
        self.selected_floor = None

    def define_road(self):
        vertices = self.matrix.flat_vertices()
        for vertex in vertices:
            vertex.unmark_as_part_of_path()
        self.search = Diijkstra(self.matrix.find_entrace_vertice(), self.matrix.find_target_vertice(), vertices)
        self.search.search_path()
        self.search.select_path_to_target()

    def vertex_pos(self, vertex):
        pos_x = self.map_position[0] + (vertex.line + 1) * self.vertex_distance - self.vertex_distance / 2
        pos_y = self.map_position[1] + (vertex.column  + 1) * self.vertex_distance - self.vertex_distance / 2
        return (int(pos_x), int(pos_y))

    def defeated(self):
        return self.player_lifes <= 0