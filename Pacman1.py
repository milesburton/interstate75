import random
import asyncio
import hub75

HEIGHT = 32
WIDTH = 64

h75 = hub75.Hub75(WIDTH, HEIGHT, stb_invert=False)
h75.start()

# Game elements
player = {'x': 1, 'y': 1, 'dx': 0, 'dy': 0}
ghosts = [{'x': 10, 'y': 10, 'dx': 1, 'dy': 0}, {'x': 20, 'y': 20, 'dx': -1, 'dy': 0}]
pellets = [(x, y) for x in range(1, WIDTH-1) for y in range(1, HEIGHT-1) if random.random() < 0.05]
maze = [
    "############################################################",
    "#                                                          #",
    "# ############## #### ############## #### ############## # #",
    "# ############## #### ############## #### ############## # #",
    "#          #            #            #            #      # #",
    "# ######## # ########## # ########## # ########## # ###### #",
    "# ######## # ########## # ########## # ########## # ###### #",
    "#          #            #            #            #      # #",
    "############################################################"
]

# Extend the maze to fit the display height
maze.extend(["#                                                          #"] * (HEIGHT - len(maze)))

def draw_border():
    for x in range(WIDTH):
        h75.set_pixel(x, 0, 255, 255, 255)  # Top border
        h75.set_pixel(x, HEIGHT - 1, 255, 255, 255)  # Bottom border

    for y in range(HEIGHT):
        h75.set_pixel(0, y, 255, 255, 255)  # Left border
        h75.set_pixel(WIDTH - 1, y, 255, 255, 255)  # Right border

def draw_maze():
    for y, row in enumerate(maze):
        for x, char in enumerate(row):
            if char == '#':
                h75.set_pixel(x, y, 0, 0, 255)

def draw_pellets():
    for x, y in pellets:
        h75.set_pixel(x, y, 255, 255, 255)

def draw_player():
    h75.set_pixel(player['x'], player['y'], 255, 255, 0)

def draw_ghosts():
    for ghost in ghosts:
        h75.set_pixel(ghost['x'], ghost['y'], 255, 0, 0)

def move_player():
    new_x = player['x'] + player['dx']
    new_y = player['y'] + player['dy']
    if 0 <= new_x < WIDTH and 0 <= new_y < HEIGHT and maze[new_y][new_x] != '#':
        player['x'], player['y'] = new_x, new_y

def move_ghosts():
    for ghost in ghosts:
        new_x = ghost['x'] + ghost['dx']
        new_y = ghost['y'] + ghost['dy']
        if 0 <= new_x < WIDTH and 0 <= new_y < HEIGHT and maze[new_y][new_x] == '#':
            ghost['dx'], ghost['dy'] = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        else:
            ghost['x'], ghost['y'] = new_x, new_y

def check_collisions():
    global pellets
    if (player['x'], player['y']) in pellets:
        pellets.remove((player['x'], player['y']))
    for ghost in ghosts:
        if ghost['x'] == player['x'] and ghost['y'] == player['y']:
            print("Game Over!")
            exit()

def simulate_player_input():
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    player['dx'], player['dy'] = random.choice(directions)

async def game_loop():
    while True:
        h75.clear()
        draw_border()
        draw_maze()
        draw_pellets()
        draw_player()
        draw_ghosts()
        move_player()
        move_ghosts()
        check_collisions()
        
        # Simulate player input occasionally
        if random.random() < 0.1:
            simulate_player_input()
        
        await asyncio.sleep(0.1)

async def main():
    await game_loop()

if __name__ == "__main__":
    asyncio.run(main())
