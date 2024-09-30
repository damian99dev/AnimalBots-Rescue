import pygame
from settings import *
from sprites import Sprite
from player import Player
from groups import AllSprites  # Importamos AllSprites para su uso en el nivel

class Level:
    def __init__(self, tmx_map):
        self.display_surface = pygame.display.get_surface()

        # Creamos grupos
        self.all_sprites = AllSprites()  # Grupo general para todos los sprites con manejo de zoom
        self.collision_sprites = pygame.sprite.Group()  # Grupo de sprites con colisiones
        self.background_objects = pygame.sprite.Group()  # Grupo para objetos de fondo (sin colisiones)

        # Inicializamos el fondo
        self.background = None

        # Configuramos el nivel
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

        # Cargamos la capa de objetos 'Objetos' (protagonista y meta)
        for obj in tmx_map.get_layer_by_name('Objetos'):
            if obj.name == 'player':
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites)
            elif obj.name == 'meta':  # Detectar la meta
                self.meta_rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                
                self.meta_image = pygame.image.load('graphics/Background/meta.png').convert_alpha()
                self.meta_image = pygame.transform.scale(self.meta_image, (obj.width, obj.height))
                self.meta_pos = (obj.x, obj.y)

        # Cargar los objetos de la capa 'Backgtras' (por ejemplo, árboles)
        self.load_background_objects(tmx_map)

    def load_background_objects(self, tmx_map):
    # Cargamos la capa de objetos traspasables como 'arbol', 'mig', 'jos', 'dam', 'gre', 'rox', 'nao'
        backgtras_layer = tmx_map.get_layer_by_name('Backgtras')
        if backgtras_layer:
            for obj in backgtras_layer:
                if obj.name == 'arbol':
                    # Crear un sprite sin colisión para el árbol
                    tree_image = pygame.image.load('graphics/Background/arbol.png').convert_alpha()  # Asegúrate de tener esta imagen en la ruta correcta
                    tree_image = pygame.transform.scale(tree_image, (obj.width, obj.height))
                    Sprite((obj.x, obj.y), tree_image, self.all_sprites)  # Agregar al grupo all_sprites (sin colisiones)

                # Agregar objetos traspasables adicionales
                elif obj.name in ['mig', 'jos', 'dam', 'gre', 'rox', 'nao']:
                    # Ruta a las imágenes correspondientes para cada objeto
                    image_path = f'graphics/Background/{obj.name}.png'  # Asegúrate de tener las imágenes en la carpeta 'graphics/objects'
                    object_image = pygame.image.load(image_path).convert_alpha()
                    object_image = pygame.transform.scale(object_image, (obj.width, obj.height))
                    Sprite((obj.x, obj.y), object_image, self.all_sprites)  # Agregar al grupo all_sprites (sin colisiones)
    # Solo agregar al grupo all_sprites, no a colisiones

    def run(self, dt):
        # Dibujamos el fondo si está cargado
        if self.background:
            self.display_surface.blit(self.background, (0, 0))
    
        # Actualizamos y dibujamos los sprites con la cámara ajustada al jugador
        self.all_sprites.update(dt)
        self.all_sprites.draw(self.player.hitbox_rect.center)  # Aquí se usa el centro del jugador para centrar la cámara

        self.display_surface.blit(self.meta_image, self.meta_pos)

        # Verificar si el jugador ha alcanzado la meta
        if self.player.hitbox_rect.colliderect(self.meta_rect):
            from victory import VictoryScreen
            victory_screen = VictoryScreen()
            victory_screen.run()  # Mostrar la pantalla de victoria
