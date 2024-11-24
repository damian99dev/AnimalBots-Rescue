import pygame
from settings import *
from sprites import Sprite
from player import Player
from groups import AllSprites  # Importamos AllSprites para su uso en el nivel
from enemy import Enemy, Enemy3, Enemy4  # Importar la clase Enemy, Enemy3 y Enemy4
from game_over import GameOverScreen, get_font  # Importar GameOverScreen y get_font

class Level:
    def __init__(self, tmx_map):
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = AllSprites()  # Grupo general para todos los sprites con manejo de zoom
        self.collision_sprites = pygame.sprite.Group()  # Grupo de sprites con colisiones
        self.enemy_sprites = pygame.sprite.Group()  # Grupo para los enemigos
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
        # Cargar los enemigos
        self.load_enemies(tmx_map)

    def load_background_objects(self, tmx_map):
        # Cargamos la capa de objetos traspasables 
        backgtras_layer = tmx_map.get_layer_by_name('Backgtras')
        if backgtras_layer:
            for obj in backgtras_layer:
                if obj.name in ['boton', 'peligro', 'mancha', 'estalactitas2', 'yo', 'gemaB', 'gemaM','dino', 'rac', 'compu', 'cajas3', 'caja', 'compu2', 'cosa', 'estalactitas', 'victoria', 'linternal', 'fence', 'barril', 'arbol', 'mig', 'jos', 'dam', 'gre', 'rox', 'nao', 'flechaa', 'flechab','pinchos', 'negro',  'derecha', 'arbu', 'arbust', 'rocab', 'rocag', 'pa', 'st', 'laser', 'laser2','xor',  'laser3', 'fondo', 'picos1', 'naonao', 'picos2', 'picos3']:
                    image_path = f'graphics/Background/{obj.name}.png'  # Asegúrate de tener las imágenes en la carpeta 'graphics/Background'
                    object_image = pygame.image.load(image_path).convert_alpha()
                    object_image = pygame.transform.scale(object_image, (obj.width, obj.height))
                    Sprite((obj.x, obj.y), object_image, self.all_sprites)  # Agregar al grupo all_sprites (sin colisiones)

    def load_enemies(self, tmx_map):
        enemies_layer = tmx_map.get_layer_by_name('enemies')
        if enemies_layer:
            for obj in enemies_layer:
                if obj.name == 'enemy1':
                    image_path1 = 'graphics/enemies/enemy1.png'
                    image_path2 = 'graphics/enemies/enemy2.png'
                    enemy_image1 = pygame.image.load(image_path1).convert_alpha()
                    enemy_image2 = pygame.image.load(image_path2).convert_alpha()
                    enemy_image1 = pygame.transform.scale(enemy_image1, (obj.width, obj.height))
                    enemy_image2 = pygame.transform.scale(enemy_image2, (obj.width, obj.height))
                    enemy_images = [enemy_image1, enemy_image2]
                    enemy = Enemy((obj.x, obj.y), enemy_images, self.collision_sprites)
                    self.all_sprites.add(enemy)
                    self.enemy_sprites.add(enemy)
                elif obj.name == 'enemy3':
                    image_path1 = 'graphics/enemies/boss.png'
                    image_path2 = 'graphics/enemies/boss2.png'
                    enemy_image1 = pygame.image.load(image_path1).convert_alpha()
                    enemy_image2 = pygame.image.load(image_path2).convert_alpha()
                    enemy_image1 = pygame.transform.scale(enemy_image1, (obj.width, obj.height))
                    enemy_image2 = pygame.transform.scale(enemy_image2, (obj.width, obj.height))
                    enemy_images = [enemy_image1, enemy_image2]
                    enemy3 = Enemy3((obj.x, obj.y), enemy_images, self.collision_sprites)
                    self.all_sprites.add(enemy3)
                    self.enemy_sprites.add(enemy3)
                elif obj.name == 'enemy4':
                    image_paths = [
                        'graphics/enemies/toro2.png',
                        'graphics/enemies/toro3.png',
                        'graphics/enemies/toro4.png',
                        'graphics/enemies/toro5.png',
                        'graphics/enemies/toro6.png',
                        'graphics/enemies/toro7.png'
                    ]
                    enemy_images = []
                    for image_path in image_paths:
                        enemy_image = pygame.image.load(image_path).convert_alpha()
                        enemy_image = pygame.transform.scale(enemy_image, (obj.width, obj.height))
                        enemy_images.append(enemy_image)
                    enemy4 = Enemy4((obj.x, obj.y), enemy_images, self.collision_sprites)
                    self.all_sprites.add(enemy4)
                    self.enemy_sprites.add(enemy4)

    def run(self, dt):
        # Dibujamos el fondo si esta cargado
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

        # Verificar si el jugador ha colisionado con algún enemigo
        for enemy in self.enemy_sprites:
            if self.player.hitbox_rect.colliderect(enemy.player_hitbox_rect):
                from game_over import GameOverScreen, get_font
                game_over_screen = GameOverScreen(self.display_surface, get_font(60))
                game_over_screen.run()  # Mostrar la pantalla de derrota
                break  # Salir del bucle una vez que se detecta una colisión
