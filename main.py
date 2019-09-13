# coding: utf-8

import pygame

from model.instructions_screen import InstructionsScreen
from model.edit_matrix_screen import EditMatrixScreen
from model.define_edges_screen import DefineEdgesScreen
from model.matrix import Matrix
from model.tower_defense import TowerDefense

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
        pass
    elif settings["current_screen"] == GAME_SCREEN:
        pass

def start_game():
    game = TowerDefense()

if __name__=="__main__":
    main()