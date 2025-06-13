def display_menu():
    """Displays the main menu and returns the user's choice."""
    print("Welcome to the Multi-Game Application!")
    print("Please select a game to play:")
    print("1. Squid Game")
    print("2. XO Game")
    print("3. Snake Game")
    print("4. Sudoku")
    print("5. Exit")

    while True:
        choice = input("Enter your choice (1-5): ")
        if choice in ["1", "2", "3", "4", "5"]:
            return choice
        else:
            print("Invalid choice. Please try again.")

import squid_game
import xo_game
import snake_game
import sudoku_game

def main():
    """Main function to run the multi-game application."""
    while True:
        choice = display_menu()

        if choice == "1":
            squid_game.play_squid_game()
        elif choice == "2":
            xo_game.play_xo_game()
        elif choice == "3":
            snake_game.play_snake_game()
        elif choice == "4":
            sudoku_game.play_sudoku_game()
        elif choice == "5":
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()
