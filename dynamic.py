

def introduce_shield_powerup(worldstate):  # Introduces a shield power-up that temporarily protects the player from enemy bullets
    if not hasattr(worldstate, 'shield_active'):
        worldstate.shield_active = False
        worldstate.shield_duration = 0
        worldstate.shield_cooldown = 300  # Cooldown time in frames
        worldstate.shield_timer = 0
    
    if not worldstate.shield_active and worldstate.shield_timer == 0:
        if worldstate.score >= 50 and worldstate.score % 50 == 0:
            worldstate.shield_active = True
            worldstate.shield_duration = 180  # Active time in frames

    if worldstate.shield_active:
        worldstate.shield_duration -= 1
        if worldstate.shield_duration <= 0:
            worldstate.shield_active = False
            worldstate.shield_timer = worldstate.shield_cooldown

    if worldstate.shield_timer > 0:
        worldstate.shield_timer -= 1

    if worldstate.shield_active:
        pygame.draw.rect(screen, (0, 0, 255), (worldstate.player.x, worldstate.player.y, worldstate.player.width, worldstate.player.height), 3)

# Summary:
# - Added introduce_shield_powerup: Implements a shield power-up that gives the player temporary immunity from bullets, activated based on score milestones.