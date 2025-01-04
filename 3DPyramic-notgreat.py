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

# Define the vertices of the hexagonal pyramid
vertices = [
    (0, 1, -1.5),   # Apex
    (1, 1, 0),      # Base vertices
    (0.5, 1, math.sqrt(3)/2),
    (-0.5, 1, math.sqrt(3)/2),
    (-1, 1, 0),
    (-0.5, 1, -math.sqrt(3)/2),
    (0.5, 1, -math.sqrt(3)/2)
]

# Define the edges of the hexagonal pyramid
edges = [
    (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6),  # Apex to base vertices
    (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 1)  # Base edges
]

async def draw_3d_pyramid():
    width = 64
    height = 32
    fov = 256
    viewer_distance = 30
    angle_x = 0
    angle_y = 0
    angle_z = 0

    while True:
        h75.clear()
        cos_angle_x = math.cos(angle_x)
        sin_angle_x = math.sin(angle_x)
        cos_angle_y = math.cos(angle_y)
        sin_angle_y = math.sin(angle_y)
        cos_angle_z = math.cos(angle_z)
        sin_angle_z = math.sin(angle_z)
        
        projected_points = []
        for vertex in vertices:
            x, y, z = vertex

            # Apply rotation around X axis
            y_rot = y * cos_angle_x - z * sin_angle_x
            z_rot = z * cos_angle_x + y * sin_angle_x
            x_rot = x

            # Apply rotation around Y axis
            x_rot = x_rot * cos_angle_y - z_rot * sin_angle_y
            z_rot = z_rot * cos_angle_y + x_rot * sin_angle_y
            y_rot = y_rot

            # Apply rotation around Z axis
            x_final = x_rot * cos_angle_z - y_rot * sin_angle_z
            y_final = y_rot * cos_angle_z + x_rot * sin_angle_z
            z_final = z_rot

            # Project the 3D coordinates to 2D
            x_2d, y_2d = project(x_final, y_final, z_final, width, height, fov, viewer_distance)
            projected_points.append((x_2d, y_2d))
        
        # Draw the edges of the pyramid
        for edge in edges:
            start, end = edge
            x1, y1 = projected_points[start]
            x2, y2 = projected_points[end]
            draw_line(x1, y1, x2, y2)

        # Update the angles for rotation
        angle_x += 0.03
        angle_y += 0.05
        angle_z += 0.04
        await asyncio.sleep(0.1)

def draw_line(x1, y1, x2, y2):
    """Bresenham's Line Algorithm"""
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy
    while True:
        h75.set_pixel(x1, y1, 255, 255, 255)  # White color for the edges
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
    await draw_3d_pyramid()

if __name__ == "__main__":
    asyncio.run(main())