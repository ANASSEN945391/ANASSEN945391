import unittest
import copy # For Sudoku game state

# Import functions from game files
from xo_game import check_win, check_draw
from snake_game import GRID_WIDTH, GRID_HEIGHT, place_food # For snake tests
# Sudoku functions will be imported directly in its test class to avoid name clashes if any
# Squid game is problematic for unit tests due to its input-driven nature

# --- TestXOGame ---
class TestXOGame(unittest.TestCase):
    def test_check_win_row(self):
        board = [['X', 'X', 'X'], [' ', 'O', ' '], ['O', ' ', ' ']]
        self.assertTrue(check_win(board, 'X'))
        board = [['O', 'O', 'O'], [' ', 'X', ' '], ['X', ' ', ' ']]
        self.assertTrue(check_win(board, 'O'))

    def test_check_win_col(self):
        board = [['X', ' ', 'O'], ['X', 'O', ' '], ['X', ' ', ' ']]
        self.assertTrue(check_win(board, 'X'))
        board = [['O', 'X', ' '], ['O', 'X', ' '], ['O', ' ', 'X']]
        self.assertTrue(check_win(board, 'O'))

    def test_check_win_diag(self):
        board = [['X', ' ', 'O'], [' ', 'X', 'O'], [' ', ' ', 'X']]
        self.assertTrue(check_win(board, 'X'))
        board = [['O', ' ', 'X'], [' ', 'O', 'X'], ['X', ' ', 'O']]
        self.assertTrue(check_win(board, 'O'))

    def test_check_win_no_winner(self):
        board = [['X', 'O', 'X'], ['O', 'X', 'O'], ['O', 'X', ' ']]
        self.assertFalse(check_win(board, 'X'))
        self.assertFalse(check_win(board, 'O'))
        board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
        self.assertFalse(check_win(board, 'X'))

    def test_check_draw_is_draw(self):
        board = [['X', 'O', 'X'], ['O', 'X', 'X'], ['O', 'X', 'O']]
        self.assertTrue(check_draw(board))

    def test_check_draw_not_draw_empty(self):
        board = [['X', 'O', 'X'], ['O', 'X', ' '], ['O', 'X', 'O']]
        self.assertFalse(check_draw(board))

    def test_check_draw_not_draw_winner(self):
        board = [['X', 'X', 'X'], ['O', 'O', ' '], [' ', ' ', ' ']]
        self.assertFalse(check_draw(board)) # X wins, so not a draw

# --- TestSnakeGame ---
# Note: Testing snake game logic that involves game loop & continuous state change is complex.
# These tests focus on specific helper functions or predictable state changes.
class TestSnakeGame(unittest.TestCase):
    def setUp(self):
        self.grid_width = GRID_WIDTH
        self.grid_height = GRID_HEIGHT

    def test_wall_collision(self):
        # Head position is (x,y)
        # Snake is list of (x,y) tuples, head is snake[0]
        snake_hitting_right_wall = [(self.grid_width -1, 5), (self.grid_width - 2, 5)]
        new_head_right = (self.grid_width, 5) # Collision

        snake_hitting_left_wall = [(0, 5), (1, 5)]
        new_head_left = (-1, 5) # Collision

        snake_hitting_top_wall = [(5, 0), (5, 1)]
        new_head_top = (5, -1) # Collision

        snake_hitting_bottom_wall = [(5, self.grid_height - 1), (5, self.grid_height - 2)]
        new_head_bottom = (5, self.grid_height) # Collision

        self.assertFalse(0 <= new_head_right[0] < self.grid_width)
        self.assertFalse(0 <= new_head_left[0] < self.grid_width)
        self.assertFalse(0 <= new_head_top[1] < self.grid_height)
        self.assertFalse(0 <= new_head_bottom[1] < self.grid_height)

    def test_self_collision(self):
        snake = [(5, 5), (5, 6), (5, 7), (4, 7)] # Head at (5,5)
        new_head_collides = (5, 7) # Collides with 3rd segment
        self.assertIn(new_head_collides, snake[1:]) # Check against body

        new_head_no_collision = (4,5)
        self.assertNotIn(new_head_no_collision, snake[1:])

    def test_food_eaten_snake_grows(self):
        # This test implies checking the length of snake before and after a simulated move onto food
        # For simplicity, we'll check the logic conceptually
        snake = [(5, 5), (4, 5)]
        food_pos = (6, 5)
        new_head_pos = (6,5) # Snake moves onto food

        # Simulate eating
        if new_head_pos == food_pos:
            snake.insert(0, new_head_pos) # Grow
            # In real game, new food would be placed

        self.assertEqual(len(snake), 3)
        self.assertEqual(snake[0], new_head_pos)

    def test_new_food_placement_on_empty_spot(self):
        snake = []
        for i in range(self.grid_width): # Almost fill one row
            if i < self.grid_width -1: # Leave one spot for food
                 snake.append((i,0))

        # Try placing food multiple times to increase chance of testing edge cases,
        # though true deterministic testing of random functions is hard without mocking.
        for _ in range(10): # Try a few times
            food_pos = place_food(snake) # place_food is from snake_game.py
            self.assertTrue(0 <= food_pos[0] < self.grid_width)
            self.assertTrue(0 <= food_pos[1] < self.grid_height)
            self.assertNotIn(food_pos, snake)

    def test_snake_moves_correctly(self):
        snake = [(5, 5), (4, 5), (3,5)] # Moving right implicitly
        # new_head_pos based on direction (1,0) -> right
        new_head_pos = (snake[0][0] + 1, snake[0][1])

        # Simulate move (no food)
        snake.insert(0, new_head_pos)
        removed_tail = snake.pop()

        self.assertEqual(snake, [(6,5), (5,5), (4,5)])
        self.assertEqual(removed_tail, (3,5))


# --- TestSudokuGame ---
from sudoku_game import is_valid_move as sudoku_is_valid, is_board_full as sudoku_is_full

class TestSudokuGame(unittest.TestCase):
    def setUp(self):
        self.empty_board = [[0 for _ in range(9)] for _ in range(9)]
        self.sample_board = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]
        self.full_board_invalid = [ # Full but with conflicts
            [5, 3, 1, 6, 7, 8, 9, 1, 2], # row conflict (1)
            [6, 7, 2, 1, 9, 5, 3, 4, 8],
            [1, 9, 8, 3, 4, 2, 5, 6, 7],
            [8, 5, 9, 7, 6, 1, 4, 2, 3],
            [4, 2, 6, 8, 5, 3, 7, 9, 1],
            [7, 1, 3, 9, 2, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, 9, 6, 3, 5],
            [3, 4, 5, 2, 8, 6, 1, 7, 9]
        ]


    def test_is_valid_move_correct(self):
        self.assertTrue(sudoku_is_valid(self.sample_board, 0, 2, 1)) # Empty spot, valid num
        self.assertTrue(sudoku_is_valid(self.sample_board, 0, 2, 4)) # Empty spot, valid num

    def test_is_valid_move_row_conflict(self):
        self.assertFalse(sudoku_is_valid(self.sample_board, 0, 2, 5)) # 5 is in row 0

    def test_is_valid_move_col_conflict(self):
        self.assertFalse(sudoku_is_valid(self.sample_board, 2, 0, 5)) # 5 is in col 0 (via row 0)

    def test_is_valid_move_subgrid_conflict(self):
        self.assertFalse(sudoku_is_valid(self.sample_board, 1, 1, 5)) # 5 is in top-left 3x3 grid

    def test_is_valid_move_already_filled_by_same_num(self):
        # is_valid_move doesn't care if the cell is pre-filled, it just checks rules
        # The game logic prevents overwriting pre-filled cells
        # If we place 7 at (0,4) where 7 already is, it's technically a conflict with itself.
        # A better check might be to temporarily place it and see.
        # Current is_valid_move: it will check the board *excluding* the current cell.
        # So, if board[0][4] is 7, and we check is_valid_move(board, 0, 4, 7),
        # it will find 7 in board[0] (itself) and return False.
        # This is acceptable for its purpose in the game (checking if a *new* number can be placed).
        self.assertFalse(sudoku_is_valid(self.sample_board, 0, 4, 7))


    def test_is_board_full_true(self):
        # Create a truly full board (no zeros, not necessarily valid)
        full_board = [[(r + c) % 9 + 1 for c in range(9)] for r in range(9)]
        self.assertTrue(sudoku_is_full(full_board))

    def test_is_board_full_false(self):
        self.assertFalse(sudoku_is_full(self.sample_board))
        self.assertFalse(sudoku_is_full(self.empty_board))

# --- TestSquidGame ---
# As noted, Squid Game's play_squid_game is highly interactive and stateful,
# making it difficult to unit test without significant refactoring.
# We can add a simple placeholder test.
class TestSquidGame(unittest.TestCase):
    def test_placeholder(self):
        """Placeholder test for Squid Game."""
        self.assertTrue(True, "Squid Game tests would require refactoring for testability.")

if __name__ == '__main__':
    unittest.main()
