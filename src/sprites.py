from settings import *

class Sprite(pygame.sprite.Sprite):
    def __init__ (self, pos, surf, groups):
        super().__init__(groups)
        self.image = pygame.Surface((tile_size,tile_size))
        self.image.fill('white')
        self.rect = self.image.get_rect(topleft = pos)
        self.old_rect = self.rect.copy()