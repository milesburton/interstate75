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

async def pulse_led(x, y, color, steps=50, delay=0.01):
    """Pulse an LED from start_color to end_color and back to start_color."""
    r, g, b = color

    # Pulse to the end color
    for i in range(steps):
        current_r = r * i // steps
        current_g = g * i // steps
        current_b = b * i // steps

        print('Setting Pixel x: {0} y: {1}. Color: {2}'.format(x, y, current_r))
        h75.set_pixel(x, y, r, g, b)
        h75.update()
        asyncio.sleep(delay)

    # Pulse back to the start color
    for i in range(steps):
        current_r = r * (steps - i) // steps
        current_g = g * (steps - i) // steps
        current_b = b * (steps - i) // steps

        print('Setting Pixel x: {0} y: {1}. Color: {2}'.format(x, y, current_r))
        h75.set_pixel(x, y, r, g, b)
        h75.update()
        asyncio.sleep(delay)


async def pulse_pixel(x, y):
    """Manage the pulsing of a single pixel."""
    while True:
        color = (255,0,0)
        random_delay = random.uniform(0.01, 0.5)  # Random delay between pulses
        await pulse_led(x, y, color, delay=random_delay)

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