import pygame

def load_image(path):
    return pygame.image.load(path).convert_alpha()
