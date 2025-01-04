'''
raw_set_pixel.py
This example shows how to set the pixels on the display individually without having to use pico graphics.
This method can be used to save on memory usage.
'''
import random
import asyncio
import hub75
import time

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

async def display_maze(maze):
    height = len(maze)
    width = len(maze[0])
    
    while True:
        for y in range(height):
            for x in range(width):
                if maze[y][x] == 1:
                    h75.set_pixel(x, y, 100, 100, 100)  # White color for walls
                else:
                    h75.set_pixel(x, y, 0, 0, 0)  # Black color for paths
        await asyncio.sleep(1)  # Display the maze continuously

async def main():
    width, height = 64, 32
    maze = generate_maze(width, height)
    await display_maze(maze)

if __name__ == "__main__":
    asyncio.run(main())