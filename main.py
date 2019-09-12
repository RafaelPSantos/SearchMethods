# coding: utf-8

import pygame
import string
import math

from model.diijkstra import Diijkstra
from model.manhattan_distance import ManhattanDistance
from model.instructions_screen import InstructionsScreen
from model.edit_matrix_screen import EditMatrixScreen
from model.define_edges_screen import DefineEdgesScreen
from model.matrix import Matrix
from model.tower_defense import TowerDefense
from model.gui import Gui
from model.color import Color

CAPTION = "Search Methods"

INSTRUCTIONS_SCREEN = 0
RESIZE_SCREEN = 1
SEARCH_SCREEN = 2
GAME_SCREEN = 3

MINIMUN_ARRAY_SIZE = 2
MAX_ARRAY_SIZE = 6

MOUSE_LEFT_BUTTON = 1
MOUSE_RIGHT_BUTTON = 3

BLACK = (0, 0, 0)
GREY = (100, 100, 100)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 100, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

SCREEN_SIZE = (600, 600)

VERTEX_RADIO = 18
VERTEX_NAME_SIZE = VERTEX_RADIO
VERTEX_DISTANCE = 80

vertices = []
matrix = None
edges = []

instructions_screen = None
edit_matrix_screen = None
define_edges_screen = None
settings = {}

def main():
    global instructions_screen
    global edit_matrix_screen
    global define_edges_screen
    global matrix
    global settings
    settings["running"] = True
    settings["current_screen"] = INSTRUCTIONS_SCREEN

    pygame.init()
    pygame.font.init()

    display = pygame.display
    display.set_caption(CAPTION)

    screen = display.set_mode(SCREEN_SIZE, 0, 32)

    matrix = Matrix(MAX_ARRAY_SIZE, MAX_ARRAY_SIZE, pygame)

    instructions_screen = InstructionsScreen(pygame, SCREEN_SIZE, settings)
    edit_matrix_screen = EditMatrixScreen(matrix, pygame, SCREEN_SIZE, settings)
    define_edges_screen = DefineEdgesScreen(pygame, SCREEN_SIZE, matrix, settings)

    while settings["running"]:
        handle_events(pygame)
        screen.fill(BLACK)
        handle_screens(screen)
        display.flip()

def handle_screens(screen):
    global settings
    global instructions_screen
    if settings["current_screen"] == INSTRUCTIONS_SCREEN:
        instructions_screen.draw(screen)
    elif settings["current_screen"] == RESIZE_SCREEN:
        edit_matrix_screen.draw(screen)
    elif settings["current_screen"] == SEARCH_SCREEN:
        define_edges_screen.draw(screen)

def handle_events(pygame):
    for event in pygame.event.get():
        pressed = pygame.key.get_pressed()
        settings["running"] = not (event.type == pygame.QUIT or pressed[pygame.K_ESCAPE])
        handle_mouse(event)
        handle_keys(pressed)

def handle_mouse(event):
    global settings
    if settings["current_screen"] == INSTRUCTIONS_SCREEN:
        instructions_screen.update(event)
    elif settings["current_screen"] == RESIZE_SCREEN:
        edit_matrix_screen.update(event)
    elif settings["current_screen"] == SEARCH_SCREEN:
        define_edges_screen.update(event)
    elif settings["current_screen"] == GAME_SCREEN:
        pass

def handle_keys(pressed):
    global settings
    if settings["current_screen"] == INSTRUCTIONS_SCREEN:
        pass
    elif settings["current_screen"] == RESIZE_SCREEN:
        pass
    elif settings["current_screen"] == SEARCH_SCREEN:
        if pressed[pygame.K_RETURN]:
            start_search()
        elif pressed[pygame.K_BACKSPACE]:
            matrix.reset()
            settings["current_screen"] = RESIZE_SCREEN
    elif settings["current_screen"] == GAME_SCREEN:
        pass


def start_search(method = 0):
    search = Diijkstra(matrix.find_entrace_vertice(), matrix.find_target_vertice(), matrix.flat_vertices())
    search.search_path()
    search.select_path_to_target()
    manhattan = ManhattanDistance(matrix.find_entrace_vertice(), matrix.find_target_vertice(), matrix.flat_vertices())
    print_adjacent_matrix(search.vertices)
    print(" ")
    print_manhatthan_distance(manhattan.calculate())
    print(" ")
    print("DISTÂNCIA TOTAL PERCORRIDA: " + str(search.distante_to_target()))
    print(" ")
    print_path(search.path_to_target())

def print_adjacent_matrix(vertices):
    print("MATRIZ DE ADJACENTES:")
    header = "  "
    max_space = 3
    for vertex in vertices:
        blank_space = max_space - len(vertex.name)
        header += "|" + vertex.name + " " * blank_space
    header += "|"
    print(header)
    for vertex_index, vertex in enumerate(vertices):
        print("-" * len(header))
        line = ""
        blank_space = max_space - len(vertex.name) - 1
        line += vertex.name + " " * blank_space
        for other_vertex_index, other_vertex in enumerate(vertices):
            line += "|"
            if vertex_index <= other_vertex_index:
                if other_vertex is vertex:
                    line += " 0 "
                else:
                    if vertex.is_conected_to(other_vertex):
                        cost = vertex.comon_edge_with(other_vertex).cost
                        if isinstance(cost, int):
                            line += " " + str(cost) + " "
                        else:
                            line += "%.1f" % cost
                    else:
                        line += " 0 "
            else:
                line += "   "
        line += "|"
        print(line)

def print_manhatthan_distance(distance):
    print("DISTÂNCIA MANHATTHAN: " + str(distance))

def print_path(vertices):
    print("CAMINHO DO COMEÇO AO FIM:")
    line = ""
    for vertex in vertices:
        line += " -> " + vertex.name
    print(line)

def start_game():
    game = TowerDefense()

if __name__=="__main__":
    main()