import random
import time

def play_squid_game():
    """Plays the Red Light, Green Light game."""
    target_distance = 10
    current_position = 0
    rounds_played = 0

    print("Welcome to Red Light, Green Light!")
    print(f"You need to reach {target_distance} steps to win.")
    print("You can take 1, 2, or 3 steps during a Green Light.")
    print("Do NOT move during a Red Light!")

    while current_position < target_distance:
        rounds_played += 1
        print(f"\n--- Round {rounds_played} ---")
        print(f"Your current position: {current_position} steps.")

        # Determine light status (making Red Light a bit less frequent)
        light_is_green = random.choices([True, False], weights=[0.6, 0.4], k=1)[0]

        if light_is_green:
            print("\nGREEN LIGHT!")
            time.sleep(1) # For dramatic effect
            while True:
                try:
                    steps_to_take_str = input("How many steps do you want to take (1, 2, or 3)? ")
                    steps_to_take = int(steps_to_take_str)
                    if steps_to_take in [1, 2, 3]:
                        break
                    else:
                        print("Invalid input. Please enter 1, 2, or 3.")
                except ValueError:
                    print("Invalid input. Please enter a number.")

            current_position += steps_to_take
            print(f"You moved {steps_to_take} steps.")

            if current_position >= target_distance:
                print(f"\nCongratulations! You've reached {current_position} steps and crossed the finish line!")
                print("YOU WIN!")
                return
        else:
            print("\nRED LIGHT!")
            time.sleep(1) # For dramatic effect
            while True:
                choice = input("Do you want to move (yes/no)? ").strip().lower()
                if choice in ["yes", "y", "no", "n"]:
                    break
                else:
                    print("Invalid input. Please enter 'yes' or 'no'.")

            if choice in ["yes", "y"]:
                print("\nOh no! You moved during a Red Light!")
                print("YOU LOSE!")
                return
            else:
                print("You stayed still. Safe for this round!")

        time.sleep(1) # Pause before next round

    # This part should ideally not be reached if win condition is met above,
    # but as a fallback:
    if current_position >= target_distance:
        print(f"\nCongratulations! You've reached {current_position} steps and crossed the finish line!")
        print("YOU WIN!")
    else:
        # This case would only happen if the loop exited unexpectedly.
        print("\nGame Over.")


if __name__ == '__main__':
    play_squid_game()
