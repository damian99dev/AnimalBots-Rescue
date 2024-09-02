import unittest
from src.player import Player
from src.settings import Settings
from src.game import Game

class TestPlayer(unittest.TestCase):
    def setUp(self):
        settings = Settings()
        self.game = Game(settings)
        self.player = Player(self.game)

    def test_player_position(self):
        self.assertEqual(self.player.rect.center, self.game.screen.get_rect().center)

if __name__ == '__main__':
    unittest.main()
