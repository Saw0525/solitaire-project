import unittest
from game_board import GameBoard
from solitaire_gui import SolitaireGUI
import tkinter as tk


class TestGameBoard(unittest.TestCase):

    def setUp(self):
        """Runs before each test."""
        self.game = GameBoard()
        self.game.new_game("English")

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
        """Create GUI instance."""
        self.root = tk.Tk()
        self.app = SolitaireGUI(self.root)

    def test_board_type_default(self):
        """Default board should be English."""
        self.assertEqual(self.app.board_type.get(), "English")

    def test_new_game_resets_selection(self):
        """Starting new game should reset selected peg."""
        self.app.selected = (3,3)
        self.app.start_new_game()
        self.assertIsNone(self.app.selected)

    def tearDown(self):
        """Destroy GUI after tests."""
        self.root.destroy()


if __name__ == "__main__":
    unittest.main()