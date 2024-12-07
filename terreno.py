"""
Proyecto Final: Terreno Procedural 3D con Prolog y Pygame
Curso: Programación Lógica y Funcional

Este proyecto genera un terreno 3D de manera procedural utilizando ruido Perlin y reglas definidas en Prolog.
El terreno se renderiza en tiempo real utilizando Pygame. La altura y el color del terreno se determinan
mediante consultas a Prolog, lo que permite una generación dinámica y variada del paisaje.

Se han agregado comentarios para facilitar la comprensión del código.
"""
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

# Configuración de la cámara
FOV = 90
FOG = True

# Inicialización de Prolog
prolog = Prolog()
prolog.consult("generador.pl")  # Consulta de parámetros de Prolog

# Cachés para almacenar alturas y colores calculados
altura_cache = {}
color_cache = {}

# Función para obtener la altura de un punto (x, y)
def get_altura(x, y):
    if (x, y) in altura_cache:
        return altura_cache[(x, y)]
    perlin_value = noise.pnoise2(x / 10, y / 10)
    altura_query = list(prolog.query(f"altura({x}, {y}, {perlin_value}, Altura)"))
    altura = altura_query[0]['Altura'] if altura_query else 0
    altura_cache[(x, y)] = altura
    return altura

# Función para interpolar entre dos colores
def interpolate_color(color1, color2, factor):
    return tuple(int(color1[i] + (color2[i] - color1[i]) * factor) for i in range(3))

# Obtención del color segun la altura
def get_color(altura):
    if altura in color_cache:
        return color_cache[altura]
    color_query = list(prolog.query(f"color({altura}, R, G, B)"))
    color = tuple(color_query[0][channel] for channel in ['R', 'G', 'B']) if color_query else (255, 255, 255)
    color_cache[altura] = color
    return color

# Desplazamiento mediante el offset
def offset_polygon(polygon, offset):
    for point in polygon:
        point[0] += offset[0]
        point[1] += offset[1]
        point[2] += offset[2]

# Proyección de poligono 3D en 2D
def project_polygon(polygon):
    projected_points = []
    for point in polygon:
        x_angle = math.atan2(point[0], point[2])
        y_angle = math.atan2(point[1], point[2])
        x = x_angle / math.radians(FOV) * screen.get_width() + screen.get_height() // 2
        y = y_angle / math.radians(FOV) * screen.get_width() + screen.get_width() // 2
        projected_points.append([x, y])
    return projected_points

# Desplazamiento y proyección de poligonos
def gen_polygon(polygon_base, polygon_data):
    generated_polygon = [point[:] for point in polygon_base]  
    offset_polygon(generated_polygon, polygon_data['pos'])
    return project_polygon(generated_polygon)

# Generación de poligonos
def generate_poly_row(y):
    global polygons
    for x in range(50):  
        poly_copy = [point[:] for point in square_polygon]  
        offset_polygon(poly_copy, [x - 25, 5, y + 5])  

        water = True
        depth = 0

        for corner in poly_copy:
            v = noise.pnoise2(corner[0] / 10, corner[2] / 10, octaves=2) * 3
            v2 = noise.pnoise2(corner[0] / 30 + 1000, corner[2] / 30)
            if v < 0:
                depth -= v
                v = 0
            else:
                water = False
            corner[1] -= v * 4.5

        # Suavizador de colores según su altura
        altura_promedio = sum(corner[1] for corner in poly_copy) / len(poly_copy)
        if water:
            color_agua = interpolate_color((0, 50, 150), (0, 120, 255), min(1, depth / 10))
            c = color_agua
        else:
            color_terreno = interpolate_color((139, 69, 19), (34, 139, 34), min(1, (altura_promedio - 1) / 4))
            c = color_terreno

        polygons = [[poly_copy, c]] + polygons

# Función para generar un plano de agua
def generate_water_plane(x_offset, y_offset):
    water_polygon = [point[:] for point in square_polygon] 
    offset_polygon(water_polygon, [x_offset, 5, y_offset])
    for corner in water_polygon:
        corner[1] = 0 
    color_agua = interpolate_color((0, 50, 150), (0, 120, 255), 1)
    polygons.append([water_polygon, color_agua])

# Configuración del terreno
poly_data = {
    'pos': [0, 0, 0],
    'rot': [0, 0, 0],
}

# Definición del polígono base (cuadrado)
square_polygon = [
    [-0.5, 0.5, -0.5],
    [0.5, 0.5, -0.5],
    [0.5, 0.5, 0.5],
    [-0.5, 0.5, 0.5],
]

# Lista de polígonos generados
polygons = []

# Generar filas de terreno
next_row = 0
for y in range(26):
    generate_poly_row(y)
    next_row += 1

# Generar planos de agua a los costados
for i in range(-25, -20): 
    generate_water_plane(i, 5)
for i in range(20, 25):  
    generate_water_plane(i, 5)

# Ruido para las nubes
noise_surf = pygame.Surface((100, 100))
for x in range(100):
    for y in range(100):
        v = noise.pnoise2(x / 30, y / 30)
        v = (v + 1) / 2
        noise_surf.set_at((x, y), (v * 255, v * 255, v * 255))

# Fondo del cielo
bg_surf = pygame.Surface(screen.get_size())
bg_surf.fill((100, 200, 250))
bg_surf.set_alpha(120)

# Sol
sun_pos = [450, 100]  # Posición inicial del sol (más abajo)
sun_radius = 40  # Radio del sol
sun_color_start = (255, 255, 0)  # Color amarillo del sol (inicio)
sun_color_end = (255, 165, 0)  # Color naranja del sol (fin)

# Dibuja un círculo con gradiente
def draw_gradient_circle(surface, color_start, color_end, center, radius):
    for i in range(radius):
        color = interpolate_color(color_start, color_end, i / radius)
        pygame.draw.circle(surface, color, center, radius - i)

# Bucle principal 
while True:
    display = screen.copy()
    display.blit(bg_surf, (0, 0))

    # Control de la posición 
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        poly_data['pos'][0] -= 0.1
        poly_data['rot'][1] -= 0.5 
    if keys[pygame.K_RIGHT]:
        poly_data['pos'][0] += 0.1
        poly_data['rot'][1] += 0.5  
    if keys[pygame.K_UP]:
        poly_data['pos'][2] -= 0.1
    if keys[pygame.K_DOWN]:
        poly_data['pos'][2] += 0.1

    # Limita la rotación para evitar mirar hacia atrás
    poly_data['rot'][1] = max(-45, min(45, poly_data['rot'][1]))  # Rango limitado de rotación

    poly_data['pos'][2] -= 0.25

    # Genera nuevas filas de terreno si es necesario
    if polygons[-1][0][0][2] < -poly_data['pos'][2]:
        polygons = polygons[:-30]
        generate_poly_row(next_row)
        next_row += 1

    # Dibuja los polígonos
    for i, polygon in enumerate(polygons):
        if FOG and (i % 90 == 0) and (i != 0) and (i < 30 * 18):
            display.blit(bg_surf, (0, 0))
        render_poly = gen_polygon(polygon[0], poly_data)
        poly2 = [point[:] for point in render_poly]  # Evitar deepcopy
        for v in poly2:
            v[1] = 100 - v[1] * 0.2
            v[0] = 500 - v[0]
        # Asegurar de que el color es una tupla RGB válida
        if isinstance(polygon[1], tuple) and len(polygon[1]) == 3 and all(isinstance(c, int) and 0 <= c <= 255 for c in polygon[1]):
            pygame.draw.polygon(display, polygon[1], render_poly)
        else:
            print(f"Color inválido: {polygon[1]}")
        d = polygon[0][0][1]
        if d < 5:
            pygame.draw.polygon(display, (min(max(0, d * 20) + 150, 255), min(max(0, d * 20) + 150, 255), min(max(0, d * 20) + 150, 255)), poly2)

    # Dibuja el sol con gradiente
    draw_gradient_circle(display, sun_color_start, sun_color_end, sun_pos, sun_radius)

    # Aplica transparencia y actualizar la pantalla
    display.set_alpha(150)
    screen.blit(display, (0, 0))

    # Maneja eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Actualiza la pantalla
    pygame.display.flip()
    clock.tick(120)