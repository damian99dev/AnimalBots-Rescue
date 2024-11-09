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
        # Ajustamos el centro de la cámara y añadimos un desplazamiento adicional en el eje X
        camera_offset_x = 100  # Ajusta este valor según sea necesario
        self.offset.x = target_pos[0] - (window_width / 2 / self.zoom_factor) + camera_offset_x
        self.offset.y = target_pos[1] - (window_height / 2 / self.zoom_factor)

        # Definir el rectángulo de la cámara
        camera_rect = pygame.Rect(
            self.offset.x,
            self.offset.y,
            window_width / self.zoom_factor,
            window_height / self.zoom_factor
        )

        # Dibujamos todos los objetos traspasables primero
        for sprite in sorted(self, key=lambda s: s.rect.bottom):
            if sprite != player and camera_rect.colliderect(sprite.rect):  # Asegurarse de no dibujar el jugador en este grupo y solo dibujar los visibles
                scaled_image = pygame.transform.scale(
                    sprite.image,
                    (int(sprite.rect.width * self.zoom_factor), int(sprite.rect.height * self.zoom_factor))
                )
                offset_pos = (sprite.rect.topleft - self.offset) * self.zoom_factor
                self.display_surface.blit(scaled_image, offset_pos)

        # Dibujamos el jugador
        player_scaled_image = pygame.transform.scale(
            player.image,
            (int(player.rect.width * self.zoom_factor), int(player.rect.height * self.zoom_factor))
        )
        player_offset_pos = (player.rect.topleft - self.offset) * self.zoom_factor
        self.display_surface.blit(player_scaled_image, player_offset_pos)
