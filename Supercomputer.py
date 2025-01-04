import hub75
import random
import time

HEIGHT = 32
WIDTH = 64
MAX_PIXELS = 64

h75 = hub75.Hub75(WIDTH, HEIGHT, stb_invert=False)
def rand_pixel():
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    return x, y

def random_color():
    """Generate a random color as a tuple of (R, G, B)."""
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def pulse_led(x, y, start_color, end_color, steps=50, delay=0.01):
    """Pulse an LED from start_color to end_color and back to start_color."""
    r1, g1, b1 = start_color
    r2, g2, b2 = end_color

    # Pulse to the end color
    for i in range(steps):
        r = r1 + (r2 - r1) * i // steps
        g = g1 + (g2 - g1) * i // steps
        b = b1 + (b2 - b1) * i // steps

        print('Setting Pixel x: {0} y: {1}'.format(x, y))
        h75.set_pixel(x, y, r, g, b)
        time.sleep(delay)

    # Pulse back to the start color
    for i in range(steps):
        r = r2 + (r1 - r2) * i // steps
        g = g2 + (g1 - g2) * i // steps
        b = b2 + (b1 - b2) * i // steps

        print('Setting Pixel x: {0} y: {1}'.format(x, y))
        h75.set_pixel(x, y, r, g, b)
        time.sleep(delay)
        
    h75.set_pixel(x, y, 0, 0, 0)

def main():
    h75.start()
    width = 64
    height = 32
    
    while True:
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        start_color = 0,0,0
        end_color = 255,255,255
        
        pulse_led(x, y, start_color, end_color)

main()