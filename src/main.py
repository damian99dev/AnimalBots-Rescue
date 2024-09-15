from settings import * #importo los ajustes de settings
from level import Level
from pytmx.util_pygame import load_pygame

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface =  pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption('AnimalBot Rescue') #Le ponemos nombre a la ventana
        self.clock = pygame.time.Clock()

        self.tmx_maps = {0: load_pygame('C:/Users/GAMER/Proyecto Integrador #3/data/tmx/prueba.tmx')}
        self.current_stage = Level(self.tmx_maps[0])

    def run(self):
        while True:
            dt = self.clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.current_stage.run(dt)
            pygame.display.update()

if __name__== '__main__':
    game = Game()
    game.run()