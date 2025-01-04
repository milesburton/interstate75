import hub75
import random
import time
import math

HEIGHT = 32
WIDTH = 64
MAX_PIXELS = 64

h75 = hub75.Hub75(WIDTH, HEIGHT, stb_invert=False)
h75.start()


    
def draw_sinewave(cycles=4):
    width = 64
    height = 32
    amplitude = height // 6  # Amplitude of the sinewave
    midline = height // 2  # Midline of the sinewave

    for x in range(width):
        # Calculate the y value of the sinewave for multiple cycles
        y = int(midline + amplitude * math.sin(2 * math.pi * cycles * x / width))
        
        # Draw the point
        h75.set_pixel(x, y, 100, 0, 0)  # Color the sinewave red

def main():
    draw_sinewave(cycles=4)

if __name__ == "__main__":
    main()