import pygame
import sys
sys.path.append('../')
from game import WorldState, Object, Player, Boss, Enemy, Bullet, SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, GREEN, RED, clock


import random
import pygame

def add_wormhole_teleport(worldstate):  # Adds wormholes to teleport enemies around the screen
    if len(worldstate.enemies) > 0 and random.randint(0, 100) < 1:  # 1% chance to activate a wormhole
        selected_enemy = random.choice(worldstate.enemies)

        def draw_wormhole(obj, screen):
            pygame.draw.circle(screen, (0, 0, 200), (obj.x, obj.y), 20)

        def update_wormhole(obj):
            if random.randint(0, 100) < 5:  # 5% chance per frame to teleport enemy
                selected_enemy.x = random.randint(0, SCREEN_WIDTH - selected_enemy.width)
                selected_enemy.y = random.randint(0, SCREEN_HEIGHT / 2)  # Enemy teleports within top half
                worldstate.objects.remove(obj)

        wormhole_x = selected_enemy.x + selected_enemy.width // 2
        wormhole_y = selected_enemy.y + selected_enemy.height // 2
        
        worldstate.objects.append(Object(wormhole_x, wormhole_y, draw_wormhole, update_wormhole))

# Summary:
# - Added add_wormhole_teleport: Introduces teleporting enemies to increase challenge.

def add_wormhole(worldstate):  # Adds wormholes that transport player to random positions
    if random.randint(0, 1000) < 5:  # Low chance to spawn a wormhole
        wormhole_x = random.randint(0, SCREEN_WIDTH - 50)
        wormhole_y = random.randint(50, SCREEN_HEIGHT - 50)

        def draw_wormhole(obj, screen):
            pygame.draw.ellipse(screen, (0, 128, 128), (obj.x, obj.y, 50, 50))

        def update_wormhole(obj):
            if pygame.Rect(obj.x, obj.y, 50, 50).colliderect(worldstate.player.x, worldstate.player.y, worldstate.player.width, worldstate.player.height):
                worldstate.player.x = random.randint(0, SCREEN_WIDTH - worldstate.player.width)
                worldstate.objects.remove(obj)  # Remove wormhole after use

        worldstate.objects.append(Object(wormhole_x, wormhole_y, draw_wormhole, update_wormhole))

# Summary:
# - Added add_wormhole: Creates wormholes that transport the player randomly.