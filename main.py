# coding: utf-8

import pygame

from model.instructions_screen import InstructionsScreen
from model.edit_matrix_screen import EditMatrixScreen
from model.define_edges_screen import DefineEdgesScreen
from model.game_screen import GameScreen
from model.matrix import Matrix
from model.color import Color

CAPTION = "Search Methods"

INSTRUCTIONS_SCREEN = 0
RESIZE_SCREEN = 1
SEARCH_SCREEN = 2
GAME_SCREEN = 3

MINIMUN_ARRAY_SIZE = 2
MAX_ARRAY_SIZE = 6

SCREEN_SIZE = (600, 600)

instructions_screen = None
edit_matrix_screen = None
define_edges_screen = None
game_Screen = None
settings = {}

def main():
    global instructions_screen
    global edit_matrix_screen
    global define_edges_screen
    global game_Screen
    global settings
    settings["running"] = True
    settings["current_screen"] = GAME_SCREEN

    pygame.init()
    pygame.font.init()

    display = pygame.display
    display.set_caption(CAPTION)

    screen = display.set_mode(SCREEN_SIZE, 0, 32)

    matrix = Matrix(MAX_ARRAY_SIZE, MAX_ARRAY_SIZE, pygame)

    instructions_screen = InstructionsScreen(pygame, SCREEN_SIZE, settings)
    edit_matrix_screen = EditMatrixScreen(matrix, pygame, SCREEN_SIZE, settings)
    define_edges_screen = DefineEdgesScreen(pygame, SCREEN_SIZE, matrix, settings)
    game_Screen = GameScreen(pygame, SCREEN_SIZE, settings)

    clock = pygame.time.Clock()

    while settings["running"]:
        handle_events(pygame)
        redirect_screen(screen, display)
        update(clock.tick(60))

def redirect_screen(screen, display):
    screen.fill(Color.BLACK)
    if settings["current_screen"] == INSTRUCTIONS_SCREEN:
        instructions_screen.draw(screen)
    elif settings["current_screen"] == RESIZE_SCREEN:
        edit_matrix_screen.draw(screen)
    elif settings["current_screen"] == SEARCH_SCREEN:
        define_edges_screen.draw(screen)
    elif settings["current_screen"] == GAME_SCREEN:
        game_Screen.draw(screen)
    display.flip()

def handle_events(pygame):
    for event in pygame.event.get():
        pressed = pygame.key.get_pressed()
        settings["running"] = not (event.type == pygame.QUIT or pressed[pygame.K_ESCAPE])
        redirect_event(event)

def redirect_event(event):
    if settings["current_screen"] == INSTRUCTIONS_SCREEN:
        instructions_screen.update(event)
    elif settings["current_screen"] == RESIZE_SCREEN:
        edit_matrix_screen.update(event)
    elif settings["current_screen"] == SEARCH_SCREEN:
        define_edges_screen.update(event)
    elif settings["current_screen"] == GAME_SCREEN:
        game_Screen.update_events(event)
        pass

def update(dt):
    if settings["current_screen"] == INSTRUCTIONS_SCREEN:
        pass
    elif settings["current_screen"] == RESIZE_SCREEN:
        pass
    elif settings["current_screen"] == SEARCH_SCREEN:
        pass
    elif settings["current_screen"] == GAME_SCREEN:
        game_Screen.update(dt)

if __name__=="__main__":
    main()