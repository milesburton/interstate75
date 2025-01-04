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
    return x, y, z

# Generate vertices for the cylinder part of the mug
def generate_cylinder_vertices(radius, height, segments):
    vertices = []
    for i in range(segments):
        angle = 2 * math.pi * i / segments
        x = radius * math.cos(angle)
        z = radius * math.sin(angle)
        vertices.append((x, -height / 2, z))  # Bottom circle
        vertices.append((x, height / 2, z))   # Top circle
    return vertices

# Generate vertices for the handle part of the mug
def generate_handle_vertices(radius, segments):
    vertices = []
    for i in range(segments):
        angle = 2 * math.pi * i / segments
        x = radius * math.cos(angle) + 1.5
        z = radius * math.sin(angle)
        vertices.append((x, 0, z))
    return vertices

# Define the faces of the mug
def generate_cylinder_faces(segments):
    faces = []
    for i in range(segments):
        bottom1 = 2 * i
        top1 = 2 * i + 1
        bottom2 = 2 * ((i + 1) % segments)
        top2 = 2 * ((i + 1) % segments) + 1
        faces.append((bottom1, bottom2, top2, top1))  # Side faces
    return faces

def generate_handle_faces(segments):
    faces = []
    for i in range(segments - 1):
        faces.append((i + len(cylinder_vertices), i + 1 + len(cylinder_vertices), (i + 2) % segments + len(cylinder_vertices)))
    return faces

# Combine the vertices and faces
cylinder_vertices = generate_cylinder_vertices(1, 2, 12)
handle_vertices = generate_handle_vertices(0.5, 12)
vertices = cylinder_vertices + handle_vertices

cylinder_faces = generate_cylinder_faces(12)
handle_faces = generate_handle_faces(12)
faces = cylinder_faces + handle_faces

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

def fill_polygon(vertices, color):
    """Fill a polygon using the vertices provided."""
    # Find the bounding box of the polygon
    min_x = min(vertices, key=lambda v: v[0])[0]
    max_x = max(vertices, key=lambda v: v[0])[0]
    min_y = min(vertices, key=lambda v: v[1])[1]
    max_y = max(vertices, key=lambda v: v[1])[1]

    # Scanline fill algorithm
    for y in range(min_y, max_y + 1):
        intersections = []
        for i in range(len(vertices)):
            v1 = vertices[i]
            v2 = vertices[(i + 1) % len(vertices)]
            if (v1[1] <= y < v2[1]) or (v2[1] <= y < v1[1]):
                x = int(v1[0] + (y - v1[1]) * (v2[0] - v1[0]) / (v2[1] - v1[1]))
                intersections.append(x)
        intersections.sort()
        for i in range(0, len(intersections), 2):
            for x in range(intersections[i], intersections[i + 1] + 1):
                h75.set_pixel(x, y, *color)

async def draw_3d_mug():
    width = 64
    height = 32
    fov = 30
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
            x_2d, y_2d, z_2d = project(x, y, z, width, height, fov, viewer_distance)
            projected_points.append((x_2d, y_2d, z_2d))
        
        # Sort faces by depth
        faces.sort(key=lambda face: sum(projected_points[vertex][2] for vertex in face) / len(face), reverse=True)

        # Draw the faces of the mug
        for face in faces:
            face_vertices = [projected_points[vertex] for vertex in face]
            avg_z = sum(v[2] for v in face_vertices) / len(face_vertices)
            color_intensity = int(100 * (1 - avg_z / (viewer_distance + fov)))
            color = (color_intensity, color_intensity, color_intensity)
            fill_polygon([(v[0], v[1]) for v in face_vertices], color)

        # Update the angle for rotation
        angle += 0.05

async def main():
    await draw_3d_mug()

if __name__ == "__main__":
    asyncio.run(main())