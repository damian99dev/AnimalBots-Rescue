import pygame, sys #importo las librerias
from pygame.math import Vector2 as vector

window_width, window_height = 1024, 1024 #creamos el alto y ancho de la pantalla
tile_size = 32
animation_speed = 6

z_layers = {
    'bg': 0,
    'clouds': 1,
    'bg tiles': 2,
    'path': 2,
    'bg details': 4,
    'main': 5,
    'fg': 7,
}