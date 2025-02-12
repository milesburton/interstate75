import random
import asyncio
import hub75

HEIGHT = 32
WIDTH = 64
h75 = hub75.Hub75(WIDTH, HEIGHT, stb_invert=False)
h75.start()

# Maze generation using iterative depth-first search
def generate_maze(width, height):
    maze = [[1] * width for _ in range(height)]
    
    def carve_passages_from(cx, cy):
        stack = [(cx, cy)]
        while stack:
            (x, y) = stack[-1]
            maze[y][x] = 0  # Mark the current cell as part of the maze
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            
            carved = False
            while directions:
                # Select a random direction
                idx = random.randrange(len(directions))
                dx, dy = directions.pop(idx)
                
                nx, ny = x + dx * 2, y + dy * 2
                if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == 1:
                    maze[ny][nx] = 0
                    maze[y + dy][x + dx] = 0
                    stack.append((nx, ny))
                    carved = True
                    break
            
            if not carved:
                stack.pop()  # Backtrack if no direction is possible

    maze[1][1] = 0
    carve_passages_from(1, 1)
    return maze

def bfs_solve(maze, start, goal):
    height = len(maze)
    width = len(maze[0])
    queue = [start]
    came_from = {start: None}
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    while queue:
        current = queue.pop(0)
        if current == goal:
            break
        for dx, dy in directions:
            next_cell = (current[0] + dx, current[1] + dy)
            if 0 <= next_cell[0] < width and 0 <= next_cell[1] < height and maze[next_cell[1]][next_cell[0]] == 0 and next_cell not in came_from:
                queue.append(next_cell)
                came_from[next_cell] = current
                
    if goal not in came_from:
        return []  # Return an empty path if no path is found

    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path

async def display_maze(maze, color):
    height = len(maze)
    width = len(maze[0])
    h75.clear()
    for y in range(height):
        for x in range(width):
            if maze[y][x] == 1:
                h75.set_pixel(x, y, color[0], color[1], color[2])  # Color for walls
            else:
                h75.set_pixel(x, y, 0, 0, 0)  # Black color for paths

async def display_maze_and_solve(maze, path, start, goal):
    height = len(maze)
    width = len(maze[0])
    
    if not path:
        # Display "FAIL" in red if no path is found
        await display_maze(maze, (100, 0, 0))
        fail_text = "FAIL"
        fail_start_x = (width - len(fail_text) * 6) // 2  # Center the text
        fail_start_y = height // 2 - 3
        for i, char in enumerate(fail_text):
            display_char(fail_start_x + i * 6, fail_start_y, char, (100, 0, 0))
        await asyncio.sleep(5)
        return

    # Keep the maze visible
    for y in range(height):
        for x in range(width):
            if maze[y][x] == 1:
                h75.set_pixel(x, y, 100, 100, 100)  # White color for walls
            else:
                h75.set_pixel(x, y, 0, 0, 0)  # Black color for paths

    # Highlight the start and end points
    h75.set_pixel(start[0], start[1], 100, 0, 0)  # Red color for start
    h75.set_pixel(goal[0], goal[1], 0, 100, 0)  # Green color for goal

    # Draw green box around the end position
    draw_box(goal[0], goal[1], (0, 100, 0))

    # Display the player solving the maze once
    for (x, y) in path:
        h75.set_pixel(x, y, 100, 100, 0)  # Yellow color for player
        await asyncio.sleep(0.1)  # Adjust the speed of the player

    # Flash the path 5 times
    for _ in range(5):
        await asyncio.sleep(0.5)
        for (x, y) in path:
            h75.set_pixel(x, y, 0, 0, 0)  # Black color to hide the path
        await asyncio.sleep(0.5)
        for (x, y) in path:
            h75.set_pixel(x, y, 100, 100, 0)  # Yellow color to show the path

    await asyncio.sleep(5)  # Display the solved maze for a while before restarting

def draw_box(x, y, color):
    box_coords = [
        (x-1, y-1), (x, y-1), (x+1, y-1),
        (x-1, y), (x+1, y),
        (x-1, y+1), (x, y+1), (x+1, y+1)
    ]
    for (bx, by) in box_coords:
        if 0 <= bx < WIDTH and 0 <= by < HEIGHT:  # Ensure the box coordinates are within bounds
            h75.set_pixel(bx, by, color[0], color[1], color[2])

def display_char(x, y, char, color):
    font = {
        'F': [
            0b11111,
            0b10000,
            0b10000,
            0b11110,
            0b10000,
            0b10000,
            0b10000,
        ],
        'A': [
            0b01110,
            0b10001,
            0b10001,
            0b11111,
            0b10001,
            0b10001,
            0b10001,
        ],
        'I': [
            0b11111,
            0b00100,
            0b00100,
            0b00100,
            0b00100,
            0b00100,
            0b11111,
        ],
        'L': [
            0b10000,
            0b10000,
            0b10000,
            0b10000,
            0b10000,
            0b10000,
            0b11111,
        ],
    }
    pattern = font.get(char.upper())
    if pattern:
        for row, bits in enumerate(pattern):
            for col in range(5):
                if bits & (1 << (4 - col)):
                    h75.set_pixel(x + col, y + row, *color)

def find_random_path_position(maze):
    height = len(maze)
    width = len(maze[0])
    while True:
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        if maze[y][x] == 0:
            return (x, y)

async def game_cycle():
    width, height = 64, 32
    while True:
        maze = generate_maze(width, height)
        
        # Find random start and goal positions
        start = find_random_path_position(maze)
        goal = find_random_path_position(maze)
        while start == goal:
            goal = find_random_path_position(maze)
        
        print(f"Start: {start}")
        print(f"Goal: {goal}")
        
        path = bfs_solve(maze, start, goal)
        if not path:
            print("No path found!")
        else:
            print("Path found!")
        await display_maze_and_solve(maze, path, start, goal)
        await asyncio.sleep(5)  # Wait for 5 seconds before restarting
        h75.clear()  # Clear the display before restarting

async def main():
    await game_cycle()

if __name__ == "__main__":
    asyncio.run(main())
