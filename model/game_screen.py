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
        self.vertex_distance = int(self.sheet.cellWidth)
        self.map_position = (0, self.vertex_distance)
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

        def add_or_upgrade():
            if self.game.selected_floor is None :
                return "Selecione um Terreno"
            elif self.game.selected_floor.tower is None:
                return "Torre 100$!"
            else:
                return "Atualizar 100$!"
        bottom = screen_size[1] - 50
        self.add_button("Começar ataque!", jump_pause, [70, bottom], can_jump_pause)
        self.add_button("Vender", self.game.sell_tower, [screen_size[0] - 190, bottom], self.game.can_sell_tower, 12)
        self.add_button(add_or_upgrade, self.game.add_or_upgrade_cannon_to_selected_floor, [screen_size[0] - 70, bottom], self.game.can_add_anything, 12)
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

    def update_events(self, event):
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
        self.draw_enemies(screen)
        self.draw_selected_floor(screen)
        self.gui.draw(screen)
        for tower in self.game.towers:
            tower.draw(screen)

    def draw_enemies(self, screen):
        for enemy in self.game.enemies:
            self.sheet.draw(screen, enemy.sprite, enemy.pos_x, enemy.pos_y)

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
        for tower in self.game.towers:
            pos_x, pos_y = tower.sprite_position()
            self.sheet.draw(screen, tower.sprite, pos_x, pos_y, False)

    def draw_roads(self, screen):
        for edge in self.matrix.edges:
            color = Color.WHITE
            if edge.first_vertex.is_part_of_path() and edge.second_vertex.is_part_of_path():
                color = Color.ROAD
                start = self.game.floor_of_vertex(edge.first_vertex).position()
                end = self.game.floor_of_vertex(edge.second_vertex).position()
                self.gui.drawable.line(screen, color, start, end, 14)

    def draw_enemies(self, screen):
        for enemy in self.game.enemies:
            pos_x, pos_y = enemy.sprite_position()
            self.sheet.draw(screen, enemy.sprite, pos_x, pos_y, False)

    def inside_floor_area(self, area, position):
        pos_x, pos_y = position
        left_bound, top_bound, right_bound, bottom_bound = area
        horizontal_inside = left_bound < pos_x and pos_x < right_bound
        vertical_inside = top_bound < pos_y and pos_y < bottom_bound
        return horizontal_inside and vertical_inside