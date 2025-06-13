import random
import time

GRID_WIDTH = 20
GRID_HEIGHT = 10
INITIAL_SNAKE_LENGTH = 3
GAME_SPEED = 0.5 # seconds per step

def display_grid(snake, food):
    """Displays the game grid, snake, and food."""
    print("\n" + "#" * (GRID_WIDTH + 2))
    for y in range(GRID_HEIGHT):
        line = "#"
        for x in range(GRID_WIDTH):
            if (x, y) == food:
                line += "F"
            elif (x, y) in snake:
                if (x,y) == snake[0]: # Snake head
                    line += "H"
                else:
                    line += "S"
            else:
                line += " "
        line += "#"
        print(line)
    print("#" * (GRID_WIDTH + 2))

def get_player_direction(current_direction_vector):
    """Gets player input for direction, preventing immediate reversal."""
    # (dx, dy) where dx is change in x, dy is change in y
    # W = (0, -1), A = (-1, 0), S = (0, 1), D = (1, 0)
    valid_inputs = {
        'w': (0, -1), 'a': (-1, 0), 's': (0, 1), 'd': (1, 0)
    }
    opposites = {
        (0, -1): (0, 1), (0, 1): (0, -1),
        (-1, 0): (1, 0), (1, 0): (-1, 0)
    }

    while True:
        direction_input = input("Enter direction (w=up, a=left, s=down, d=right): ").lower()
        if direction_input in valid_inputs:
            new_direction_vector = valid_inputs[direction_input]
            if current_direction_vector and new_direction_vector == opposites[current_direction_vector]:
                print("You cannot immediately reverse direction!")
            else:
                return new_direction_vector
        else:
            print("Invalid input. Please use w, a, s, or d.")

def place_food(snake):
    """Places food randomly on an empty spot."""
    while True:
        food_pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if food_pos not in snake:
            return food_pos

def play_snake_game():
    """Plays the Snake game."""
    # Initial snake position (head first)
    snake = []
    start_x = GRID_WIDTH // 2
    start_y = GRID_HEIGHT // 2
    for i in range(INITIAL_SNAKE_LENGTH):
        snake.append((start_x - i, start_y)) # Snake starts horizontally, facing right implicitly

    food = place_food(snake)

    # Initial direction: right (1,0). (dx, dy)
    # dx: change in x, dy: change in y. (0,0) is top-left.
    # 'w': (0, -1) up
    # 's': (0, 1)  down
    # 'a': (-1, 0) left
    # 'd': (1, 0)  right
    direction_vector = (1, 0) # (dx, dy) - initially moving right
    score = 0

    print("Welcome to Snake!")
    print("Use w, a, s, d to control the snake. Try to eat the food (F)!")

    while True:
        display_grid(snake, food)
        print(f"Score: {score}")

        # Get player input (will block here due to input())
        new_direction_vector = get_player_direction(direction_vector)
        direction_vector = new_direction_vector

        # Calculate new head position
        head_x, head_y = snake[0]
        new_head_x = head_x + direction_vector[0]
        new_head_y = head_y + direction_vector[1]
        new_head_pos = (new_head_x, new_head_y)

        # Check for wall collision
        if not (0 <= new_head_x < GRID_WIDTH and 0 <= new_head_y < GRID_HEIGHT):
            print("\nGame Over! You hit the wall.")
            print(f"Final Score: {score}")
            return

        # Check for self-collision
        if new_head_pos in snake: # Check if new head collides with any part of the existing snake
            print("\nGame Over! You ran into yourself.")
            print(f"Final Score: {score}")
            return

        snake.insert(0, new_head_pos) # Add new head

        # Check if food eaten
        if new_head_pos == food:
            score += 1
            print("Yum! Food eaten.")
            food = place_food(snake) # Place new food
        else:
            snake.pop() # Remove tail if no food eaten

        time.sleep(GAME_SPEED)

if __name__ == '__main__':
    play_snake_game()
