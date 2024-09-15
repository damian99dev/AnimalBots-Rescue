from settings import *
from sprites import Sprite
from player import Player

class Level:
    def __init__(self, tmx_map):
        self.display_surface = pygame.display.get_surface()
        
        #Creamos grupos
        self.all_sprites = pygame.sprite.Group() #Creamos un grupo general para todos los sprites
        self.collision_sprites  = pygame.sprite.Group() #Creamos el grupo de Sprites con colisiones

        self.setup(tmx_map)

    def setup(self, tmx_map):
        for x, y, surf in tmx_map.get_layer_by_name('Suelo').tiles(): #aqui estoy llamando la capa de suelo del tmx de tiled
            Sprite((x * tile_size,y * tile_size), surf, (self.all_sprites, self.collision_sprites))

        for obj in tmx_map.get_layer_by_name('Objetos'): #aqui estoy llamando la capa de objetos (en este caso la prota) del tmx de tiled
            if obj.name == 'prota':
                Player((obj.x, obj.y), self.all_sprites, self.collision_sprites)


    def run(self, dt):
        self.all_sprites.update(dt)
        self.display_surface.fill('black')
        self.all_sprites.draw(self.display_surface)