import hub75
import random
import time
import math
import asyncio

HEIGHT = 32
WIDTH = 64
MAX_PIXELS = 64

h75 = hub75.Hub75(WIDTH, HEIGHT, stb_invert=False)
h75.start()

# Perspective projection function
def project(x, y, z, width, height, fov, viewer_distance):
    factor = fov / (viewer_distance + z)
    x = int(x * factor + width / 2)
    y = int(-y * factor + height / 2)
    return x, y

# Define the vertices of the 3D box
vertices = [
    (-1, -1, -1),
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, 1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, 1, 1)
]

# Define the edges of the 3D box
edges = [
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 0),
    (4, 5),
    (5, 6),
    (6, 7),
    (7, 4),
    (0, 4),
    (1, 5),
    (2, 6),
    (3, 7)
]

async def draw_3d_box():
    width = 64
    height = 32
    fov = 100
    viewer_distance = 40
    angle = 0

    while True:
        h75.clear()
        # Rotate the box around the Y axis
        cos_angle = math.cos(angle)
        sin_angle = math.sin(angle)
        
        projected_points = []
        for vertex in vertices:
            x, y, z = vertex
            # Apply rotation
            x_rot = x * cos_angle - z * sin_angle
            z_rot = z * cos_angle + x * sin_angle
            y_rot = y
            # Project the 3D coordinates to 2D
            x_2d, y_2d = project(x_rot, y_rot, z_rot, width, height, fov, viewer_distance)
            projected_points.append((x_2d, y_2d))
        
        # Draw the edges of the box
        for edge in edges:
            start, end = edge
            x1, y1 = projected_points[start]
            x2, y2 = projected_points[end]
            draw_line(x1, y1, x2, y2)

        # Update the angle for rotation
        angle += 0.05
        await asyncio.sleep(0.1)

def draw_line(x1, y1, x2, y2):
    """Bresenham's Line Algorithm"""
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy
    while True:
        h75.set_pixel(x1, y1, 100, 100, 100)  # White color for the edges
        if x1 == x2 and y1 == y2:
            break
        e2 = err * 2
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy

async def main():
    await draw_3d_box()

if __name__ == "__main__":
    asyncio.run(main())