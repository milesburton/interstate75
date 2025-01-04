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

# Define the flag colors
blue = (0, 0, 255)
yellow = (255, 255, 0)
red = (255, 0, 0)
green = (0, 255, 0)
# Define a simple flag pattern (Windows logo)
flag_pattern = [
    [blue, blue, blue, blue, yellow, yellow, yellow, yellow],
    [blue, blue, blue, blue, yellow, yellow, yellow, yellow],
    [blue, blue, blue, blue, yellow, yellow, yellow, yellow],
    [blue, blue, blue, blue, yellow, yellow, yellow, yellow],
    [red, red, red, red, green, green, green, green],
    [red, red, red, red, green, green, green, green],
    [red, red, red, red, green, green, green, green],
    [red, red, red, red, green, green, green, green]
]

async def waving_bouncing_flag_animation():
    width = 64
    height = 32
    flag_width = len(flag_pattern[0])
    flag_height = len(flag_pattern)
    amplitude = 2  # Amplitude of the wave
    frequency = 1  # Frequency of the wave
    phase = 0  # Initial phase

    # Initial position and velocity of the flag
    pos_x = (width - flag_width) // 2
    pos_y = (height - flag_height) // 2
    vel_x = 1
    vel_y = 1

    while True:
        h75.clear()
        for y in range(flag_height):
            for x in range(flag_width):
                # Calculate the wave offset
                offset = int(amplitude * math.sin(2 * math.pi * frequency * (x / flag_width) + phase))
                canvas_y = (y + offset + pos_y) % height  # Wrap around the height
                canvas_x = (x + pos_x) % width  # Ensure x coordinate stays within bounds
                if 0 <= canvas_x < width and 0 <= canvas_y < height:
 
        # Update the phase to animate the wave
        phase += 0.1

        # Update flag position
        pos_x += vel_x
        pos_y += vel_y

        # Bounce the flag off the edges
        if pos_x <= 0 or pos_x >= width - flag_width:
            vel_x = -vel_x
        if pos_y <= 0 or pos_y >= height - flag_height:
            vel_y = -vel_y

        await asyncio.sleep(0.05)  # Control animation speed

async def main():
    await waving_bouncing_flag_animation()

if __name__ == "__main__":
    asyncio.run(main())