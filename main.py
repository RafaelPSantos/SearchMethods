# coding: utf-8

import pygame

from model.main_menu_screen import MainMenuScreen
from model.info_screen import InfoScreen
from model.edit_matrix_screen import EditMatrixScreen
from model.define_edges_screen import DefineEdgesScreen
from model.game_screen import GameScreen
from model.matrix import Matrix
from model.color import Color

CAPTION = "Search Methods"

START_SCREEN = 0
RESIZE_SCREEN = 1
SEARCH_SCREEN = 2
DESCRIPTION_SCREEN = 3
GAME_SCREEN = 4

MINIMUN_ARRAY_SIZE = 2
MAX_ARRAY_SIZE = 6

SCREEN_SIZE = (600, 600)

main_menu_screen = None
description_screen = None
edit_matrix_screen = None
define_edges_screen = None
game_Screen = None

settings = {}

def main():
    global main_menu_screen
    global description_screen
    global edit_matrix_screen
    global define_edges_screen
    global game_Screen
    global settings
    settings["running"] = True
    settings["current_screen"] = START_SCREEN

    pygame.init()
    pygame.font.init()

    display = pygame.display
    display.set_caption(CAPTION)

    screen = display.set_mode(SCREEN_SIZE, 0, 32)

    matrix = Matrix(MAX_ARRAY_SIZE, MAX_ARRAY_SIZE)

    main_menu_screen = MainMenuScreen(pygame, SCREEN_SIZE, settings)
    game_history = []
    game_history.append("HISTORIA")
    game_history.append("      Um poderoso exército inimigo esta se aproximando pelo norte.")
    game_history.append("      Seu rei, ordenou que nossa cidade fosse invadida imediatamente")
    game_history.append("ele disse a suas tropas para seguirem sem parar custe o que custar.")
    game_history.append("para isso, ele juntou todos os matemáticos do reino")
    game_history.append("e ordenou que calculassem a menor rota até nós,")
    game_history.append("e que seu exército, marche sem parar até a cidade por essa rota")
    game_history.append("sem parar significa que ele deu ordens apenas correrem")
    game_history.append("de fato, esse não é o melhor rei de todos, mas essa será nossa salvação...")
    game_history.append("você deve aprender como os matematicos do rei, descobriram a menor rota possivel")
    game_history.append("depois deverá preparar torres defensivas ao longo dessa rota,")
    game_history.append("e destruir o exécito antes que chegue até nós")
    game_history.append("     A forma que os matematicos descobriram a menor rota se chama: 'Diijkstra'")
    game_history.append("você deve testar essa forma e então preparar nossas defesas")
    game_history.append("AVISO: você não poderá construir torres enquanto o inimigo ataca,")
    game_history.append("apenas durante os intervalos entre ataques!")

    description_screen = InfoScreen(pygame, SCREEN_SIZE, settings, game_history)
    edit_matrix_screen = EditMatrixScreen(matrix, pygame, SCREEN_SIZE, settings)
    define_edges_screen = DefineEdgesScreen(pygame, SCREEN_SIZE, matrix, settings)
    game_Screen = GameScreen(pygame, SCREEN_SIZE, settings)

    clock = pygame.time.Clock()

    while settings["running"]:
        current = current_screen()

        for event in pygame.event.get():
            pressed = pygame.key.get_pressed()
            settings["running"] = not (event.type == pygame.QUIT or pressed[pygame.K_ESCAPE])
            current.event_handler(event)

        screen.fill(Color.BLACK)
        current.draw(screen)
        display.flip()

        current.update(clock.tick(60))

def current_screen():
    screen = None
    if settings["current_screen"] == START_SCREEN:
        screen =  main_menu_screen
    elif settings["current_screen"] == DESCRIPTION_SCREEN:
        screen = description_screen
    elif settings["current_screen"] == RESIZE_SCREEN:
        screen = edit_matrix_screen
    elif settings["current_screen"] == SEARCH_SCREEN:
        screen = define_edges_screen
    elif settings["current_screen"] == GAME_SCREEN:
        screen = game_Screen
    return screen

if __name__=="__main__":
    main()