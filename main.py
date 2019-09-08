import pygame
import string
import math

from model.vertex import Vertex
from model.edge import Edge
from model.diijkstra import Diijkstra
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

def main():
    global matrix
    pygame.init()
    pygame.font.init()

    display = pygame.display
    display.set_caption(CAPTION)

    screen = display.set_mode(SCREEN_SIZE, 0, 32)

    running = True
    current_screen = 0

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
        screen.fill(BLACK)
        for event in pygame.event.get():
            pressed = pygame.key.get_pressed()
            running = not (event.type == pygame.QUIT or pressed[pygame.K_ESCAPE])
            if current_screen == 0:
                if pressed[pygame.K_RETURN]:
                    current_screen = 1
            elif current_screen == 1:
                matrix.define_matrix_size(pygame.mouse.get_pos())
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
                if pressed[pygame.K_1]:
                    start_to_search()
                elif pressed[pygame.K_RETURN]:
                    matrix.reset()
                    current_screen = 1

        if current_screen == 0:
            instructions_screen.draw()
        elif current_screen == 1:
            define_matrix_screen(screen)
        elif current_screen == 2:
            define_edges_screen(screen)
        display.flip()

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

if __name__=="__main__":
    main()