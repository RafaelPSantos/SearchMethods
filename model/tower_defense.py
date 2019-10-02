from .color import Color
from .matrix import Matrix
from .diijkstra import Diijkstra
from .vertex import Vertex
from .floor import Floor
from .tower import Tower
from .enemy import Enemy
from .animation import Animation
from .slow_down_effect import SlowDownEffect
from .burn_effect import BurnEffect
from .cheat import Cheat

class TowerDefense():

    MAP_WIDTH = 12
    MAP_HEIGHT = 10

    def __init__(self, matrix, side_size, map_position):
        self.map_position = map_position
        self.side_size = side_size
        self.enemy_spawn_position = self.vertex_position_according_map(matrix.find_entrace_vertice())
        self.matrix = matrix
        self.floors = []
        for vertex in self.matrix.flat_vertices():
            floor_animation = Animation([12])
            self.floors.append(Floor(floor_animation, vertex, self.side_size, self.vertex_position_according_map(vertex)))
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
        tower_animation = Animation([12])
        one_sec = 1000

        def slow_down(enemy):
            return SlowDownEffect(enemy)

        def burn(enemy):
            return BurnEffect(enemy)

        self.tower_attributes = {
            'light_tower': {
                'animation': tower_animation,
                'damage': 0.1,
                'range': 150,
                'fire_time': 80,
                'effect': None,
                'price': 80,
                'attack_color': Color.YELLOW
            },
            'ice_tower': {
                'animation': tower_animation,
                'damage': 0.5,
                'range': 80,
                'fire_time': 600,
                'effect': slow_down,
                'price': 100,
                'attack_color': Color.LIGHT_BLUE
            },
            'fire_tower': {
                'animation': tower_animation,
                'damage': 1,
                'range': 100,
                'fire_time': 1000,
                'effect': burn,
                'price': 150,
                'attack_color': Color.RED
            },
        }
        
        self.cheats = []

        def give_player_credits():
            self.player_money += 99999

        self.cheats.append(Cheat('money', give_player_credits))

        def give_player_lifes():
            self.player_lifes += 100

        self.cheats.append(Cheat('lifes', give_player_lifes))

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
        for cheat in self.cheats:
            cheat.update(dt);

    def key_input_handler(self, key):
        for cheat in self.cheats:
            cheat.update_code(key)
            if cheat.correct_code_inserted():
                for unused_cheat in self.cheats:
                    unused_cheat.reset()
                return

    def spawn_enemy(self):
        path_to_target = self.search.path_to_target()
        floors_to_target = []
        for vertex in path_to_target:
            floor = self.floor_of_vertex(vertex)
            if floor is not None:
                floors_to_target.append(floor)
        extra_speed = self.current_level / 200
        extra_hp = int(self.current_level / 10)
        sprite_time = 300
        if self.current_attack_strength - 2  > 0:
            self.current_attack_strength -= 1
            animation = Animation([4, 5], sprite_time)
            new_enemy = Enemy(animation, self.enemy_spawn_position, self.side_size, floors_to_target, 10 + extra_hp, 150, 0.05 + extra_speed)
        elif self.current_attack_strength - 1  > 0:
            self.current_attack_strength -= 0.5
            animation = Animation([2, 3], sprite_time)
            new_enemy = Enemy(animation, self.enemy_spawn_position, self.side_size, floors_to_target, 5 + extra_hp, 50, 0.15 + extra_speed)
        else:
            animation = Animation([0, 1], sprite_time)
            new_enemy = Enemy(animation, self.enemy_spawn_position, self.side_size, floors_to_target, 3 + extra_hp, 15, 0.1 + extra_speed)
        self.enemies.append(new_enemy)

    def sell_tower(self):
        tower = self.selected_floor.tower
        self.player_money += tower.selling_price()
        self.towers.remove(tower)
        self.matrix.connect_vertex_to_all_neighbors(self.selected_floor.vertex)
        self.define_road()
        self.selected_floor.tower = None

    def buy_tower_to_selected_floor(self, tower_name):
        if self.selected_floor.tower is None:
            vertex = self.selected_floor.vertex
            self.matrix.desconnect_vertex_from_everyone(vertex)
            self.define_road()
            if self.search.path_to_target_exist():
                floor = self.selected_floor
                position = (floor.pos_x, floor.pos_y)
                new_tower = Tower(position, self.side_size, **self.tower_attributes[tower_name])
                if self.player_money - new_tower.price >= 0:
                    self.player_money -= new_tower.price
                    floor.tower = new_tower
                    self.towers.append(new_tower)
            else:
                self.matrix.connect_vertex_to_all_neighbors(vertex)
                self.define_road()

    def player_able_to_buy_tower(self, tower_slug):
        return self.player_money - self.tower_attributes[tower_slug]['price'] >= 0

    def upgrade_selected_tower(self):
        tower = self.selected_floor.tower
        upgrade_cost = self.current_tower_upgrade_price()
        tower.upgrade()
        tower.increase_price(upgrade_cost)
        self.player_money -= upgrade_cost

    def current_tower_can_be_upgraded(self):
        return self.selected_floor.tower.current_level < Tower.MAX_LEVEL

    def player_able_to_upgrade_tower(self):
        return self.player_money - self.current_tower_upgrade_price() >= 0

    def current_tower_upgrade_price(self):
        return self.selected_floor.tower.upgrade_price()

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