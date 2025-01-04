import hub75
import math
import asyncio

HEIGHT = 32
WIDTH = 64
MAX_PIXELS = 64

h75 = hub75.Hub75(WIDTH, HEIGHT, stb_invert=False)
h75.start()

def mandelbrot_color(x, y, max_iter):
    c = complex(x, y)
    z = 0.0j
    for i in range(max_iter):
        z = z*z + c
        if (z.real*z.real + z.imag*z.imag) >= 4:
            return (i % 8 * 32, i % 16 * 16, i % 32 * 8)  # Color mapping
    return (0, 0, 0)

async def fractal_animation():
    width = 64
    height = 32
    max_iter = 100  # Reduced iterations for faster computation
    zoom = 1
    zoom_factor = 0.9  # Increased zoom factor for faster zoom effect
    move_x, move_y = -0.5, 0

    while True:
        h75.clear()

        for y in range(height):
            for x in range(width):
                # Convert pixel coordinate to complex number
                re = 1.5 * (x - width / 2) / (0.5 * zoom * width) + move_x
                im = (y - height / 2) / (0.5 * zoom * height) + move_y
                color = mandelbrot_color(re, im, max_iter)
                h75.set_pixel(x, y, *color)

        # Update zoom for animation effect
        zoom *= zoom_factor

        # Reset the animation if zoom level is too high
        if zoom < 0.001:
            zoom = 1
            move_x, move_y = -0.5, 0  # Reset position if needed

        await asyncio.sleep(0.05)  # Reduced sleep time for faster animation

async def main():
    await fractal_animation()

if __name__ == "__main__":
    asyncio.run(main())