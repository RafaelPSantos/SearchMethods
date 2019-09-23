from .default_screen import Screen
from .sprite_sheet import SpriteSheet
from .matrix import Matrix
from .define_edges_screen import DefineEdgesScreen
from .color import Color
from .tower_defense import TowerDefense

class GameScreen(Screen):
    def __init__(self, pygame, screen_size, settings):
        super().__init__(pygame)
        self.sheet = SpriteSheet("atlas.png", 4, 4)
        self.map_square_size = int(self.sheet.cellWidth)
        self.vertex_distance = self.map_square_size
        self.map_position = (0, 0)
        self.start_matrix()
        self.game = TowerDefense(self.matrix.find_entrace_vertice(), self.matrix, self.sheet.cellWidth, self.map_position)
        self.settings = settings

        self.reset_game()

        def score():
            return "moedas: " + str(self.game.player_money)

        def lifes():
            return "vidas: " + str(self.game.player_lifes)

        def timer():
            timer = ("% 0.1f" % float(self.game.current_time / 1000))
            if self.game.attack:
                return "Duração do ataque: " + timer + "s"
            else:
                return "Proxima invasão em: " + timer + "s"

        def level():
            return "Invasão nº" + str(self.game.current_level)

        def can_jump_pause():
            return not self.game.attack

        def jump_pause():
            self.game.current_time = 0

        def add_tower(tower_name, tower_slug):
            tower = self.game.tower_attributes[tower_slug]
            return tower_name + " $" +str(tower[6])

        def allowed_to_buy_anything():
            floor = self.game.selected_floor
            return floor is not None and floor.tower is None and not self.game.attack

        def able_to_buy(tower_slug):
            def able():
                return self.game.player_able_to_buy_tower(tower_slug)
            return able;

        def can_upgrade_a_tower():
            floor = self.game.selected_floor
            return floor is not None and floor.tower is not None and self.game.current_tower_can_be_upgraded()

        bottom = screen_size[1] - self.map_square_size / 2
        left_corner = self.map_square_size / 2
        right_corner = screen_size[0]
        button_size = [self.map_square_size, self.map_square_size]

        position = [left_corner, bottom]
        start_button = self.add_button(">>", jump_pause, position, 24, button_size)
        start_button.visible_if(can_jump_pause)

        button_size = (60, 60)
        bottom = screen_size[1] - button_size[0] / 2

        position = [right_corner + button_size[0] / 2, bottom]
        position[0] -= button_size[0]
        sell_button = self.add_button("Vender", self.game.sell_tower, position, 12, button_size)
        sell_button.visible_if(self.game.can_sell_tower)

        position[0] -= button_size[0]

        def add_light_tower():
            self.game.add_tower_to_selected_floor("light_tower")

        def add_fire_tower():
            self.game.add_tower_to_selected_floor("fire_tower")

        def add_ice_tower():
            self.game.add_tower_to_selected_floor("ice_tower")

        upgrade_button = self.add_button("Atualizar", self.game.upgrade_selected_tower, position, 12, button_size)
        upgrade_button.visible_if(can_upgrade_a_tower)
        upgrade_button.active_if(self.game.player_able_to_upgrade_tower)

        position = [right_corner - button_size[0] * 2 - button_size[0] / 2, bottom]

        light_tower_button = self.add_button(add_tower("Raio", "light_tower"), add_light_tower, position, 12, button_size)
        light_tower_button.visible_if(allowed_to_buy_anything)
        light_tower_button.active_if(able_to_buy("light_tower"))
        position[0] -= button_size[0]

        ice_tower_button = self.add_button(add_tower("Fogo", "fire_tower"), add_fire_tower, position, 12, button_size)
        ice_tower_button.visible_if(allowed_to_buy_anything)
        ice_tower_button.active_if(able_to_buy("fire_tower"))
        position[0] -= button_size[0]

        fire_tower_button = self.add_button(add_tower("Gelo", "ice_tower"), add_ice_tower, position, 12, button_size)
        fire_tower_button.visible_if(allowed_to_buy_anything)
        fire_tower_button.active_if(able_to_buy("ice_tower"))

        self.add_label(score, 18, [0, 20], False, Color.YELLOW)
        self.add_label(lifes, 18, [520, 20], False, Color.RED)
        self.add_label(timer, 20, [300, 20], True, Color.WHITE)
        self.add_label(level, 20, [300, 560], True, Color.WHITE)

    def start_matrix(self):
        self.matrix = Matrix(12, 10)
        self.matrix.connect_all_vertices()
        vertices = self.matrix.flat_vertices()
        self.matrix.select_targets(vertices[0])
        self.matrix.select_targets(vertices[len(vertices)-1])

    def reset_game(self):
        self.game = TowerDefense(self.matrix.find_entrace_vertice(), self.matrix, self.sheet.cellWidth, self.map_position)

    def event_handler(self, event):
        left_mouse_clicked = event.type == self.mouse_button_up and event.button == Screen.MOUSE_LEFT_BUTTON
        if left_mouse_clicked:
            for floor in self.game.floors:
                if self.inside_floor_area(floor.area(), event.pos):
                    if self.game.selected_floor == floor:
                        self.game.selected_floor = None
                    else:
                        self.game.selected_floor = floor
                    break
        self.gui.update(left_mouse_clicked)

    def update(self, dt):
        self.game.update(dt)
        if self.game.defeated():
            self.settings["current_screen"] = 0
            self.reset_game()

    def draw(self, screen):
        self.draw_floor(screen)
        self.draw_roads(screen)
        self.draw_towers(screen)
        self.draw_selected_floor(screen)
        self.draw_enemies(screen)
        self.gui.draw(screen)
        for tower in self.game.towers:
            tower.draw(screen)

    def draw_enemies(self, screen):
        life_bar_height = 5
        for enemy in self.game.enemies:
            pos_x, pos_y = enemy.sprite_position()
            self.sheet.draw(screen, enemy.sprite, pos_x, pos_y, False)
            life_bar_max_width = enemy.side_size
            life_bar_width = enemy.current_hp * (life_bar_max_width / enemy.max_hp)
            life_bar_pos_x = pos_x
            life_bar_pos_y = pos_y + enemy.side_size - life_bar_height
            max_rec = (life_bar_pos_x, life_bar_pos_y, life_bar_max_width, life_bar_height)
            current_rec = (life_bar_pos_x, life_bar_pos_y, life_bar_width, life_bar_height)
            self.gui.drawable.rect(screen, Color.RED, max_rec)
            self.gui.drawable.rect(screen, Color.GREEN, current_rec)

    def draw_floor(self, screen):
        for floor in self.game.floors:
            pos_x, pos_y = floor.sprite_position()
            self.sheet.draw(screen, 14, pos_x, pos_y)
        for floor in self.game.floors:
            vertex = floor.vertex
            position = floor.sprite_position()
            self.gui.drawable.rect(screen, Color.BLACK, floor.rec(), 1)

    def draw_selected_floor(self, screen):
        if self.game.selected_floor is not None:
            for floor in self.game.floors:
                vertex = floor.vertex
                position = floor.position()
                if floor == self.game.selected_floor:
                    self.gui.drawable.rect(screen, Color.WHITE, floor.rec(), 1)
                    if floor.tower is not None:
                        self.gui.drawable.circle(screen, Color.GREEN, position, floor.tower.range, 1)
                    break

    def draw_towers(self, screen):
        level_margim = 1
        for tower in self.game.towers:
            level_box_size = 6
            pos_x, pos_y = tower.sprite_position()
            self.sheet.draw(screen, tower.sprite, pos_x, pos_y, False)
            level_box_pos_y = pos_y + tower.side_size - level_box_size
            for level in range(tower.current_level):
                level_box_pos_x = pos_x + (level_box_size * level) + level_margim * level
                rec = (level_box_pos_x, level_box_pos_y, level_box_size, level_box_size)
                self.gui.drawable.rect(screen, tower.attack_color, rec)

    def draw_roads(self, screen):
        for edge in self.matrix.edges:
            color = Color.WHITE
            if edge.first_vertex.is_part_of_path() and edge.second_vertex.is_part_of_path():
                color = Color.ROAD
                start = self.game.floor_of_vertex(edge.first_vertex).position()
                end = self.game.floor_of_vertex(edge.second_vertex).position()
                self.gui.drawable.line(screen, color, start, end, 14)

    def inside_floor_area(self, area, position):
        pos_x, pos_y = position
        left_bound, top_bound, right_bound, bottom_bound = area
        horizontal_inside = left_bound < pos_x and pos_x < right_bound
        vertical_inside = top_bound < pos_y and pos_y < bottom_bound
        return horizontal_inside and vertical_inside