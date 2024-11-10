import pygame
from game import WorldState, Obstacle, Player, Boss, Enemy, Bullet, SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, GREEN, RED, screen, clock


import pygame
def deploy_shield_over_player(worldstate):  # Deploys a temporary shield over the player
    shield_duration = 300  # Duration for the shield to stay active
    shield_activation_score = 100  # Score at which the shield is activated

    if worldstate.score >= shield_activation_score:
        current_time = pygame.time.get_ticks()
        if not hasattr(worldstate, 'shield_activated'):
            worldstate.shield_activated = current_time

        if current_time - worldstate.shield_activated < shield_duration:
            # Draw a shield around the player
            shield_color = (0, 255, 0)
            player_x = worldstate.player.x
            player_y = worldstate.player.y
            shield_padding = 5
            shield_rect = (
                player_x - shield_padding,
                player_y - shield_padding,
                worldstate.player.width + 2 * shield_padding,
                worldstate.player.height + 2 * shield_padding
            )
            pygame.draw.rect(worldstate.screen, shield_color, shield_rect, 2)

            # Prevent enemy bullets from hitting the player
            for bullet in worldstate.bullets:
                if (
                    bullet.x > player_x - shield_padding
                    and bullet.x < player_x + worldstate.player.width + shield_padding
                    and bullet.y > player_y - shield_padding
                    and bullet.y < player_y + worldstate.player.height + shield_padding
                ):
                    worldstate.bullets.remove(bullet)

        # Reset shield activation when duration is exceeded
        else:
            delattr(worldstate, 'shield_activated')

# Summary:
# - Added deploy_shield_over_player: Activates a temporary shield above the player at a certain score.

import pygame
import random

def create_shield(worldstate):  # Randomly creates shields for the player at the bottom of the screen
    shield_width = 100
    shield_height = 10
    shield_y = SCREEN_HEIGHT - worldstate.player.height - 20
    
    if len(worldstate.shields) < 3:  # Limiting the number of active shields
        shield_x = random.randint(0, SCREEN_WIDTH - shield_width)
        worldstate.shields.append({'x': shield_x, 'y': shield_y, 'width': shield_width, 'height': shield_height})

# Summary:
# - Added create_shield: Creates defensive shields below the player for protection from enemy bullets.

import pygame
import random

def add_enemy_shields(worldstate):  # Allows random enemies to have a protective shield
    for enemy in worldstate.enemies:
        if hasattr(enemy, 'shield') and enemy.shield > 0:
            continue
        if random.randint(0, 100) < 10:  # 10% chance to acquire a shield on each loop
            enemy.shield = random.randint(1, 3)  # Shield strength 1 to 3

def handle_enemy_shield_collision(worldstate):  # Handles collision with shielded enemies
    for bullet in worldstate.bullets:
        for enemy in worldstate.enemies:
            if enemy.shield > 0 and enemy.rect.colliderect(bullet.rect):
                enemy.shield -= 1
                worldstate.bullets.remove(bullet)
                if enemy.shield <= 0:
                    worldstate.enemies.remove(enemy)
                break

# Summary:
# - Added add_enemy_shields: Enables random enemies to have shields that require multiple hits to be destroyed.
# - Added handle_enemy_shield_collision: Manages interactions and collisions with shielded enemies.

import pygame
import random

def spawn_meteors(worldstate):  # Spawns meteors that fall from the top of the screen
    meteor_width = 20
    meteor_height = 20
    meteor_speed = 3
    num_meteors = 5
    
    if len(worldstate.meteors) < num_meteors:
        for _ in range(num_meteors - len(worldstate.meteors)):
            x_position = random.randint(0, SCREEN_WIDTH - meteor_width)
            new_meteor = {'x': x_position, 'y': 0, 'width': meteor_width, 'height': meteor_height, 'speed': meteor_speed}
            worldstate.meteors.append(new_meteor)
            
    for meteor in worldstate.meteors:
        meteor['y'] += meteor['speed']
        if meteor['y'] > SCREEN_HEIGHT:
            worldstate.meteors.remove(meteor)
        elif (worldstate.player.x < meteor['x'] < worldstate.player.x + worldstate.player.width or 
              worldstate.player.x < meteor['x'] + meteor['width'] < worldstate.player.x + worldstate.player.width) and \
             (worldstate.player.y < meteor['y'] < worldstate.player.y + worldstate.player.height or 
              worldstate.player.y < meteor['y'] + meteor['height'] < worldstate.player.y + worldstate.player.height):
            worldstate.player.health -= 1
            worldstate.meteors.remove(meteor)

# Summary:
# - Added spawn_meteors: Introduces falling meteors for a Level 2 challenge.

import pygame
def scatter_enemy_fire(worldstate):  # Enemies randomly fire bullets to increase challenge
    import random
    if worldstate.enemies:
        firing_chance = 0.01
        for enemy in worldstate.enemies:
            if random.random() < firing_chance:
                bullet = Bullet(enemy.x + enemy.width // 2, enemy.y + enemy.height, -5)
                worldstate.bullets.append(bullet)

# Summary:
# - Added scatter_enemy_fire: Enemies occasionally fire bullets to enhance difficulty.

import pygame
def activate_shield(worldstate):  # Activates a temporary shield for the player that absorbs one attack
    if not hasattr(worldstate.player, 'shield_active'):
        worldstate.player.shield_active = False
    
    if not hasattr(worldstate.player, 'shield_duration'):
        worldstate.player.shield_duration = 0

    if worldstate.score >= 100 and not worldstate.player.shield_active:
        worldstate.player.shield_active = True
        worldstate.player.shield_duration = 300  # Activate the shield for 5 seconds

    if worldstate.player.shield_active:
        worldstate.player.shield_duration -= 1
        if worldstate.player.shield_duration <= 0:
            worldstate.player.shield_active = False
     
    if worldstate.player.shield_active:
        # Detect collision with bullets or enemies
        # Pseudo-code for collision detection, a real collision check should be implemented
        for bullet in worldstate.bullets:
            if bullet.collides_with(worldstate.player):
                worldstate.bullets.remove(bullet)
                worldstate.player.shield_active = False
                break

# Summary:
# - Added activate_shield: Implemented a temporary shield for the player that activates upon reaching a score of 100 and absorbs attacks for 5 seconds.

import pygame
def activate_enemy_bullets(worldstate):  # Enables enemies to shoot towards the player
    for enemy in worldstate.enemies:
        if worldstate.score >= 300 and worldstate.score < 500:  # Level 3 criteria
            if random.randint(1, 100) <= 5:  # 5% chance to shoot each frame
                enemy_bullet = Bullet(enemy.x + enemy.width // 2, enemy.y, -1, 5)  # Create enemy bullet
                worldstate.bullets.append(enemy_bullet)

# Summary:
# - Added activate_enemy_bullets: Introduces enemy shooting mechanics when score is between 300 and 500.

import pygame
import random

def spawn_shield_pickup(worldstate):  # Spawns a shield power-up occasionally for the player to collect
    if random.randint(0, 1000) > 995:
        shield_x = random.randint(0, SCREEN_WIDTH - 20)
        shield_y = random.randint(0, SCREEN_HEIGHT - 20)
        worldstate.shields.append({'x': shield_x, 'y': shield_y})

def apply_shield(worldstate):  # Applies shield power-up when player collides with it
    new_shields = []
    for shield in worldstate.shields:
        if (worldstate.player.x < shield['x'] < worldstate.player.x + worldstate.player.width or
                shield['x'] < worldstate.player.x < shield['x'] + 20) and \
           (worldstate.player.y < shield['y'] < worldstate.player.y + worldstate.player.height or
                shield['y'] < worldstate.player.y < shield['y'] + 20):
            worldstate.player.is_shielded = True
            worldstate.player.shield_timer = 300  # Shield lasts for 300 frames
        else:
            new_shields.append(shield)
    worldstate.shields = new_shields

def update_shield_effect(worldstate):  # Updates shield status and effect duration
    if worldstate.player.is_shielded:
        worldstate.player.shield_timer -= 1
        if worldstate.player.shield_timer <= 0:
            worldstate.player.is_shielded = False

# Summary:
# - Added spawn_shield_pickup: Spawns a collectible shield power-up on the screen.
# - Added apply_shield: Activates shield when player collects power-up.
# - Added update_shield_effect: Manages the duration and deactivation of the shield.

import pygame
import random

def introduce_meteor_shower(worldstate):  # Adds meteor shower obstacles to increase level difficulty
    if random.randint(1, 100) <= 5:  # 5% chance to introduce a new meteor each frame
        meteor = {
            'x': random.randint(0, SCREEN_WIDTH),
            'y': 0,
            'speed': random.randint(2, 5),
            'width': 20,
            'height': 20
        }
        worldstate.meteors.append(meteor)

    for meteor in worldstate.meteors:
        meteor['y'] += meteor['speed']
        if meteor['y'] > SCREEN_HEIGHT:
            worldstate.meteors.remove(meteor)
        elif (worldstate.player.x < meteor['x'] < worldstate.player.x + worldstate.player.width and
                worldstate.player.y < meteor['y'] < worldstate.player.y + worldstate.player.height):
            worldstate.lives -= 1
            worldstate.meteors.remove(meteor)

# Summary:
# - Added introduce_meteor_shower: Introduces meteor obstacles that randomly appear.

import pygame
def introduce_enemy_shields(worldstate):  # Introduces temporary shields for enemies at Level 3
    if worldstate.current_level == 3:
        for enemy in worldstate.enemies:
            if not hasattr(enemy, 'shield'):  # Add shield attribute if not present
                enemy.shield = True
                enemy.shield_duration = 300  # Duration of shield

            if enemy.shield:
                enemy.shield_duration -= 1
                if enemy.shield_duration <= 0:
                    enemy.shield = False  # Remove shield after duration ends

            # Prevent bullets from hitting shielded enemies
            for bullet in worldstate.bullets:
                if enemy.shield and (enemy.rect.colliderect(bullet.rect)):
                    worldstate.bullets.remove(bullet)

# Summary:
# - Added introduce_enemy_shields: Implements temporary shields for enemies in Level 3.