

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

def drop_random_obstacles(worldstate):  # Drops random obstacles that the player must avoid
    import random
    if random.randint(0, 100) < 5:  # 5% chance to drop a new obstacle each frame
        obstacle = Obstacle(
            random.randint(0, SCREEN_WIDTH - 50),  # Random X position within screen width
            0,  # Start at the top of the screen
            50,  # Width of the obstacle
            20,  # Height of the obstacle
            5  # Speed of the obstacle falling down
        )
        worldstate.obstacles.append(obstacle)

    for obstacle in list(worldstate.obstacles):  # Iterate over a copy of the list
        obstacle.y += obstacle.speed  # Move the obstacle down the screen
        if obstacle.y > SCREEN_HEIGHT:  # Remove obstacle if it moves beyond the bottom
            worldstate.obstacles.remove(obstacle)

class Obstacle:  # Define an Obstacle class to handle obstacle properties
    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed

# Adjust worldstate initialization (outside the function):
worldstate.obstacles = []  # Add an 'obstacles' list attribute to the worldstate

# Summary:
# - Added drop_random_obstacles: Periodically drops obstacles that the player must dodge to survive.

def spawn_shield_power_up(worldstate):  # Spawns a protective shield power-up that can be collected by the player
    import random
    if random.randint(0, 100) < 5:  # 5% chance to spawn a power-up each frame
        shield_power_up = {
            'x': random.randint(0, SCREEN_WIDTH - 30),
            'y': 0,  # Start at the top of the screen
            'width': 30,
            'height': 30,
            'speed': 2,
            'active': True
        }
        worldstate.power_ups.append(shield_power_up)

    for power_up in worldstate.power_ups:
        if power_up['active']:
            power_up['y'] += power_up['speed']
            if power_up['y'] > SCREEN_HEIGHT:
                power_up['active'] = False

    for power_up in list(worldstate.power_ups):
        if power_up['active']:
            player_rect = worldstate.player.rect()
            power_up_rect = (
                power_up['x'], power_up['y'], power_up['width'], power_up['height'])
            if player_rect.colliderect(power_up_rect):
                worldstate.player.shielded = True
                worldstate.power_ups.remove(power_up)
                break

def manage_shield_effect(worldstate):  # Manages the shield effect duration and rendering
    if hasattr(worldstate.player, 'shielded') and worldstate.player.shielded:
        if not hasattr(worldstate.player, 'shield_duration'):
            worldstate.player.shield_duration = 300  # Duration for shield effect in frames

        worldstate.player.shield_duration -= 1
        if worldstate.player.shield_duration <= 0:
            worldstate.player.shielded = False
            delattr(worldstate.player, 'shield_duration')

def render_shield(worldstate, screen):  # Renders the shield effect if active
    if hasattr(worldstate.player, 'shielded') and worldstate.player.shielded:
        import pygame
        shield_color = (0, 255, 255)
        player_rect = worldstate.player.rect()
        pygame.draw.ellipse(screen, shield_color, player_rect.inflate(10, 10), 2)

# Summary:
# - Added spawn_shield_power_up: Spawns a protective shield power-up on the screen, collectable by the player.
# - Added manage_shield_effect: Controls the duration and state of the active shield on the player.
# - Added render_shield: Visually represents the shield effect around the player when active.

def introduce_boss_level(worldstate):  # Introduces a boss enemy with unique attack patterns and higher difficulty
    # Check if the current level is 3 and the boss hasn't been introduced yet
    if worldstate.level == 3 and not hasattr(worldstate, 'boss'):
        # Create a boss enemy
        boss = {
            'x': SCREEN_WIDTH // 2,
            'y': 100,
            'width': 150,
            'height': 50,
            'speed': 2,
            'direction': 1,  # 1 for right, -1 for left
            'health': 20
        }
        
        worldstate.boss = boss

    # If the boss exists, handle its movement and attacks
    if hasattr(worldstate, 'boss'):
        # Move the boss
        worldstate.boss['x'] += worldstate.boss['speed'] * worldstate.boss['direction']
        
        # Reverse direction if it hits the screen edge
        if worldstate.boss['x'] <= 0 or worldstate.boss['x'] + worldstate.boss['width'] >= SCREEN_WIDTH:
            worldstate.boss['direction'] *= -1
        
        # Introduce a unique attack pattern: boss drops explosive shots
        if worldstate.frame_count % 60 == 0:  # Fire every 60 frames
            new_bullet = {
                'x': worldstate.boss['x'] + worldstate.boss['width'] // 2,
                'y': worldstate.boss['y'] + worldstate.boss['height'],
                'speed': 5,
                'damage': 2
            }
            worldstate.bullets.append(new_bullet)

        # Check if the boss is hit by player's bullets and reduce health
        for bullet in worldstate.bullets:
            if worldstate.boss['x'] < bullet['x'] < worldstate.boss['x'] + worldstate.boss['width'] and worldstate.boss['y'] < bullet['y'] < worldstate.boss['y'] + worldstate.boss['height']:
                worldstate.boss['health'] -= 1
                worldstate.bullets.remove(bullet)

        # If boss health reaches 0, increase score significantly and remove boss
        if worldstate.boss['health'] <= 0:
            worldstate.score += 500
            del worldstate.boss

# Summary:
# - Added introduce_boss_level: Introduces a boss enemy with unique attack patterns for Level 3.

from random import randint

def spawn_shield_power_up(worldstate):  # Spawns a shield power-up that temporarily makes the player invincible
    if randint(1, 3600) == 1:  # Random chance to spawn a shield every 60 seconds (assuming 60 FPS)
        shield_power_up = {
            'x': randint(0, SCREEN_WIDTH - 20),  # Random x position, accounting for power-up width
            'y': randint(0, SCREEN_HEIGHT - 20),  # Random y position, accounting for power-up height
            'width': 20,
            'height': 20,
            'active': True
        }
        worldstate.shield_power_ups.append(shield_power_up)

    for power_up in worldstate.shield_power_ups:
        if power_up['active']:
            if (worldstate.player.position.x < power_up['x'] + power_up['width'] and
                    worldstate.player.position.x + worldstate.player.width > power_up['x'] and
                    worldstate.player.position.y < power_up['y'] + power_up['height'] and
                    worldstate.player.position.y + worldstate.player.height > power_up['y']):
                worldstate.player.invincible_timer = 180  # Player is invincible for 3 seconds
                power_up['active'] = False

    if hasattr(worldstate.player, 'invincible_timer') and worldstate.player.invincible_timer > 0:
        worldstate.player.invincible_timer -= 1
    else:
        worldstate.player.invincible_timer = 0

# Summary:
# - Added spawn_shield_power_up: Spawns a shield power-up on the field that makes the player invincible 
#   for a short duration upon collection.

def introduce_boss_level(worldstate):  # Introduces a boss enemy with higher health and power in Level 5
    if worldstate.level == 5 and not hasattr(worldstate, 'boss'):
        class Boss:
            def __init__(self):
                self.width = 60
                self.height = 60
                self.x = (SCREEN_WIDTH - self.width) / 2
                self.y = 50
                self.health = 50
                self.speed = 1
                self.direction = 1  # 1: right, -1: left

            def move(self):
                self.x += self.speed * self.direction
                if self.x <= 0 or self.x + self.width >= SCREEN_WIDTH:
                    self.direction *= -1

            def take_damage(self, damage):
                self.health -= damage
                if self.health <= 0:
                    worldstate.score += 50
                    worldstate.boss = None  # Remove boss when defeated

            def check_collision(self, bullet):
                if (bullet.x > self.x and bullet.x < self.x + self.width and
                        bullet.y > self.y and bullet.y < self.y + self.height):
                    return True
                return False

        worldstate.boss = Boss()  # Initialize the boss

    if hasattr(worldstate, 'boss') and worldstate.boss is not None:
        worldstate.boss.move()

        for bullet in worldstate.bullets:
            if worldstate.boss.check_collision(bullet):
                worldstate.boss.take_damage(10)
                worldstate.bullets.remove(bullet)  # Remove bullet after hitting the boss

# Summary:
# - Added introduce_boss_level: Introduces a boss enemy in Level 5 with higher health and movement across the screen.

import random

def asteroid_storm(worldstate):  # Introduces random falling asteroids as obstacles
    # Create a new asteroid object with random position and speed
    if random.randint(0, 100) < 5:  # 5% chance to create a new asteroid on each call
        asteroid = {
            'x': random.randint(0, SCREEN_WIDTH),  # Random horizontal position
            'y': 0,  # Start from the top of the screen
            'speed': random.randint(2, 5)  # Random descent speed
        }
        worldstate.asteroids.append(asteroid)
    
    # Update the position of each asteroid and check for off-screen or collision
    for asteroid in worldstate.asteroids[:]:
        asteroid['y'] += asteroid['speed']  # Move asteroid downwards

        if asteroid['y'] > SCREEN_HEIGHT:  # Remove asteroids that fall off the screen
            worldstate.asteroids.remove(asteroid)
        
        # Check for collision between player and asteroid
        if (worldstate.player.y < asteroid['y'] < worldstate.player.y + worldstate.player.height) and \
           (worldstate.player.x < asteroid['x'] < worldstate.player.x + worldstate.player.width):
            worldstate.player.lives -= 1  # Deduct a life if player is hit
            worldstate.asteroids.remove(asteroid)  # Remove the asteroid upon collision

# Summary:
# - Added asteroid_storm: Introduces random falling asteroids as obstacles that the player must avoid or risk losing lives.

import random

def spawn_enemy_obstacles(worldstate):  # Spawns enemy obstacles that move across the screen
    for _ in range(3):  # Spawning 3 obstacles
        x = random.randint(0, SCREEN_WIDTH - worldstate.enemies[0].width)
        y = random.randint(0, SCREEN_HEIGHT // 2)
        new_obstacle = Enemy(x, y)  # Assuming Enemy class can be used for obstacles
        new_obstacle.speed = random.randint(1, 3)
        new_obstacle.direction = "down"  # Obstacles move downward
        worldstate.enemies.append(new_obstacle)

    for enemy in worldstate.enemies:
        if hasattr(enemy, "direction") and enemy.direction == "down":
            enemy.y += enemy.speed
            if enemy.y > SCREEN_HEIGHT:
                worldstate.enemies.remove(enemy)

# Summary:
# - Added spawn_enemy_obstacles: Spawns moving enemy-like obstacles from the top of the screen that travel downwards.