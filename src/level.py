import pygame
from settings import *
from sprites import Sprite
from player import Player
from groups import AllSprites  # Importamos AllSprites para su uso en el nivel
from game_over import GameOverScreen, get_font  # Importar GameOverScreen y get_font

class Level:
    def __init__(self, tmx_map):
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = AllSprites()  # Grupo general para todos los sprites con manejo de zoom
        self.collision_sprites = pygame.sprite.Group()  # Grupo de sprites con colisiones
        self.background_objects = pygame.sprite.Group()  # Grupo para objetos de fondo (sin colisiones)
        self.background = None
        self.fin_objects = []
        self.setup(tmx_map)

    def setup(self, tmx_map):
        # Cargamos la capa de fondo 'backg'
        backg_layer = tmx_map.get_layer_by_name('backg')
        if backg_layer:
            self.background = pygame.Surface((tmx_map.width * tile_size, tmx_map.height * tile_size))
            for x, y, surf in backg_layer.tiles():
                self.background.blit(surf, (x * tile_size, y * tile_size))
        # Cargamos la capa de suelo 'Suelo'
        for x, y, surf in tmx_map.get_layer_by_name('Suelo').tiles():
            Sprite((x * tile_size, y * tile_size), surf, (self.all_sprites, self.collision_sprites))
        # Cargamos la capa de objetos 'Objetos' (protagonista, meta y fin)
        for obj in tmx_map.get_layer_by_name('Objetos'):
            if obj.name == 'player':
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites)
            elif obj.name == 'meta':  # Detectar la meta
                self.meta_rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                self.meta_image = pygame.image.load('graphics/Background/meta.png').convert_alpha()
                self.meta_image = pygame.transform.scale(self.meta_image, (obj.width, obj.height))
                self.meta_pos = (obj.x, obj.y)
            elif obj.name == 'fin':  # Detectar el fin
                fin_rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                fin_image = pygame.image.load('graphics/Background/ded.png').convert_alpha()
                fin_image = pygame.transform.scale(fin_image, (obj.width, obj.height))
                self.fin_objects.append((fin_rect, fin_image, (obj.x, obj.y)))
        # Cargar los objetos de la capa 'Backgtras' (por ejemplo, árboles)
        self.load_background_objects(tmx_map)

    def load_background_objects(self, tmx_map):
        # Cargamos la capa de objetos traspasables 
        backgtras_layer = tmx_map.get_layer_by_name('Backgtras')
        if backgtras_layer:
            for obj in backgtras_layer:
                if obj.name in ['arbol', 'mig', 'jos', 'dam', 'gre', 'rox', 'nao', 'flechaa', 'flechab','pinchos', 'negro',  'derecha', 'arbu', 'arbust', 'rocab', 'rocag', 'pa', 'st', 'laser', 'laser2', 'laser3', 'fondo', 'picos1', 'picos2', 'picos3']:
                    image_path = f'graphics/Background/{obj.name}.png'  # Asegúrate de tener las imágenes en la carpeta 'graphics/Background'
                    object_image = pygame.image.load(image_path).convert_alpha()
                    object_image = pygame.transform.scale(object_image, (obj.width, obj.height))
                    Sprite((obj.x, obj.y), object_image, self.all_sprites)  # Agregar al grupo all_sprites (sin colisiones)

    def run(self, dt):
        # Dibujamos el fondo si está cargado
        if self.background:
            self.display_surface.blit(self.background, (0, 0))
    
        # Actualizamos y dibujamos los sprites con la cámara ajustada al jugador
        self.all_sprites.update(dt)
        self.all_sprites.draw(self.player.hitbox_rect.center, self.player)  # Aquí se usa el centro del jugador para centrar la cámara
        self.display_surface.blit(self.meta_image, self.meta_pos)
        for fin_rect, fin_image, fin_pos in self.fin_objects:
            self.display_surface.blit(fin_image, fin_pos)
        # Verificar si el jugador ha alcanzado la meta
        if self.player.hitbox_rect.colliderect(self.meta_rect):
            from victory import VictoryScreen
            victory_screen = VictoryScreen()
            victory_screen.run()  # Mostrar la pantalla de victoria
        # Verificar si el jugador ha alcanzado alguno de los objetos 'fin'
        for fin_rect, _, _ in self.fin_objects:
            if self.player.hitbox_rect.colliderect(fin_rect):
                from game_over import GameOverScreen, get_font
                game_over_screen = GameOverScreen(self.display_surface, get_font(60))
                game_over_screen.run()  # Mostrar la pantalla de derrota
                break  # Salir del bucle una vez que se detecta una colisión
