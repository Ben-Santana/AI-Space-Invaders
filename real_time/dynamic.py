import pygame
from game import WorldState, Object, Player, Boss, Enemy, Bullet, SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, GREEN, RED, clock



import pygame
def meteor_shower(worldstate):  # Introduces random meteors falling from the top of the screen
    import random
    # Define meteor attributes
    meteor_chance = 0.02  # Probability of a meteor appearing each frame
    meteor_speed = 3  # Speed at which meteors fall
    
    # Add new meteors at random
    if random.random() < meteor_chance:
        x_position = random.randint(0, SCREEN_WIDTH)
        meteor = {'x': x_position, 'y': 0, 'width': 10, 'height': 20}
        worldstate.meteors.append(meteor)

    # Move meteors and check for collisions
    for meteor in worldstate.meteors[:]:
        meteor['y'] += meteor_speed
        if meteor['y'] > SCREEN_HEIGHT:
            worldstate.meteors.remove(meteor)
        elif (worldstate.player.x < meteor['x'] < worldstate.player.x + worldstate.player.width and
              worldstate.player.y < meteor['y'] < worldstate.player.y + worldstate.player.height):
            worldstate.lives -= 1
            worldstate.meteors.remove(meteor)

# Summary:
# - Added meteor_shower: Introduces falling meteors that the player must avoid.