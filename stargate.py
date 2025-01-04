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
def hsv_to_rgb(h, s, v):
    """Convert HSV to RGB color."""
    if s == 0.0: return (v, v, v)
    i = int(h*6.0)  # Assume hue < 1
    f = (h*6.0) - i
    p = v * (1.0 - s)
    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0 - f))
    i = i % 6
    if i == 0: return (v, t, p)
    if i == 1: return (q, v, p)
    if i == 2: return (p, v, t)
    if i == 3: return (p, q, v)
    if i == 4: return (t, p, v)
    if i == 5: return (v, p, q)

async def wormhole_animation():
    width = 64
    height = 32
    cx, cy = width // 2, height // 2  # Center of the display

    while True:
        for frame in range(360):
            for x in range(width):
                for y in range(height):
                    # Calculate distance and angle from the center
                    dx, dy = x - cx, y - cy
                    distance = math.sqrt(dx * dx + dy * dy)
                    angle = (math.atan2(dy, dx) + math.pi) / (2 * math.pi)
                    
                    # Create a pulsing effect based on distance and frame
                    hue = (angle + frame / 360) % 1.0
                    saturation = 1.0
                    value = (1 + math.sin(distance / 2.0 - frame / 10.0)) / 2.0
                    
                    # Convert HSV to RGB
                    r, g, b = hsv_to_rgb(hue, saturation, value)
                    
                    # Set pixel color
                    h75.set_pixel(x, y, int(r * 255), int(g * 255), int(b * 255))

            await asyncio.sleep(0.003)  # Control animation speed

async def main():
    h75.start()
    await wormhole_animation()

if __name__ == "__main__":
    asyncio.run(main())