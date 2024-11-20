# src/enemy.py
import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, image, collision_sprites):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox_rect = self.rect.inflate(-10, -3)
        self.direction = pygame.Vector2(1, 0)  # Movimiento hacia la derecha
        self.speed = 150
        self.collision_sprites = collision_sprites

    def update(self, dt):
        # Movimiento en el eje x
        self.rect.x += self.direction.x * self.speed * dt
        if pygame.sprite.spritecollideany(self, self.collision_sprites):
            self.rect.x -= self.direction.x * self.speed * dt  # Revertir movimiento
            self.direction.x *= -1  # Cambiar de dirección en el eje x

        # Movimiento en el eje y
        self.rect.y += self.direction.y * self.speed * dt
        if pygame.sprite.spritecollideany(self, self.collision_sprites):
            self.rect.y -= self.direction.y * self.speed * dt  # Revertir movimiento
            self.direction.y *= -1  # Cambiar de dirección en el eje y