import random
import asyncio
import hub75

HEIGHT = 32
WIDTH = 64
WATER_SURFACE_Y = HEIGHT // 3
PLAYER_Y = WATER_SURFACE_Y - 2
HOOK_START_Y = WATER_SURFACE_Y

h75 = hub75.Hub75(WIDTH, HEIGHT, stb_invert=False)
h75.start()

# Player and Hook
player_x = WIDTH // 2
hook_y = HOOK_START_Y
hook_active = False

# Fish
fish_positions = [(random.randint(1, WIDTH-2), random.randint(WATER_SURFACE_Y+1, HEIGHT-2), random.randint(1, 3)) for _ in range(5)]
fish_directions = [(random.choice([-1, 1]), random.choice([-1, 1])) for _ in range(5)]

# Waves
wave_offset = 0

async def draw_border():
    for x in range(WIDTH):
        h75.set_pixel(x, 0, 255, 255, 255)  # Top border
        h75.set_pixel(x, HEIGHT - 1, 255, 255, 255)  # Bottom border

    for y in range(HEIGHT):
        h75.set_pixel(0, y, 255, 255, 255)  # Left border
        h75.set_pixel(WIDTH - 1, y, 255, 255, 255)  # Right border

async def draw_water_surface():
    global wave_offset
    wave_height = 2  # Increase the wave height for larger waves
    wave_frequency = 0.1  # Frequency of the waves
    for x in range(WIDTH):
        wave = int(wave_height * (1 + random.random() - 0.5) * 0.5)  # Larger waves
        h75.set_pixel(x, WATER_SURFACE_Y + wave, 0, 0, 255)  # Blue water surface
    wave_offset = (wave_offset + 1) % WIDTH

async def draw_player():
    h75.set_pixel(player_x, PLAYER_Y, 0, 255, 0)  # Green player

async def draw_hook():
    if hook_active:
        for y in range(WATER_SURFACE_Y, hook_y):
            h75.set_pixel(player_x, y, 255, 255, 255)  # White hook

async def draw_fish():
    for x, y, size in fish_positions:
        for i in range(size):
            for j in range(size):
                if 0 <= x+i < WIDTH and WATER_SURFACE_Y+1 <= y+j < HEIGHT:
                    h75.set_pixel(x + i, y + j, 0, 0, 255)  # Blue fish

async def update_fish():
    for i in range(len(fish_positions)):
        x, y, size = fish_positions[i]
        dx, dy = fish_directions[i]

        # Move fish
        new_x = x + dx
        new_y = y + dy

        # Check bounds and change direction if needed
        if new_x <= 1 or new_x + size >= WIDTH - 2:
            dx = -dx
        if new_y <= WATER_SURFACE_Y + 1 or new_y + size >= HEIGHT - 2:
            dy = -dy

        fish_positions[i] = (new_x, new_y, size)
        fish_directions[i] = (dx, dy)

async def check_hook():
    global hook_y, hook_active
    if hook_active:
        hook_y += 1
        if hook_y >= HEIGHT - 1:
            hook_active = False
            hook_y = HOOK_START_Y
        else:
            for i, (x, y, size) in enumerate(fish_positions):
                if x <= player_x < x + size and y <= hook_y < y + size:
                    fish_positions.pop(i)
                    fish_positions.append((random.randint(1, WIDTH-2), random.randint(WATER_SURFACE_Y+1, HEIGHT-2), random.randint(1, 3)))
                    hook_active = False
                    hook_y = HOOK_START_Y
                    break

async def game_loop():
    global player_x, hook_active, hook_y
    while True:
        h75.clear()
        await draw_border()
        await draw_water_surface()
        await draw_player()
        await draw_hook()
        await draw_fish()
        await update_fish()
        await check_hook()
        await asyncio.sleep(0.1)

        # Simulate player input (for testing purposes)
        if random.random() < 0.1:
            player_x = max(1, player_x - 1)
        elif random.random() < 0.2:
            player_x = min(WIDTH - 2, player_x + 1)
        if random.random() < 0.05 and not hook_active:
            hook_active = True

async def main():
    await game_loop()

if __name__ == "__main__":
    asyncio.run(main())
