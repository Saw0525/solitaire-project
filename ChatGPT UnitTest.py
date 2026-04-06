import unittest
from game_board import GameBoard
from solitaire_gui import SolitaireGUI
import tkinter as tk


class TestGameBoard(unittest.TestCase):

    def setUp(self):
        """Runs before each test."""
        self.game = GameBoard()
        self.game.new_game("English", 7)

    def test_new_game_creates_board(self):
        """Test that a new game initializes a board."""
        self.assertEqual(len(self.game.board), 7)
        self.assertEqual(len(self.game.board[0]), 7)

    def test_center_is_empty(self):
        """English board should start with center empty."""
        self.assertEqual(self.game.board[3][3], 0)

    def test_get_cell_valid(self):
        """Test getting a valid cell value."""
        value = self.game.get_cell(2,2)
        self.assertIn(value, [1,0,-1])

    def test_get_cell_outside_board(self):
        """Out-of-range coordinates should return -1."""
        value = self.game.get_cell(10,10)
        self.assertEqual(value, -1)

    def test_valid_move(self):
        """Test a legal move."""
        # create a simple move scenario
        self.game.board[3][3] = 0
        self.game.board[3][2] = 1
        self.game.board[3][1] = 1

        self.assertTrue(self.game.is_valid_move(3,1,3,3))

    def test_invalid_move(self):
        """Test illegal move detection."""
        self.assertFalse(self.game.is_valid_move(0,0,0,2))

    def test_make_move(self):
        """Test performing a valid move."""
        self.game.board[3][3] = 0
        self.game.board[3][2] = 1
        self.game.board[3][1] = 1

        moved = self.game.make_move(3,1,3,3)

        self.assertTrue(moved)
        self.assertEqual(self.game.board[3][1], 0)
        self.assertEqual(self.game.board[3][2], 0)
        self.assertEqual(self.game.board[3][3], 1)

    def test_game_not_over_initially(self):
        """Game should not be over at start."""
        self.assertFalse(self.game.game_over())


class TestSolitaireGUI(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.app = SolitaireGUI(self.root)

    def test_board_type_default(self):
        self.assertEqual(self.app.board_type.get(), "English")

    def test_new_game_resets_selection(self):
        self.app.selected = (3,3)
        self.app.start_new_game()
        self.assertIsNone(self.app.selected)

    def test_auto_move(self):
        self.app.game_mode.set("Auto")
        self.app.start_new_game()

        moved = self.app.game.auto_move()
        self.assertIn(moved, [True, False])

    def test_randomize(self):
        self.app.start_new_game()

        self.app.game.randomize()

        board = self.app.game.board.board
        values = [cell for row in board for cell in row if cell != -1]

        self.assertTrue(all(v in [0,1] for v in values))

    def tearDown(self):
        self.root.destroy()

if __name__ == "__main__":
    unittest.main()