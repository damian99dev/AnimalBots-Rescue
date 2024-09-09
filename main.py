import pygame
from src.settings import Settings
from src.game import Game

def main():
    pygame.init()
    settings = Settings()
    game = Game(settings)
    game.run()
    pygame.quit()

if __name__ == "__main__":
    main()
print ("hola geis")


