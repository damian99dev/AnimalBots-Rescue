import pygame
from src.player import Player

class Game:
    def __init__(self, settings):
        self.settings = settings
        self.screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
        pygame.display.set_caption("Animalbots Recue")
        self.clock = pygame.time.Clock()
        self.player = Player(self)

    def run(self):
        while True:
            self._check_events()
            self._update_screen()
            self.clock.tick(self.settings.fps)

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.player.draw()
        pygame.display.flip()
