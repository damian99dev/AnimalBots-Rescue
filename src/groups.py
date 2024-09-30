import pygame
from settings import *

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = vector()
        self.zoom_factor = 3  #Aqui definimos el zoom que queremos hacer a la protagonista

    def set_zoom(self, zoom_factor):
        self.zoom_factor = zoom_factor

    def draw(self, target_pos):
        # Ajustamos el centro de la cámara
        self.offset.x = -(target_pos[0] - window_width / 2) * self.zoom_factor
        self.offset.y = -(target_pos[1] - window_height / 2) * self.zoom_factor

        for sprite in self:
            # Escalar el sprite según el factor de zoom
            scaled_image = pygame.transform.scale(
                sprite.image, 
                (int(sprite.rect.width * self.zoom_factor), int(sprite.rect.height * self.zoom_factor))
            )

            # Calculamos la posición del sprite con el offset ajustado
            offset_pos = (sprite.rect.topleft - vector(target_pos)) * self.zoom_factor + vector(window_width / 2, window_height / 2)

            # Dibujamos el sprite escalado
            self.display_surface.blit(scaled_image, offset_pos)
