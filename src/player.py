from settings import *
import os

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprite):
        super().__init__(groups)
        # Ruta relativa para cargar la imagen 'mona china 1.png'
        base_path = os.path.dirname(__file__)  # Directorio donde está player.py
        img_path = os.path.join(base_path, '..', 'graphics', 'Protagonist', 'mona china 1.png')

        # Cargar la imagen del protagonista
        self.image = pygame.image.load(img_path).convert_alpha()

        #Rectangulos
        self.rect = self.image.get_rect(topleft = pos)
        self.old_rect = self.rect.copy()


        #Creamos el movimiento del personaje
        self.direction = vector()
        self.speed = 200
        self.gravity = 600
        self.jump = False
        self.jump_dist = 400

        #Creamos las colisiones
        self.collision_sprites = collision_sprite
        self.on_surface = {'Suelo': False, 'left': False, 'right': False}
    
    def input(self):
        keys = pygame.key.get_pressed()
        input_vector = vector(0,0)
        if keys[pygame.K_RIGHT]:
            input_vector.x += 1       
        if keys[pygame.K_LEFT]:
            input_vector.x -= 1
        self.direction.x = input_vector.normalize().x if input_vector else input_vector.x

        if keys[pygame.K_SPACE]:
            self.jump = True

    def move(self, dt):
        #Movimiento horizontal
        self.rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')

        #Movimiento vertical
        self.direction.y += self.gravity / 2 * dt
        self.rect.y += self.direction.y * dt
        self.direction.y += self.gravity / 2 * dt
        self.collision('vertical')

        if self.jump:
            if self.on_surface['Suelo']:
                self.direction.y = -self.jump_dist
            self.jump = False

    def check_contact(self):
        floor_rect = pygame.Rect(self.rect.bottomleft,(self.rect.width,2))
        collide_rects = [sprite.rect for sprite in self.collision_sprites]

        self.on_surface['Suelo'] = True if floor_rect.collidelist(collide_rects) >= 0 else False

    def collision(self, axis):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if axis == 'horizontal':
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right

                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left

                else:
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom

                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                    self.direction.y = 0
                        

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.input()
        self.move(dt)
        self.check_contact()