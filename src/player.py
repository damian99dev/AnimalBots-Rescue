from settings import *
import os

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprite):
        super().__init__(groups)
        # Ruta base
        base_path = os.path.dirname(__file__)  # Directorio donde está player.py
        img_folder = os.path.join(base_path, '..', 'graphics', 'Protagonist')
        
        # Cargar las imágenes de la animación
        self.images_right = [
            pygame.image.load(os.path.join(img_folder, 'mona china 1.png')).convert_alpha(),
            pygame.image.load(os.path.join(img_folder, 'mona china 2.png')).convert_alpha()
        ]
        self.images_jump = [
            pygame.image.load(os.path.join(img_folder, 'salto.png')).convert_alpha()
        ]
        # Crear las imágenes invertidas para la dirección izquierda
        self.images_left = [pygame.transform.flip(image, True, False) for image in self.images_right]
        self.images_jump_left = [pygame.transform.flip(image, True, False) for image in self.images_jump]

        # Parámetros de animación
        self.index = 0
        self.image = self.images_right[self.index]
        self.animation_speed = 0.3
        self.flip = False
        
        # Rectángulos
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox_rect = self.rect.inflate(-10, -3)
        self.old_rect = self.hitbox_rect.copy()

        # Movimiento del personaje
        self.direction = pygame.Vector2(0, 0)
        self.speed = 200
        self.gravity = 800
        self.jump = False
        self.jump_dist = 300

        # Creamos las colisiones
        self.collision_sprites = collision_sprite
        self.on_surface = {'Suelo': False, 'left': False, 'right': False}

    def animate(self, dt):
        # Si está en el aire, mantener la imagen estática
        if not self.on_surface['Suelo']:  # Verifica si el personaje está en el aire
            self.index += self.animation_speed
            if self.index >= len(self.images_jump):
                self.index = 0
            if self.flip:
                self.image = self.images_jump_left[int(self.index)]
            else:
                self.image = self.images_jump[int(self.index)]
        else:
            # Si el personaje está en el suelo y se mueve, animar
            if self.direction.x != 0:
                self.index += self.animation_speed
                if self.index >= len(self.images_right):
                    self.index = 0
                
                # Seleccionar la imagen correcta según la dirección
                if self.flip:
                    self.image = self.images_left[int(self.index)]
                else:
                    self.image = self.images_right[int(self.index)]
            else:
                # Si no se mueve, mostrar la primera imagen de la animación
                self.index = 0
                if self.flip:
                    self.image = self.images_left[self.index]  # Imagen estática mirando a la izquierda
                else:
                    self.image = self.images_right[self.index]  # Imagen estática mirando a la derecha

    def check_contact(self):
        floor_rect = pygame.Rect(self.hitbox_rect.bottomleft, (self.hitbox_rect.width, 2))
        collide_rects = [sprite.rect for sprite in self.collision_sprites]

        self.on_surface['Suelo'] = True if floor_rect.collidelist(collide_rects) >= 0 else False

    def input(self):
        keys = pygame.key.get_pressed()
        input_vector = pygame.Vector2(0, 0)
        
        if keys[pygame.K_RIGHT]:
            input_vector.x += 1
            self.flip = False  # Dirección hacia la derecha
        if keys[pygame.K_LEFT]:
            input_vector.x -= 1
            self.flip = True  # Dirección hacia la izquierda
        
        self.direction.x = input_vector.normalize().x if input_vector else input_vector.x
        
        if keys[pygame.K_SPACE]:
            self.jump = True
            
    def move(self, dt):
        # Movimiento horizontal
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')

        # Movimiento vertical
        self.direction.y += self.gravity / 2 * dt
        self.hitbox_rect.y += self.direction.y * dt
        self.direction.y += self.gravity / 2 * dt
        self.collision('vertical')

        if self.jump:
            if self.on_surface['Suelo']:
                self.direction.y = -self.jump_dist  # El jugador salta
            self.jump = False

        self.rect.center = self.hitbox_rect.center

    def collision(self, axis):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if axis == 'horizontal':
                    if self.hitbox_rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.hitbox_rect.left = sprite.rect.right

                    if self.hitbox_rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.hitbox_rect.right = sprite.rect.left
                    

                else:
                    if self.hitbox_rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.hitbox_rect.top = sprite.rect.bottom

                    if self.hitbox_rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.hitbox_rect.bottom = sprite.rect.top
                    self.direction.y = 0

    def update(self, dt):
        self.old_rect = self.hitbox_rect.copy()
        self.input()
        self.move(dt)
        self.animate(dt)  # Llamada para animar el personaje
        self.check_contact()
