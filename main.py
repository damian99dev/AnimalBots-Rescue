import pygame
from src.settings import Settings
from src.game import Game

def main():
    pygame.init()
    settings = Settings()
    game = Game(settings)
    game.run()
    

if __name__ == "__main__":
    main()

print("Hello Developers")
