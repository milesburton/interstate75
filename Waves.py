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

async def river_wave_animation():
    width = 64
    height = 32
    midline = height // 2
    amplitude1 = 8
    amplitude2 = 4
    frequency1 = 2  # Number of full waves in the display width
    frequency2 = 4
    phase1 = 0
    phase2 = 0

    while True:
        h75.clear()
        for x in range(width):
            # Calculate y values for two sine waves
            y1 = int(midline + amplitude1 * math.sin(2 * math.pi * frequency1 * x / width + phase1))
            y2 = int(midline + amplitude2 * math.sin(2 * math.pi * frequency2 * x / width + phase2))
            
            # Combine the two sine waves to create a more complex wave pattern
            y = (y1 + y2) // 2

            # Draw the points
            h75.set_pixel(x, y, 0, 0, 10)  # Color the waves blue

        # Update the phases to animate the waves
        phase1 += 0.1
        phase2 += 0.05

        # Swap the canvas to display the updated wave pattern
        await asyncio.sleep(0.005)  # Control animation speed

async def main():
    await river_wave_animation()

if __name__ == "__main__":
    asyncio.run(main())