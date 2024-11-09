

def spawn_power_up(worldstate):  # Spawns a power-up that increases player speed temporarily when collected
    import random
    
    if not hasattr(worldstate, 'power_up'):
        worldstate.power_up = None
        worldstate.power_up_timer = 0

    # Spawn a power-up every 1000 frames if there is none
    if worldstate.power_up is None and random.randint(1, 1000) == 1:
        power_up_x = random.randint(0, SCREEN_WIDTH - 20)
        power_up_y = random.randint(50, SCREEN_HEIGHT - 100)
        worldstate.power_up = pygame.Rect(power_up_x, power_up_y, 20, 20)

    # Check if the player collects the power-up
    if worldstate.power_up:
        if (worldstate.player.x < worldstate.power_up.x + 20 and 
            worldstate.player.x + worldstate.player.width > worldstate.power_up.x and
            worldstate.player.y < worldstate.power_up.y + 20 and
            worldstate.player.y + worldstate.player.height > worldstate.power_up.y):
            
            worldstate.player.speed += 2
            worldstate.power_up = None
            worldstate.power_up_timer = 600  # 10 seconds at 60 FPS

    # Draw the power-up
    if worldstate.power_up:
        pygame.draw.rect(screen, (0, 255, 0), worldstate.power_up)

    # Handle the power-up timer
    if worldstate.power_up_timer > 0:
        worldstate.power_up_timer -= 1
        if worldstate.power_up_timer == 0:
            worldstate.player.speed = 5

# Summary:
# - Added spawn_power_up: Introduces a power-up that increases player speed temporarily when collected.