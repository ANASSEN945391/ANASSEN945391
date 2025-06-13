def print_board(board):
    """Prints the Tic-Tac-Toe board."""
    print("\n  0 1 2")
    for i, row in enumerate(board):
        print(f"{i} {'|'.join(row)}")
        if i < 2:
            print("  -----")

def check_win(board, player):
    """Checks if the given player has won."""
    # Check rows
    for row in board:
        if all(s == player for s in row):
            return True
    # Check columns
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    # Check diagonals
    if all(board[i][i] == player for i in range(3)):
        return True
    if all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def check_draw(board):
    """Checks if the game is a draw."""
    for row in board:
        if ' ' in row:
            return False  # There's an empty space, so not a draw yet
    return not check_win(board, 'X') and not check_win(board, 'O') # No winner and board is full

def get_player_move(player, board):
    """Gets and validates the player's move."""
    while True:
        try:
            print_board(board)
            print(f"Player {player}, it's your turn.")
            row_str = input("Enter row (0, 1, or 2): ")
            col_str = input("Enter column (0, 1, or 2): ")

            if not row_str or not col_str: # Handle empty input
                print("Input cannot be empty. Please try again.")
                continue

            row = int(row_str)
            col = int(col_str)

            if row < 0 or row > 2 or col < 0 or col > 2:
                print("Invalid input. Row and column must be between 0 and 2.")
            elif board[row][col] != ' ':
                print("That spot is already taken! Try again.")
            else:
                return row, col
        except ValueError:
            print("Invalid input. Please enter numbers for row and column.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}. Please try again.")


def play_xo_game():
    """Plays the Tic-Tac-Toe game."""
    board = [[' ' for _ in range(3)] for _ in range(3)]
    current_player = 'X'
    game_over = False
    moves = 0

    print("Welcome to Tic-Tac-Toe (XO Game)!")

    while not game_over and moves < 9:
        row, col = get_player_move(current_player, board)
        board[row][col] = current_player
        moves += 1

        if check_win(board, current_player):
            print_board(board)
            print(f"\nCongratulations, Player {current_player}! You WIN!")
            game_over = True
        elif moves == 9: # Board is full
            if check_draw(board): # ensure no one won on the last move
                 print_board(board)
                 print("\nIt's a DRAW!")
                 game_over = True
            # else: last player won, handled by check_win

        if not game_over:
            current_player = 'O' if current_player == 'X' else 'X'

    if not game_over: # Should be caught by moves < 9, but as a fallback
        print_board(board)
        if check_draw(board):
            print("\nIt's a DRAW!")
        else:
            # This state implies a logic error if reached.
            print("\nGame over, but no winner or draw determined. (Error)")


if __name__ == '__main__':
    play_xo_game()
