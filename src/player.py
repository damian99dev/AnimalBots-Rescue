
import pygame

class Player:
    def __init__(self, game):
        self.screen = game.screen
        self.image = pygame.image.load("assets\images\player\Sonia_ 1.png")
        self.rect = self.image.get_rect()
        self.rect.center = game.screen.get_rect().center

    def draw(self):
        self.screen.blit(self.image, self.rect)
