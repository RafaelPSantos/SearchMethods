# coding: utf-8

import pygame
import string
import math

from model.vertex import Vertex
from model.edge import Edge
from model.diijkstra import Diijkstra
from model.manhattan_distance import ManhattanDistance
from model.instructions_screen import InstructionsScreen
from model.matrix import Matrix

CAPTION = "Search Methods"

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
resize_matrix_screen = None
current_screen = 0
running = True

def main():
    global instructions_screen
    global current_screen
    global matrix
    global running

    pygame.init()
    pygame.font.init()

    display = pygame.display
    display.set_caption(CAPTION)

    screen = display.set_mode(SCREEN_SIZE, 0, 32)

    instructions_title = "Bem Vindo ao " + CAPTION
    paragraphs = []
    paragraphs.append("")
    paragraphs.append("O " + CAPTION +" é um programa para demonstrar diferentes metodos de busca.")
    paragraphs.append("Nele você poderá definir os vertices e as aresta que quiser, bem como o inicio e fim.")
    paragraphs.append("")
    paragraphs.append("Você pode prosseguir para proma tela a hora que quiser, basta pressionar ENTER.")
    paragraphs.append("Mas caso queira, tambem pode ficar aqui mais um pouco e ler as instruções:")
    paragraphs.append("")
    paragraphs.append("1.1 - Na proxima tela, você irá se deparar com a tela para decidir o tamanho da matriz")
    paragraphs.append("1.2 - Para decidir o tamanho da matriz, basta arastar o mouse até o canto direito inferior,")
    paragraphs.append("e, dependendo quando estiver satisfeito com o tamanho, clique com o botão esquerdo")
    paragraphs.append("2.1 - Na proxima tela, você poderá decidir as arestas bem como o ponto inicial e final")
    paragraphs.append("2.2 - Para criar uma aresta, clique sobre um vertice e depois sobre outro proximo,")
    paragraphs.append("quando você clicar sobre um vertice, notará a mudança de cor dos demais.")
    paragraphs.append("* os vertices brancos, são os que é possivel criar uma aresta em comum")
    paragraphs.append("* os vertices cinzas, estão muito longes para se criar uma aresta")
    paragraphs.append("* os vertices laranjas, ja possuem aresta e clicando sobre eles, irá remover a mesma")
    paragraphs.append("2.2 - Para escolher o ponto de inicio, e fim, clique usando o botão direito do mouse")
    paragraphs.append("* o vertice verde será o inicio da procura")
    paragraphs.append("* o vertice azul será o destino da procura")
    paragraphs.append("3.1 - Quando quiser iniciar a procura, pressione o botão 1, e sera feita utilizando:")
    paragraphs.append("Diijkstra")

    instructions_screen = InstructionsScreen(pygame.font, screen)
    instructions_screen.add_text(instructions_title, paragraphs)

    matrix = Matrix(MAX_ARRAY_SIZE, MAX_ARRAY_SIZE, pygame)

    while running:
        handle_events(pygame)
        handle_screens(screen, display)

def define_matrix_screen(screen):
    matrix.draw_vertex(screen)

def define_edges_screen(screen):
    matrix.draw_edges(screen)
    matrix.draw_vertex(screen)

def start_to_search(method = 0):
    search = Diijkstra(matrix.find_entrace_vertice(), matrix.find_target_vertice(), matrix.flat_vertices())
    search.search_path()
    search.select_path_to_target()
    search.print_table()

    m = ManhattanDistance(matrix.find_entrace_vertice(), matrix.find_target_vertice(), matrix.flat_vertices())
    print(m.calculate())

def handle_screens(screen, display):
    global current_screen
    global instructions_screen
    screen.fill(BLACK)
    if current_screen == 0:
        instructions_screen.draw()
    elif current_screen == 1:
        define_matrix_screen(screen)
    elif current_screen == 2:
        define_edges_screen(screen)
        draw_legend(screen)
    display.flip()

def handle_events(pygame):
    global running
    for event in pygame.event.get():
        pressed = pygame.key.get_pressed()
        running = not (event.type == pygame.QUIT or pressed[pygame.K_ESCAPE])
        handle_mouse(pygame.mouse, event)
        handle_keys(pressed)

def handle_mouse(mouse, event):
    global current_screen
    if current_screen == 0:
        pass
    elif current_screen == 1:
        matrix.define_matrix_size(mouse.get_pos())
        if event.type == pygame.MOUSEBUTTONUP:
            matrix.remove_unselected_vertices()
            current_screen = 2
    elif current_screen == 2:
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == MOUSE_LEFT_BUTTON:
                if matrix.any_vertex_bellow_mouse(event.pos[0], event.pos[1]):
                    matrix.define_edges(event.pos[0], event.pos[1])
            elif event.button == MOUSE_RIGHT_BUTTON:
                matrix.select_targets(event.pos[0], event.pos[1])

def handle_keys(pressed):
    global current_screen
    if current_screen == 0:
        if pressed[pygame.K_RETURN]:
                    current_screen = 1
    elif current_screen == 1:
        pass
    elif current_screen == 2:
        if pressed[pygame.K_1]:
            start_to_search()
        elif pressed[pygame.K_RETURN]:
            matrix.reset()
            current_screen = 1


def draw_legend(screen):
    global matrix
    margin = 5
    pos_x = 10
    pos_y = 10
    rec_side = 20
    pos_y = draw_legend_rect(screen, pos_x, pos_y, "inicio", matrix.entrace_color, rec_side)
    pos_y = draw_legend_rect(screen, pos_x, pos_y, "fim", matrix.target_color, rec_side)
    pos_y = draw_legend_rect(screen, pos_x, pos_y, "não selecionado", matrix.normal_color, rec_side)
    pos_y = draw_legend_rect(screen, pos_x, pos_y, "selecionado", matrix.selected_color, rec_side)
    pos_y = draw_legend_rect(screen, pos_x, pos_y, "desabilitado", matrix.disabled_color, rec_side)
    pos_y = draw_legend_rect(screen, pos_x, pos_y, "conectado", matrix.connected_color, rec_side)
    pos_y = draw_legend_rect(screen, pos_x, pos_y, "caminho", matrix.path_color, rec_side)

def draw_legend_rect(screen, pos_x, pos_y, text, color, rec_side):
    pygame.draw.rect(screen, color, (pos_x, pos_y, rec_side, rec_side))

    monospace_font = pygame.font.SysFont("arial", Matrix.VERTEX_NAME_SIZE)
    label = monospace_font.render(text, 1, color)
    text_size = label.get_rect()
    text_pos = (pos_x, pos_y + rec_side)
    screen.blit(label, text_pos)
    return text_pos[1] + text_size.height

if __name__=="__main__":
    main()