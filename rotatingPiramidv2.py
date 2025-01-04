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

def generate_random_axis():
    """Generate a random unit vector to serve as the axis of rotation."""
    x = random.uniform(-1, 1)
    y = random.uniform(-1, 1)
    z = random.uniform(-1, 1)
    length = math.sqrt(x*x + y*y + z*z)
    return x/length, y/length, z/length

def rotate_vertex(vertex, axis, angle):
    """Rotate a vertex around a given axis by a certain angle."""
    ux, uy, uz = axis
    x, y, z = vertex
    cos_angle = math.cos(angle)
    sin_angle = math.sin(angle)
    
    rot_x = (cos_angle + ux*ux*(1-cos_angle)) * x + (ux*uy*(1-cos_angle) - uz*sin_angle) * y + (ux*uz*(1-cos_angle) + uy*sin_angle) * z
    rot_y = (uy*ux*(1-cos_angle) + uz*sin_angle) * x + (cos_angle + uy*uy*(1-cos_angle)) * y + (uy*uz*(1-cos_angle) - ux*sin_angle) * z
    rot_z = (uz*ux*(1-cos_angle) - uy*sin_angle) * x + (uz*uy*(1-cos_angle) + ux*sin_angle) * y + (cos_angle + uz*uz*(1-cos_angle)) * z
    
    return rot_x, rot_y, rot_z

async def draw_3d_pyramid():
    width = 64
    height = 32
    fov = 40
    viewer_distance = 4
    angle = 0

    # Generate a random axis of rotation
    axis = generate_random_axis()

    while True:
        h75.clear()
        
        projected_points = []
        for vertex in vertices:
            # Rotate the vertex around the random axis
            rotated_vertex = rotate_vertex(vertex, axis, angle)
            x, y, z = rotated_vertex

            # Project the 3D coordinates to 2D
            x_2d, y_2d = project(x, y, z, width, height, fov, viewer_distance)
            projected_points.append((x_2d, y_2d))
        
        # Draw the edges of the pyramid
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