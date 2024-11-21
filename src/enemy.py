# src/enemy.py
import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, images, collision_sprites):
        super().__init__()
        self.images = images
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox_rect = self.rect.inflate(-10, -3)  # Rectángulo de colisión con las paredes
        self.player_hitbox_rect = self.rect.inflate(-20, -80)  # Rectángulo de colisión con el jugador
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