import hub75
import random
import time
import asyncio

# Setup display
HEIGHT = 32
WIDTH = 64
MAX_PIXELS = 64

h75 = hub75.Hub75(WIDTH, HEIGHT, stb_invert=False)
def random_color():
    """Generate a random color as a tuple of (R, G, B)."""
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

async def pulse_led(x, y, start_color, end_color, steps=50, delay=0.01):
    """Pulse an LED from start_color to end_color and back to start_color."""
    r1, g1, b1 = start_color
    r2, g2, b2 = end_color

    # Pulse to the end color
    for i in range(steps):
        r = r1 + (r2 - r1) * i // steps
        g = g1 + (g2 - g1) * i // steps
        b = b1 + (b2 - b1) * i // steps

        h75.set_pixel(x, y, r, g, b)
        await asyncio.sleep(delay)

    # Pulse back to the start color
    for i in range(steps):
        r = r2 + (r1 - r2) * i // steps
        g = g2 + (g1 - g2) * i // steps
        b = b2 + (b1 - b2) * i // steps

        h75.set_pixel(x, y, r, g, b)
        await asyncio.sleep(delay)
    h75.set_pixel(x, y, 0, 0, 0)

async def pulse_pixel(x, y):
    """Manage the pulsing of a single pixel."""
    while True:
        start_color = random_color()
        end_color = random_color()
        random_delay = random.uniform(0.01, 0.5)  # Random delay between pulses
        await pulse_led(x, y, start_color, end_color, delay=random_delay)

async def main():
    h75.start()
    width = 64
    height = 32

    tasks = []
    for x in range(10):
        for y in range(10):
            task = asyncio.create_task(pulse_pixel(x, y))
            tasks.append(task)

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())