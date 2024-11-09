

def introduce_powerup(worldstate):  # Introduces a temporary speed boost power-up for the player
    import random
    if not hasattr(worldstate, 'powerup') and random.random() < 0.01:  # 1% chance each frame
        worldstate.powerup = {
            'x': random.randint(0, SCREEN_WIDTH - 20),
            'y': -20,  # Start above the screen
            'width': 20,
            'height': 20,
            'color': (0, 255, 0)  # Green power-up
        }

    if hasattr(worldstate, 'powerup'):
        worldstate.powerup['y'] += 3  # Power-up falls down

        # Check player collision with the power-up
        player = worldstate.player
        if (player.x < worldstate.powerup['x'] + worldstate.powerup['width'] and
            player.x + player.width > worldstate.powerup['x'] and
            player.y < worldstate.powerup['y'] + worldstate.powerup['height'] and
            player.y + player.height > worldstate.powerup['y']):
            worldstate.player.speed += 2  # Increase player speed temporarily
            del worldstate.powerup

        # Remove the power-up if it goes off screen
        if worldstate.powerup['y'] > SCREEN_HEIGHT:
            del worldstate.powerup

# Summary:
# - Added introduce_powerup: Introduces a speed boost power-up that the player can collect.