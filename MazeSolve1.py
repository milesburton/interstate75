import random
import asyncio
import hub75
import time
from collections import deque

HEIGHT = 32
WIDTH = 64
MAX_PIXELS = 64

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

async def bfs_solve_animated(maze, start, goal):
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

                # Animate the exploration
                h75.set_pixel(next_cell[0], next_cell[1], 0, 0, 255)  # Blue color for exploration
                await asyncio.sleep(0.01)  # Adjust the speed of the exploration
                
    if goal not in came_from:
        return []  # Return an empty path if no path is found

    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path

async def display_maze_and_solve(maze, path):
    height = len(maze)
    width = len(maze[0])
    
    while True:
        h75.clear()
        for y in range(height):
            for x in range(width):
                if maze[y][x] == 1:
                    h75.set_pixel(x, y, 255, 255, 255)  # White color for walls
                else:
                    h75.set_pixel(x, y, 0, 0, 0)  # Black color for paths

        # Display the player solving the maze
        for (x, y) in path:
            h75.set_pixel(x, y, 255, 255, 0)  # Yellow color for player
            await asyncio.sleep(0.1)  # Adjust the speed of the player

        await asyncio.sleep(1)  # Display the solved maze for a while

async def main():
    width, height = 64, 32
    maze = generate_maze(width, height)
    start = (1, 1)
    
    # Ensure the goal position is within bounds and on a path
    goal = (width - 2, height - 2)
    while goal[0] > 0 and goal[1] > 0 and maze[goal[1]][goal[0]] == 1:
        goal = (goal[0] - 2, goal[1] - 2)
    
    print(f"Start: {start}")
    print(f"Goal: {goal}")
    
    path = await bfs_solve_animated(maze, start, goal)
    if not path:
        print("No path found!")
        return
    print("Path found!")
    await display_maze_and_solve(maze, path)

if __name__ == "__main__":
    asyncio.run(main())