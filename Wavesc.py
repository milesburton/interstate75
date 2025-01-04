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
    base_amplitudes = [8, 6, 4]  # Base amplitudes for depth effect
    frequency = 2  # Frequency of the waves
    phase_increments = [0.1, 0.08, 0.06]  # Different phase increments for animation
    colors = [(0, 0, 150), (0, 0, 100), (0, 0, 500)]  # Different shades of blue for depth effect
    phases = [0, 0, 0]  # Initial phases for each wave layer

    while True:
        h75.clear()
        for layer in range(len(base_amplitudes)):
            # Randomly vary the amplitude around the base amplitude
            amplitude = base_amplitudes[layer] + random.uniform(-1, 1)
            phase = phases[layer]
            color = colors[layer]

            for x in range(width):
                # Calculate the y value for the sine wave
                y = int(midline + amplitude * math.sin(2 * math.pi * frequency * x / width + phase))
                
                # Draw the point
                h75.set_pixel(x, y, *color)

            # Update the phase to animate the wave
            phases[layer] += phase_increments[layer]

        await asyncio.sleep(0.000 5)  # Control animation speed

async def main():
    await river_wave_animation()

if __name__ == "__main__":
    asyncio.run(main())