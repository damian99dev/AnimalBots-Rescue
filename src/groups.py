import pygame
from settings import *

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = vector()
        self.zoom_factor = 3  # Aquí definimos el zoom que queremos hacer a la protagonista

    def set_zoom(self, zoom_factor):
        self.zoom_factor = zoom_factor

    def draw(self, target_pos, player):
        # Ajustamos el centro de la cámara
        self.offset.x = -(target_pos[0] - window_width / 2) * self.zoom_factor
        self.offset.y = -(target_pos[1] - window_height / 2) * self.zoom_factor

        # Dibujamos todos los objetos traspasables primero
        for sprite in sorted(self, key=lambda s: s.rect.bottom):
            if sprite != player:  # Asegurarse de no dibujar el jugador en este grupo
                scaled_image = pygame.transform.scale(
                    sprite.image,
                    (int(sprite.rect.width * self.zoom_factor), int(sprite.rect.height * self.zoom_factor))
                )
                offset_pos = (sprite.rect.topleft - vector(target_pos)) * self.zoom_factor + vector(window_width / 2, window_height / 2)
                self.display_surface.blit(scaled_image, offset_pos)

        # Dibujamos el jugador
        player_scaled_image = pygame.transform.scale(
            player.image,
            (int(player.rect.width * self.zoom_factor), int(player.rect.height * self.zoom_factor))
        )
        player_offset_pos = (player.rect.topleft - vector(target_pos)) * self.zoom_factor + vector(window_width / 2, window_height / 2)
        self.display_surface.blit(player_scaled_image, player_offset_pos)


        # Dibujamos el jugador
        player_scaled_image = pygame.transform.scale(
            player.image, 
            (int(player.rect.width * self.zoom_factor), int(player.rect.height * self.zoom_factor))
        )
        player_offset_pos = (player.rect.topleft - vector(target_pos)) * self.zoom_factor + vector(window_width / 2, window_height / 2)
        self.display_surface.blit(player_scaled_image, player_offset_pos)

