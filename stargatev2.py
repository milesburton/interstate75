import hub75
import random
import time
import asyncio
import math

# Setup display
HEIGHT = 32
WIDTH = 64
MAX_PIXELS = 4

h75 = hub75.Hub75(WIDTH, HEIGHT, stb_invert=False)
def create_color_gradient():
    """Create a color gradient array."""
    gradient = []
    for i in range(256):
        # Simple gradient from blue to red
        r = i if i < 128 else 255 - i
        g = 0
        b = 255 - i if i < 128 else i
        gradient.append((r, g, b))
    return gradient

async def wormhole_animation():
    width = 64
    height = 32
    cx, cy = width // 2, height // 2  # Center of the display
    gradient = create_color_gradient()
    max_distance = math.sqrt(cx**2 + cy**2)

    while True:
        for frame in range(256):
          #  h75.clear()
            for x in range(width):
                for y in range(height):
                    # Calculate distance from the center
                    dx, dy = x - cx, y - cy
                    distance = math.sqrt(dx * dx + dy * dy)
                    index = int((distance / max_distance) * 255) % 256

                    # Get color from gradient
                    color = gradient[(index + frame) % 256]
                    h75.set_pixel(x, y, *color)

            await asyncio.sleep(0.05)  # Control animation speed

async def main():
    h75.start()
    await wormhole_animation()

if __name__ == "__main__":
    asyncio.run(main())