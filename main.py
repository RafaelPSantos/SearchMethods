import pygame
import string
import math

from model.vertex import Vertex
from model.edge import Edge
from model.diijkstra import Diijkstra
from model.instructions_screen import InstructionsScreen

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
entrace = None
target = None
edges = []

def main():
    pygame.init()
    pygame.font.init()

    display = pygame.display
    display.set_caption(CAPTION)

    screen = display.set_mode(SCREEN_SIZE, 0, 32)

    initialize_vertex()

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

    while running:
        screen.fill(BLACK)
        for event in pygame.event.get():
            pressed = pygame.key.get_pressed()
            running = not (event.type == pygame.QUIT or pressed[pygame.K_ESCAPE])
            if current_screen == 0:
                if pressed[pygame.K_RETURN]:
                    current_screen = 1
            elif current_screen == 1:
                define_matrix_size(pygame.mouse.get_pos())
                if event.type == pygame.MOUSEBUTTONUP:
                    remove_unselected_vertices()
                    current_screen = 2
            elif current_screen == 2:
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == MOUSE_LEFT_BUTTON:
                        define_edges(event.pos[0], event.pos[1])
                    elif event.button == MOUSE_RIGHT_BUTTON:
                        select_targets(event.pos[0], event.pos[1])
                if pressed[pygame.K_1]:
                    start_to_search()

        if current_screen == 0:
            instructions_screen.draw()
        elif current_screen == 1:
            define_matrix_screen(screen)
        elif current_screen == 2:
            define_edges_screen(screen)
        display.flip()

def define_matrix_screen(screen):
    draw_vertex(screen)

def define_edges_screen(screen):
    draw_edges(screen)
    draw_vertex(screen)

def draw_vertex(screen):
    monospace_font = pygame.font.SysFont("arial", VERTEX_NAME_SIZE)

    first_selected = None
    for vertex in flat_vertices():
        if vertex.selected:
            first_selected = vertex
            break

    for vertex in flat_vertices():
        color = WHITE
        if vertex.selected:
            color = YELLOW
        elif vertex is entrace:
            color = GREEN
        elif vertex is target:
            color = BLUE
        elif type(first_selected) is Vertex:
            if not first_selected.is_directly_neighbor_of(vertex):
                color = GREY
            elif vertex.is_conected_to(first_selected):
                color = ORANGE
        vertex_pos = (vertex.pos_x, vertex.pos_y)
        pygame.draw.circle(screen, color, vertex_pos, vertex.radio)

        label = monospace_font.render(vertex.name, 1, RED)
        text_size = label.get_rect()
        text_pos = (vertex.pos_x - text_size.width/2, vertex.pos_y - text_size.height/2)
        screen.blit(label, text_pos)

def draw_edges(screen):
    for edge in edges:
        color = WHITE
        if edge.first_vertex.selected or edge.second_vertex.selected:
            color = ORANGE
        pygame.draw.line(screen, color, edge.start(), edge.end(), 5)

def define_edges(pos_x, pos_y):
    selected_vertices = []
    vertex = flat_vertices()[0]
    distance = math.sqrt((pos_x - vertex.pos_x) ** 2 + (pos_y - vertex.pos_y) ** 2)

    for vertex in flat_vertices():
        distance = math.sqrt((pos_x - vertex.pos_x) ** 2 + (pos_y - vertex.pos_y) ** 2)
        if distance <= vertex.radio:
            vertex.selected = True
        if vertex.selected:
            selected_vertices.append(vertex)
    if len(selected_vertices) >= 2:
        first_vertex, second_vertex = selected_vertices
        if first_vertex.is_directly_neighbor_of(second_vertex):
            comon_edge = first_vertex.comon_edge_with(second_vertex)
            if type(comon_edge) is Edge:
                first_vertex.remove_edge(comon_edge)
                second_vertex.remove_edge(comon_edge)
                edges.remove(comon_edge)
            else:
                edges.append(Edge(first_vertex, second_vertex))
        for vertex in flat_vertices():
            vertex.selected = False

def select_targets(pos_x, pos_y):
    global entrace
    global target
    if not type(entrace) is Vertex:
        entrace = vertex_bellow_mouse(pos_x, pos_y)
    elif entrace == vertex_bellow_mouse(pos_x, pos_y):
        entrace = None
    elif not type(target) is Vertex:
        target = vertex_bellow_mouse(pos_x, pos_y)
    elif target == vertex_bellow_mouse(pos_x, pos_y):
        target = None


def vertex_bellow_mouse(mouse_pos_x, mouse_pos_y):
    for vertex in flat_vertices():
        distance = math.sqrt((mouse_pos_x - vertex.pos_x) ** 2 + (mouse_pos_y - vertex.pos_y) ** 2)
        if distance <= vertex.radio:
            return vertex

def define_matrix_size(mouse_pos):
    mouse_pos_x, mouse_pos_y = mouse_pos
    min_pos = min(mouse_pos_x, mouse_pos_y)
    for vertex in flat_vertices():
        horizontal_range = vertex.pos_x - vertex.radio < min_pos
        vertical_range = vertex.pos_y - vertex.radio < min_pos
        vertex.selected = (horizontal_range and vertical_range) or (vertex.line < 2 and vertex.column < 2)

def remove_unselected_vertices():
    global vertices
    new_list = []
    for column in vertices:
        new_line = []
        for vertex in column:
            if vertex.selected:
                new_line.append(vertex)
                vertex.selected = False
        new_list.append(new_line)
    vertices = new_list

def initialize_vertex():
    for line in range(MAX_ARRAY_SIZE):
        new_line = []
        for column in range(MAX_ARRAY_SIZE):
            name = Vertex.generate_a_name(string.ascii_uppercase, line + column * MAX_ARRAY_SIZE)
            pos_x = (1 + line) * VERTEX_DISTANCE + 60
            pos_y = (1 + column) * VERTEX_DISTANCE + 60
            new_line.append(Vertex(name, pos_x, pos_y, line, column, VERTEX_RADIO))
        vertices.append(new_line)
        # vertices[X][Y]

def flat_vertices(with_removed = False):
    flatted_list = []
    for column in range(len(vertices)):
        for line in range(len(vertices[column])):
            flatted_list.append(vertices[line][column])
    return flatted_list

def start_to_search(method = 0):
    search = Diijkstra(entrace, target, flat_vertices())
    search.search_path()
    search.select_path_to_target()
    search.print_table()

if __name__=="__main__":
    main()