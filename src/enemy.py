# src/enemy.py
import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, images, collision_sprites):
        super().__init__()
        self.images = images
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox_rect = self.rect.copy()
        self.player_hitbox_rect = self.rect.copy()
        self.direction = pygame.Vector2(1, 0)  # Movimiento hacia la derecha
        self.speed = 150
        self.collision_sprites = collision_sprites
        self.gravity = 800
        self.on_ground = False
        self.facing_right = True  # Estado para la dirección del enemigo
        self.animation_index = 0
        self.animation_speed = 0.1

    def apply_gravity(self, dt):
        if not self.on_ground:
            self.direction.y += self.gravity * dt
        else:
            self.direction.y = 0

    def check_ground_collision(self):
        self.on_ground = False
        for sprite in self.collision_sprites:
            if self.hitbox_rect.colliderect(sprite.rect):
                if self.direction.y > 0:  # Falling
                    self.hitbox_rect.bottom = sprite.rect.top
                    self.direction.y = 0
                    self.on_ground = True

    def animate(self, dt):
        self.animation_index += self.animation_speed
        if self.animation_index >= len(self.images):
            self.animation_index = 0
        self.image = self.images[int(self.animation_index)]
        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)

    def update(self, dt):
        # Movimiento en el eje x
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        for sprite in self.collision_sprites:
            if self.hitbox_rect.colliderect(sprite.rect):
                if self.direction.x > 0:  # Moving right
                    self.hitbox_rect.right = sprite.rect.left
                elif self.direction.x < 0:  # Moving left
                    self.hitbox_rect.left = sprite.rect.right
                self.direction.x *= -1  # Cambiar de dirección en el eje x
                self.facing_right = not self.facing_right  # Cambiar el estado de dirección

        # Aplicar gravedad
        self.apply_gravity(dt)

        # Movimiento en el eje y
        self.hitbox_rect.y += self.direction.y * dt
        self.check_ground_collision()

        # Actualizar la posición del rectángulo principal
        self.rect.topleft = self.hitbox_rect.topleft

        # Actualizar la posición del rectángulo de colisión con el jugador
        self.player_hitbox_rect.center = self.hitbox_rect.center

        # Animar el enemigo
        self.animate(dt)

class Enemy3(Enemy):
    def __init__(self, pos, images, collision_sprites):
        super().__init__(pos, images, collision_sprites)
        self.rect.size = (200, 200)
        self.hitbox_rect.size = (180, 200)  # Ajustar el tamaño de la hitbox
        self.player_hitbox_rect.size = (120, 125)  # Ajustar el tamaño de la hitbox de colisión con el jugador
        self.jump_force = -500  # Fuerza del salto, ajusta según sea necesario

    def jump(self):
        if self.on_ground:
            self.direction.y = self.jump_force
            self.on_ground = False

    def apply_gravity(self, dt):
        super().apply_gravity(dt)
        # Variaciones específicas de Enemy3 en la gravedad

    def check_ground_collision(self):
        self.on_ground = False
        for sprite in self.collision_sprites:
            if self.hitbox_rect.colliderect(sprite.rect):
                if self.direction.y > 0:  # Falling
                    self.hitbox_rect.bottom = sprite.rect.top
                    self.direction.y = 0
                    self.on_ground = True
                    self.jump()  # Llamar al método jump cuando toca el suelo

    def animate(self, dt):
        super().animate(dt)
        # Variaciones específicas de Enemy3 en la animación

    def update(self, dt):
        super().update(dt)
        # Variaciones específicas de Enemy3 en la actualización