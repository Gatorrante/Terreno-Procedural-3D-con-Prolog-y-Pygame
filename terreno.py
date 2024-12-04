import pygame
import sys
import math
from copy import deepcopy
from pyswip import Prolog
import noise

# Inicialización de Pygame
pygame.init()
pygame.display.set_caption('Terreno procedural 3D con Prolog | Proyecto de Investigación | UTP')
screen = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()

FOV = 90
FOG = True

def offset_polygon(polygon, offset):
    for point in polygon:
        point[0] += offset[0]
        point[1] += offset[1]
        point[2] += offset[2]

def project_polygon(polygon):
    projected_points = []
    for point in polygon:
        x_angle = math.atan2(point[0], point[2])
        y_angle = math.atan2(point[1], point[2])
        x = x_angle / math.radians(FOV) * screen.get_width() + screen.get_height() // 2
        y = y_angle / math.radians(FOV) * screen.get_width() + screen.get_width() // 2
        projected_points.append([x, y])
    return projected_points

def gen_polygon(polygon_base, polygon_data):
    generated_polygon = deepcopy(polygon_base)
    offset_polygon(generated_polygon, polygon_data['pos'])
    return project_polygon(generated_polygon)

# Configuración del terreno
poly_data = {
    'pos': [0, 0, 4.5],
    'rot': [0, 0, 0],
}

square_polygon = [
    [-0.5, 0.5, -0.5],
    [0.5, 0.5, -0.5],
    [0.5, 0.5, 0.5],
    [-0.5, 0.5, 0.5],
]

polygons = []
prolog = Prolog()
prolog.consult("generador.pl")  # Consulta de parametros de prolog

altura_cache = {}
color_cache = {}

def get_altura(x, y):
    if (x, y) in altura_cache:
        return altura_cache[(x, y)]
    perlin_value = noise.pnoise2(x / 10, y / 10)
    altura_query = list(prolog.query(f"altura({x}, {y}, {perlin_value}, Altura)"))
    altura = altura_query[0]['Altura'] if altura_query else 0
    altura_cache[(x, y)] = altura
    return altura

def get_color(altura):
    if altura in color_cache:
        return color_cache[altura]
    color_query = list(prolog.query(f"color({altura}, R, G, B)"))
    color = tuple(color_query[0][channel] for channel in ['R', 'G', 'B']) if color_query else (255, 255, 255)
    color_cache[altura] = color
    return color

def generate_poly_row(y):
    global polygons
    for x in range(50):
        poly_copy = deepcopy(square_polygon)
        offset_polygon(poly_copy, [x - 25, 5, y + 5])

        for corner in poly_copy:
            corner[1] -= get_altura(corner[0], corner[2])

        altura_promedio = sum(corner[1] for corner in poly_copy) / len(poly_copy)
        color = get_color(altura_promedio)

        polygons.insert(0, [poly_copy, color])

# Generar filas
next_row = 0
for y in range(26):
    generate_poly_row(y)
    next_row += 1

# Generar ruido para las nubes
noise_surf = pygame.Surface((100, 100))
for x in range(100):
    for y in range(100):
        v = noise.pnoise2(x / 30, y / 30)
        v = (v + 1) / 2
        noise_surf.set_at((x, y), (v * 255, v * 255, v * 255))

while True:
    bg_surf = pygame.Surface(screen.get_size())
    bg_surf.fill((100, 200, 250))
    display = screen.copy()
    display.blit(bg_surf, (0, 0))
    bg_surf.set_alpha(120)

    poly_data['pos'][2] -= 0.25

    if polygons[-1][0][0][2] < -poly_data['pos'][2]:
        polygons = polygons[:-30]
        generate_poly_row(next_row)
        next_row += 1

    for i, polygon in enumerate(polygons):
        if FOG and (i % 90 == 0) and (i != 0) and (i < 30 * 18):
            display.blit(bg_surf, (0, 0))
        render_poly = gen_polygon(polygon[0], poly_data)
        poly2 = deepcopy(render_poly)
        for v in poly2:
            v[1] = 100 - v[1] * 0.2
            v[0] = 500 - v[0]
        pygame.draw.polygon(display, polygon[1], render_poly)
        d = polygon[0][0][1]
        if d < 5:
            pygame.draw.polygon(display, (min(max(0, d * 20) + 150, 255), min(max(0, d * 20) + 150, 255), min(max(0, d * 20) + 150, 255)), poly2)

    display.set_alpha(150)
    screen.blit(display, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.flip()
    clock.tick(60)