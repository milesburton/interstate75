import random
import asyncio
import hub75
import sys

# Constants
PANEL_WIDTH = 64
PANEL_HEIGHT = 32
PADDLE_WIDTH = 2
PADDLE_HEIGHT = 8
BALL_SIZE = 2
GAME_SPEED = 0.05
PADDLE_SPEED = 0.8

class GameState:
    def __init__(self):
        self.paddle1_y = (PANEL_HEIGHT - PADDLE_HEIGHT) // 2
        self.paddle2_y = (PANEL_HEIGHT - PADDLE_HEIGHT) // 2
        self.paddle1_x = 2
        self.paddle2_x = PANEL_WIDTH - PADDLE_WIDTH - 2
        self.reset_ball()
    
    def reset_ball(self):
        self.ball_x = PANEL_WIDTH // 2
        self.ball_y = PANEL_HEIGHT // 2
        self.ball_dx = 1.5 if random.random() > 0.5 else -1.5
        self.ball_dy = random.uniform(-0.8, 0.8)

def update_paddle_positions(game_state):
    # (same as before)
    target_y = game_state.ball_y - (PADDLE_HEIGHT // 2)
    if game_state.paddle1_y < target_y:
        game_state.paddle1_y = min(game_state.paddle1_y + PADDLE_SPEED,
                                   PANEL_HEIGHT - PADDLE_HEIGHT)
    elif game_state.paddle1_y > target_y:
        game_state.paddle1_y = max(game_state.paddle1_y - PADDLE_SPEED, 0)

    if game_state.paddle2_y < target_y:
        game_state.paddle2_y = min(game_state.paddle2_y + PADDLE_SPEED,
                                   PANEL_HEIGHT - PADDLE_HEIGHT)
    elif game_state.paddle2_y > target_y:
        game_state.paddle2_y = max(game_state.paddle2_y - PADDLE_SPEED, 0)

def draw_paddle(panel, x, y):
    y = int(y)
    for i in range(PADDLE_HEIGHT):
        for j in range(PADDLE_WIDTH):
            panel.set_pixel(x + j, y + i, 255, 255, 255)

def draw_ball(panel, x, y):
    x = int(x)
    y = int(y)
    for i in range(BALL_SIZE):
        for j in range(BALL_SIZE):
            panel.set_pixel(x + i, y + j, 255, 255, 0)

def check_collisions(game_state):
    # Wall collisions
    if game_state.ball_y <= 0:
        game_state.ball_y = 0
        game_state.ball_dy *= -1
    elif game_state.ball_y >= PANEL_HEIGHT - BALL_SIZE:
        game_state.ball_y = PANEL_HEIGHT - BALL_SIZE
        game_state.ball_dy *= -1

    # Ball bounding box
    ball_left   = game_state.ball_x
    ball_right  = game_state.ball_x + BALL_SIZE
    ball_top    = game_state.ball_y
    ball_bottom = game_state.ball_y + BALL_SIZE

    # Left paddle bounding box
    paddle1_left   = game_state.paddle1_x
    paddle1_right  = game_state.paddle1_x + PADDLE_WIDTH
    paddle1_top    = game_state.paddle1_y
    paddle1_bottom = game_state.paddle1_y + PADDLE_HEIGHT

    # Collision check with left paddle
    if (ball_right >= paddle1_left and
        ball_left <= paddle1_right and
        ball_bottom >= paddle1_top and
        ball_top <= paddle1_bottom):
        game_state.ball_dx = abs(game_state.ball_dx)
        game_state.ball_dy += random.uniform(-0.2, 0.2)

    # Right paddle bounding box
    paddle2_left   = game_state.paddle2_x
    paddle2_right  = game_state.paddle2_x + PADDLE_WIDTH
    paddle2_top    = game_state.paddle2_y
    paddle2_bottom = game_state.paddle2_y + PADDLE_HEIGHT

    # Collision check with right paddle
    if (ball_right >= paddle2_left and
        ball_left <= paddle2_right and
        ball_bottom >= paddle2_top and
        ball_top <= paddle2_bottom):
        game_state.ball_dx = -abs(game_state.ball_dx)
        game_state.ball_dy += random.uniform(-0.2, 0.2)

    # Reset ball if it goes out of left/right bounds
    if game_state.ball_x <= 0 or game_state.ball_x >= PANEL_WIDTH - BALL_SIZE:
        game_state.reset_ball()

async def game_loop(panel):
    """Main game loop with an existing panel instance."""
    try:
        game_state = GameState()

        while True:
            update_paddle_positions(game_state)

            # Update ball position
            game_state.ball_x += game_state.ball_dx
            game_state.ball_y += game_state.ball_dy

            # Check collisions
            check_collisions(game_state)

            # Clear display
            panel.clear()

            # Draw objects
            draw_paddle(panel, game_state.paddle1_x, game_state.paddle1_y)
            draw_paddle(panel, game_state.paddle2_x, game_state.paddle2_y)
            draw_ball(panel, game_state.ball_x, game_state.ball_y)

            # Update display
            panel.update(panel)

            await asyncio.sleep(GAME_SPEED)

    except Exception as e:
        print(f"Error in game loop: {str(e)}")
        sys.print_exception(e)  # prints stack trace + line number
        raise

# Create the panel instance here, if your library supports these arguments.
try:
    # Depending on your library, the constructor may differ:
    # panel = hub75.Hub75()       # some libraries need no args
    # panel = hub75.Hub75((64,32))  # some want a tuple
    # panel = hub75.Hub75(rows=32, chain_length=2) # or named args
    panel = hub75.Hub75(PANEL_WIDTH, PANEL_HEIGHT, stb_invert=False)

    panel.start()
    print("Starting Pong animation...")
    asyncio.run(game_loop(panel))

except KeyboardInterrupt:
    print("Animation ended by user")

except Exception as e:
    print(f"Animation crashed: {str(e)}")

finally:
    # Clean up *without* re-initializing the panel
    try:
        panel.clear()
        panel.update(panel)
    except:
        pass
