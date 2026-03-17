import unittest
from game_board import GameBoard

class TestGameBoard(unittest.TestCase):

    def setUp(self):
        self.game = GameBoard()
        self.game.new_game("English")

    def test_valid_move(self):
        # valid move example
        result = self.game.make_move(3,1,3,3)
        self.assertTrue(result)

    def test_invalid_move(self):
        result = self.game.make_move(0,0,0,2)
        self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()