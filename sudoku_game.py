import copy

def display_board(board):
    """Prints the Sudoku board with separators."""
    print("\n    0 1 2   3 4 5   6 7 8")
    print("  +-------+-------+-------+")
    for i, row in enumerate(board):
        if i % 3 == 0 and i != 0:
            print("  +-------+-------+-------+")
        line = f"{i} | "
        for j, num in enumerate(row):
            if j % 3 == 0 and j != 0:
                line += "| "
            line += str(num) if num != 0 else "."
            line += " "
        line += "|"
        print(line)
    print("  +-------+-------+-------+")

def is_valid_move(board, row, col, num):
    """Checks if placing num at (row, col) is valid."""
    # Check row
    if num in board[row]:
        return False
    # Check column
    if num in [board[r][col] for r in range(9)]:
        return False
    # Check 3x3 subgrid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            if board[r][c] == num:
                return False
    return True

def is_board_full(board):
    """Checks if all cells are filled (no zeros)."""
    for row in board:
        if 0 in row:
            return False
    return True

def get_player_input(initial_board):
    """Gets and validates player input for row, col, and number."""
    while True:
        try:
            row_str = input("Enter row (0-8), or 'q' to quit: ")
            if row_str.lower() == 'q': return "quit", -1, -1
            col_str = input("Enter column (0-8): ")
            num_str = input("Enter number (1-9): ")

            if not all([row_str, col_str, num_str]):
                print("Input cannot be empty. Please try again.")
                continue

            row, col, num = int(row_str), int(col_str), int(num_str)

            if not (0 <= row <= 8 and 0 <= col <= 8 and 1 <= num <= 9):
                print("Invalid input. Row/Col must be 0-8, Number must be 1-9.")
            elif initial_board[row][col] != 0:
                print("This cell is part of the initial puzzle and cannot be changed.")
            else:
                return row, col, num
        except ValueError:
            print("Invalid input. Please enter numbers for row, column, and number.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

def play_sudoku_game():
    """Plays the Sudoku game."""
    # 0 represents an empty cell
    initial_puzzle = [
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
    # Make a deep copy for the game board, so initial_puzzle remains unchanged
    game_board = copy.deepcopy(initial_puzzle)

    print("Welcome to Sudoku!")
    print("Fill in the board. Use '.' for empty cells. Enter 'q' for row to quit.")

    while True:
        display_board(game_board)

        # Check for win condition before asking for input
        # (in case the loaded puzzle is already solved, or becomes solved)
        if is_board_full(game_board):
            # Final validation (optional, as is_valid_move should prevent incorrect entries)
            # For robustness, one could iterate and check all cells.
            # For this implementation, reaching full board with valid moves means a win.
            print("\nCongratulations! You've solved the Sudoku puzzle!")
            break

        user_input = get_player_input(initial_puzzle)
        if user_input[0] == "quit":
            print("\nThanks for playing Sudoku!")
            break

        row, col, num = user_input

        if is_valid_move(game_board, row, col, num):
            game_board[row][col] = num
        else:
            print(f"Invalid move: Placing {num} at ({row},{col}) violates Sudoku rules. Try again.")
            # Optionally, allow player to undo or clear the cell if they made a mistake
            # For now, the cell remains as it was or empty if it was empty.

if __name__ == '__main__':
    play_sudoku_game()
