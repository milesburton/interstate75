import random
import asyncio
import hub75

HEIGHT = 32
WIDTH = 64
WATER_SURFACE_Y = HEIGHT // 3
FISHERMAN_X = 1
PLAYER_Y = WATER_SURFACE_Y - 1
HOOK_START_X = FISHERMAN_X + 1
HOOK_START_Y = WATER_SURFACE_Y

h75 = hub75.Hub75(WIDTH, HEIGHT, stb_invert=False)
h75.start()

# Player and Hook
hook_x = HOOK_START_X
hook_y = HOOK_START_Y
hook_active = False
hook_casting = False
rod_bend = 0

# Fish
fish_positions = [(random.randint(1, WIDTH-2), random.randint(WATER_SURFACE_Y+1, HEIGHT-2), random.randint(2, 3)) for _ in range(5)]
fish_directions = [(random.choice([-1, 1]), random.choice([-1, 1])) for _ in range(5)]
fish_jump = [False] * len(fish_positions)

# Waves
wave_offset = 0

# Fish patterns
fish_patterns = {
    2: [(0, 0), (1, 0), (0, 1), (1, 1)],  # Small fish
    3: [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],  # Large fish
}

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

async def draw_fisherman():
    h75.set_pixel(FISHERMAN_X, PLAYER_Y, 0, 255, 0)  # Green fisherman

async def draw_rod():
    if hook_active:
        rod_tip_y = PLAYER_Y + rod_bend
        rod_tip_x = min(WIDTH - 1, hook_x)
        
        # Draw the rod vertically
        for y in range(PLAYER_Y, rod_tip_y):
            h75.set_pixel(FISHERMAN_X, y, 139, 69, 19)  # Brown rod
        
        # Draw the rod horizontally
        for x in range(FISHERMAN_X + 1, rod_tip_x):
            h75.set_pixel(x, rod_tip_y, 139, 69, 19)  # Brown rod horizontal part

async def draw_hook():
    if hook_active:
        h75.set_pixel(hook_x, hook_y, 255, 255, 255)  # White hook
        if not hook_casting:
            for y in range(PLAYER_Y + rod_bend + 1, hook_y):
                h75.set_pixel(hook_x, y, 255, 255, 255)  # White line

async def draw_fish():
    for i, (x, y, size) in enumerate(fish_positions):
        pattern = fish_patterns[size]
        if fish_jump[i]:
            y -= 3  # Fish jumps 3 pixels above the water
        for dx, dy in pattern:
            if 0 <= x + dx < WIDTH and WATER_SURFACE_Y + 1 <= y + dy < HEIGHT:
                h75.set_pixel(x + dx, y + dy, 0, 0, 255)  # Blue fish

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

        # Random chance for fish to jump
        if random.random() < 0.01 and not fish_jump[i]:
            fish_jump[i] = True

        # If fish is jumping, animate splash and reset jump state
        if fish_jump[i] and new_y >= WATER_SURFACE_Y + 1:
            fish_jump[i] = False
            await animate_splash(new_x, WATER_SURFACE_Y + 1)

async def animate_splash(x, y):
    # Draw splash effect
    splash_pattern = [(0, 0), (-1, -1), (1, -1), (-1, 1), (1, 1)]
    for dx, dy in splash_pattern:
        if 0 <= x + dx < WIDTH and 0 <= y + dy < HEIGHT:
            h75.set_pixel(x + dx, y + dy, 255, 255, 255)  # White splash
    await asyncio.sleep(0.2)
    for dx, dy in splash_pattern:
        if 0 <= x + dx < WIDTH and 0 <= y + dy < HEIGHT:
            h75.set_pixel(x + dx, y + dy, 0, 0, 0)  # Clear splash

async def check_hook():
    global hook_x, hook_y, hook_active, hook_casting, rod_bend
    if hook_active:
        if hook_casting:
            hook_x += 1
            rod_bend += 1
            if hook_x >= WIDTH - 1 or rod_bend >= 5:
                hook_casting = False
                rod_bend = 0
        else:
            hook_y += 1
            if hook_y >= HEIGHT - 1:
                hook_active = False
                hook_x, hook_y = HOOK_START_X, HOOK_START_Y
            else:
                for i, (x, y, size) in enumerate(fish_positions):
                    pattern = fish_patterns[size]
                    for dx, dy in pattern:
                        if x + dx == hook_x and y + dy == hook_y:
                            fish_positions.pop(i)
                            fish_positions.append((random.randint(1, WIDTH-2), random.randint(WATER_SURFACE_Y+1, HEIGHT-2), random.randint(2, 3)))
                            hook_active = False
                            hook_x, hook_y = HOOK_START_X, HOOK_START_Y
                            break

async def game_loop():
    global hook_active, hook_casting, hook_x, hook_y
    while True:
        h75.clear()
        await draw_border()
        await draw_water_surface()
        await draw_fisherman()
        await draw_rod()
        await draw_hook()
        await draw_fish()
        await update_fish()
        await check_hook()
        await asyncio.sleep(0.1)

        # Simulate player input (for testing purposes)
        if random.random() < 0.05 and not hook_active:
            hook_active = True
            hook_casting = True

async def main():
    await game_loop()

if __name__ == "__main__":
    asyncio.run(main())
