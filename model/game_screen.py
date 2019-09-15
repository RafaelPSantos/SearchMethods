from .default_screen import Screen
from .sprite_sheet import SpriteSheet
from .matrix import Matrix
from .define_edges_screen import DefineEdgesScreen
from .color import Color
from .diijkstra import Diijkstra
from .floor import Floor
from .tower import Tower
from .enemy import Enemy

class GameScreen(Screen):
    def __init__(self, pygame, screen_size, settings):
        super().__init__(pygame)
        self.sheet = SpriteSheet("atlas.png", 4, 4)
        self.vertex_distance = int(self.sheet.cellWidth)
        self.enemies = []
        self.floors = []
        self.towers = []
        self.search = None
        self.map_position = (0, self.vertex_distance)

        self.matrix = Matrix(12, 10, pygame)
        self.matrix.connect_all_vertices()
        vertices = self.matrix.flat_vertices()
        self.matrix.select_targets(vertices[0])
        self.matrix.select_targets(vertices[len(vertices)-1])

        self.define_road()
        self.selected_floor = None
        for vertex in self.matrix.flat_vertices():
            self.floors.append(Floor(14, vertex, self.sheet.cellWidth, self.vertex_pos(vertex)))

        self.player_money = 200
        self.player_lifes = 10

        def score():
            return "moedas: " + str(self.player_money)

        def lifes():
            return "vidas: " + str(self.player_lifes)

        bottom = screen_size[1] - 50
        self.add_button("Começar", self.spawn_enemy, [70, bottom])
        self.add_button("CANNON!", self.add_cannon_to_selected_floor, [screen_size[0] - 70, bottom], self.can_add_anything)
        self.add_label(score, 12, [0, 0], False, Color.YELLOW)
        self.add_label(lifes, 12, [100, 0], False, Color.RED)

    def update_events(self, event):
        left_mouse_clicked = event.type == self.mouse_button_up and event.button == Screen.MOUSE_LEFT_BUTTON
        if left_mouse_clicked:
            print(event.pos)
            for floor in self.floors:
                if self.inside_floor_area(floor.area(True), event.pos):
                    if self.selected_floor == floor:
                        self.selected_floor = None
                    else:
                        self.selected_floor = floor
                    break
        self.gui.update(left_mouse_clicked)

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

    def draw(self, screen):
        self.draw_floor(screen)
        self.draw_roads(screen)
        self.draw_towers(screen)
        self.draw_enemies(screen)
        self.draw_selected_floor(screen)
        self.gui.draw(screen)
        for tower in self.towers:
            tower.draw(screen)

    def draw_enemies(self, screen):
        for enemy in self.enemies:
            self.sheet.draw(screen, enemy.sprite, enemy.pos_x, enemy.pos_y)

    def draw_floor(self, screen):
        for floor in self.floors:
            pos_x, pos_y = floor.sprite_position()
            self.sheet.draw(screen, 14, pos_x, pos_y)
            screen.set_at((floor.pos_x, floor.pos_y), (255, 0, 0))
        for floor in self.floors:
            vertex = floor.vertex
            position = self.vertex_pos(vertex)
            side_size = self.sheet.cellWidth
            self.gui.drawable.rect(screen, Color.BLACK, floor.rec(True), 1)

    def draw_selected_floor(self, screen):
        if self.selected_floor is not None:
            for floor in self.floors:
                vertex = floor.vertex
                position = self.vertex_pos(vertex)
                if floor == self.selected_floor:
                    self.gui.drawable.rect(screen, Color.WHITE, floor.rec(True), 1)
                    if floor.tower is not None:
                        self.gui.drawable.circle(screen, Color.GREEN, position, floor.tower.range, 1)
                    break

    def draw_towers(self, screen):
        for tower in self.towers:
            pos_x, pos_y = tower.sprite_position()
            self.sheet.draw(screen, tower.sprite, pos_x, pos_y, False)

    def draw_roads(self, screen):
        for edge in self.matrix.edges:
            color = Color.WHITE
            if edge.first_vertex.is_part_of_path() and edge.second_vertex.is_part_of_path():
                color = Color.ROAD
                start = self.vertex_pos(edge.first_vertex)
                end = self.vertex_pos(edge.second_vertex)
                self.gui.drawable.line(screen, color, start, end, 10)

    def draw_enemies(self, screen):
        for enemy in self.enemies:
            pos_x, pos_y = enemy.sprite_position()
            self.sheet.draw(screen, enemy.sprite, pos_x, pos_y, False)

    def vertex_pos(self, vertex):
        pos_x = self.map_position[0] + (vertex.line + 1) * self.vertex_distance - self.vertex_distance / 2
        pos_y = self.map_position[1] + (vertex.column  + 1) * self.vertex_distance - self.vertex_distance / 2
        return (int(pos_x), int(pos_y))

    def define_road(self):
        vertices = self.matrix.flat_vertices()
        for vertex in vertices:
            vertex.unmark_as_part_of_path()
        self.search = Diijkstra(self.matrix.find_entrace_vertice(), self.matrix.find_target_vertice(), vertices)
        self.search.search_path()
        self.search.select_path_to_target()

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

    def inside_floor_area(self, area, position):
        pos_x, pos_y = position
        left_bound, top_bound, right_bound, bottom_bound = area
        horizontal_inside = left_bound < pos_x and pos_x < right_bound
        vertical_inside = top_bound < pos_y and pos_y < bottom_bound
        return horizontal_inside and vertical_inside

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

    def floor_of_vertex(self, vertex):
        for floor in self.floors:
            if floor.vertex is vertex:
                return floor
        return None

    def defeated(self):
        return self.player_lifes <= 0