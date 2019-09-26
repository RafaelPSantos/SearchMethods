from .color import Color
from .matrix import Matrix
from .diijkstra import Diijkstra
from .vertex import Vertex
from .floor import Floor
from .tower import Tower
from .enemy import Enemy

class TowerDefense():

    MAP_WIDTH = 12
    MAP_HEIGHT = 10
    TOWER_SELLING_PERCENT = 0.5
    TOWER_UPGRADE_PERCENT = 0.8

    def __init__(self, enemy_spawn_vertex, matrix, side_size, map_position):
        self.map_position = map_position
        self.side_size = side_size
        self.enemy_spawn_position = self.vertex_position_according_map(enemy_spawn_vertex)
        self.matrix = matrix
        self.floors = []
        for vertex in self.matrix.flat_vertices():
            self.floors.append(Floor(14, vertex, self.side_size, self.vertex_position_according_map(vertex)))
        self.enemies = []
        self.selected_floor = None
        self.towers = []
        self.current_level = 0
        self.player_money = 200
        self.player_lifes = 10
        self.attack_time = 10000
        self.attack_strength = 0
        self.current_attack_strength = self.attack_strength
        self.spawn_time = 2000
        self.current_spawn_time = 0
        self.min_spawn_time = 100
        self.pause_time = 30000
        self.current_time = 0
        self.attack = True
        self.search = None
        self.define_road()

        self.tower_attributes = {}
        self.tower_attributes["light_tower"] = [12, 0.1, 150, 80, None, Color.YELLOW, 80]
        self.tower_attributes["ice_tower"] = [12, 1, 50, 500, None, Color.LIGHT_BLUE, 100]
        self.tower_attributes["fire_tower"] = [12, 3, 100, 850, None, Color.RED, 150]
        self.max_level_up = 3

    def update(self, dt):
        if self.current_time > 0:
            self.current_time -= dt
            if self.current_time < 0:
                self.current_time = 0

        if self.attack:
            if self.current_time <= 0 and not self.any_enemy_alive():
                self.attack = False
                self.current_time = self.pause_time
                self.current_spawn_time = 0
                self.spawn_time -= 200
                if self.spawn_time < self.min_spawn_time:
                    self.spawn_time = self.min_spawn_time
            elif self.current_time > 0:
                if self.current_spawn_time <= 0:
                    self.spawn_enemy()
                    self.current_spawn_time = self.spawn_time
                else:
                    self.current_spawn_time -= dt
        else:
            if self.current_time <= 0:
                self.attack_strength += 0.5
                self.current_attack_strength = self.attack_strength + len(self.towers) / 5
                self.attack = True
                self.current_time = self.attack_time
                self.current_level += 1
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
        floors_to_target = []
        for vertex in path_to_target:
            floor = self.floor_of_vertex(vertex)
            if floor is not None:
                floors_to_target.append(floor)
        extra_speed = self.current_level / 200
        extra_hp = int(self.current_level / 10)
        sheet_size = 50
        if self.current_attack_strength - 2  > 0:
            self.current_attack_strength -= 1
            new_enemy = Enemy(5, self.enemy_spawn_position, self.side_size, floors_to_target, 10 + extra_hp, 150, 0.05 + extra_speed)
        elif self.current_attack_strength - 1  > 0:
            self.current_attack_strength -= 0.5
            new_enemy = Enemy(3, self.enemy_spawn_position, self.side_size, floors_to_target, 5 + extra_hp, 50, 0.15 + extra_speed)
        else:
            new_enemy = Enemy(1, self.enemy_spawn_position, self.side_size, floors_to_target, 3 + extra_hp, 15, 0.1 + extra_speed)
        self.enemies.append(new_enemy)

    def sell_tower(self):
        tower = self.selected_floor.tower
        self.player_money += tower.current_price * TowerDefense.TOWER_SELLING_PERCENT
        self.towers.remove(tower)
        self.matrix.connect_vertex_to_all_neighbors(self.selected_floor.vertex)
        self.define_road()
        self.selected_floor.tower = None

    def buy_tower_to_selected_floor(self, tower_name):
        atr = self.tower_attributes[tower_name]
        if self.selected_floor.tower is None:
            vertex = self.selected_floor.vertex
            self.matrix.desconnect_vertex_from_everyone(vertex)
            self.define_road()
            if self.search.path_to_target_exist():
                floor = self.selected_floor
                position = (floor.pos_x, floor.pos_y)
                new_tower = Tower(atr[0], atr[1], atr[2], atr[3], atr[4], position, self.side_size, atr[6], atr[5])
                if self.player_money - new_tower.price >= 0:
                    self.player_money -= new_tower.price
                    floor.tower = new_tower
                    self.towers.append(new_tower)
            else:
                self.matrix.connect_vertex_to_all_neighbors(vertex)
                self.define_road()

    def player_able_to_buy_tower(self, tower_slug):
        return self.player_money - self.tower_attributes[tower_slug][6] >= 0

    def upgrade_selected_tower(self):
        tower = self.selected_floor.tower
        upgrade_cost = self.current_tower_upgrade_price()
        tower.upgrade()
        tower.increase_price(upgrade_cost)
        self.player_money -= upgrade_cost

    def current_tower_can_be_upgraded(self):
        return self.selected_floor.tower.current_level < self.max_level_up

    def player_able_to_upgrade_tower(self):
        return self.player_money - self.current_tower_upgrade_price() >= 0

    def current_tower_upgrade_price(self):
        return 100 * TowerDefense.TOWER_UPGRADE_PERCENT

    def define_road(self):
        vertices = self.matrix.flat_vertices()
        for vertex in vertices:
            vertex.unmark_as_part_of_path()
        self.search = Diijkstra(self.matrix.find_entrace_vertice(), self.matrix.find_target_vertice(), vertices)
        self.search.search_path()
        self.search.select_path_to_target()

    def floor_of_vertex(self, vertex):
        for floor in self.floors:
            if floor.vertex is vertex:
                return floor
        return None

    def vertex_position_according_map(self, vertex):
        pos_x = self.map_position[0] + (vertex.line + 1) * self.side_size - self.side_size / 2
        pos_y = self.map_position[1] + (vertex.column  + 1) * self.side_size - self.side_size / 2

        return (int(pos_x), int(pos_y))

    def any_enemy_alive(self):
        return len(self.enemies) > 0

    def defeated(self):
        return self.player_lifes <= 0

    def is_there_a_selected_floor_with_tower(self):
        return self.is_any_floor_selected() and self.does_selected_floor_has_any_tower()

    def is_any_floor_selected(self):
        return self.selected_floor is not None

    def does_selected_floor_has_any_tower(self):
        return self.selected_floor.tower is not None

    def selected_tower(self):
        return self.selected_floor.tower