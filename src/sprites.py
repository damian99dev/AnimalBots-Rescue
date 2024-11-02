from settings import *

class Sprite(pygame.sprite.Sprite):
    def __init__ (self, pos, surf = pygame.Surface((tile_size,tile_size)), groups = None):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.old_rect = self.rect.copy()