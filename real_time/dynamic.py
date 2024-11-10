import math
import pygame
import sys
import random
sys.path.append('../')
from game import WorldState, Object, Player, Boss, Enemy, Bullet, SCREEN_WIDTH, SCREEN_HEIGHT, clock, PLAYER_HEIGHT, BLACK, WHITE, BLUE, ORANGE, PURPLE, RED, GREEN


import random

def add_power_up(worldstate):  # Introduces a random power-up that can be collected by the player
    if random.randint(0, 1000) < 3:  # 0.3% chance to generate a power-up each frame
        power_up_x = random.randint(0, SCREEN_WIDTH - 20)
        power_up_speed = random.uniform(1, 3)

        def draw_power_up(obj, screen):
            pygame.draw.circle(screen, BLUE, (obj.x, obj.y), 10)

        def update_power_up(obj):
            obj.y += power_up_speed
            if obj.y > SCREEN_HEIGHT:
                worldstate.objects.remove(obj)  # Remove power-up when out of screen
            
            player_rect = pygame.Rect(worldstate.player.x, PLAYER_HEIGHT, worldstate.player.width, worldstate.player.height)
            power_up_rect = pygame.Rect(obj.x - 10, obj.y - 10, 20, 20)
            if power_up_rect.colliderect(player_rect):
                worldstate.player.fastFire = True  # Enable fast shooting when collected
                worldstate.objects.remove(obj)

        worldstate.objects.append(Object(power_up_x, 0, draw_power_up, update_power_up))

# Summary:
# - Added add_power_up: Introduces a random power-up that grants fast shooting.

import random

def add_teleport_portal(worldstate):  # Creates a portal that the player can use to teleport across the screen
    if random.randint(0, 1500) < 2:  # Small chance to generate a teleport portal
        portal_x1 = random.randint(20, SCREEN_WIDTH - 70)
        portal_x2 = random.randint(20, SCREEN_WIDTH - 70)

        def draw_portal(obj, screen):
            pygame.draw.ellipse(screen, ORANGE, (obj.x, PLAYER_HEIGHT - 5, 50, 30))

        def update_portal(obj):
            player_rect = pygame.Rect(worldstate.player.x, PLAYER_HEIGHT, worldstate.player.width, worldstate.player.height)
            portal_rect = pygame.Rect(obj.x, PLAYER_HEIGHT - 5, 50, 30)

            if portal_rect.colliderect(player_rect):
                worldstate.player.x = SCREEN_WIDTH - worldstate.player.x - worldstate.player.width  # Teleport player to the opposite side
                worldstate.objects.remove(obj)  # Remove portal after use

            # Optionally, add a timer so that the portal disappears after a few seconds
            obj.timer -= 1
            if obj.timer <= 0:
                worldstate.objects.remove(obj)

        # Append two portals at once so the player can use either of them to teleport
        for portal_x in [portal_x1, portal_x2]:
            teleport_obj = Object(portal_x, PLAYER_HEIGHT - 30, draw_portal, update_portal)
            teleport_obj.timer = 600  # Portal remains for 10 seconds if not used
            worldstate.objects.append(teleport_obj)

# Summary:
# - Added add_teleport_portal: Creates portals for the player to teleport across the screen.

import random

def add_enemy_shield(worldstate):  # Gives a temporary shield to a random enemy, making it invulnerable
    if worldstate.enemies and random.randint(0, 1500) < 2:  # Small chance to shield an enemy each frame
        protected_enemy = random.choice(worldstate.enemies)
        original_color = PURPLE

        def draw_shielded_enemy(obj, screen):
            pygame.draw.rect(screen, BLUE, (obj.x, obj.y, obj.width, obj.height))  # Blue color for shielded enemy

        def update_shielded_enemy(obj):
            # Keep moving enemy, ensuring it keeps its shield for a duration
            obj.x += obj.speed * obj.direction
            if obj.x <= 20 or obj.x + obj.width >= SCREEN_WIDTH - 20:
                obj.direction *= -1

            obj.timer -= 1
            if obj.timer <= 0:
                # Revert enemy to its original state when shield duration ends
                obj.draw_function = lambda obj, screen: pygame.draw.rect(screen, original_color, (obj.x, obj.y, obj.width, obj.height))
                worldstate.objects.remove(obj)

        shielded_enemy_obj = Object(protected_enemy.x, protected_enemy.y, draw_shielded_enemy, update_shielded_enemy)
        shielded_enemy_obj.width = protected_enemy.width
        shielded_enemy_obj.height = protected_enemy.height
        shielded_enemy_obj.speed = protected_enemy.speed
        shielded_enemy_obj.direction = protected_enemy.direction
        shielded_enemy_obj.timer = 600  # Shield lasts for 10 seconds
        worldstate.objects.append(shielded_enemy_obj)

# Summary:
# - Added add_enemy_shield: Temporarily grants an invulnerability shield to a random enemy.

import random

def add_gravity_well(worldstate):  # Introduces a gravity well that affects bullet trajectories
    if random.randint(0, 2000) < 2:  # Small chance to generate a gravity well each frame
        well_x = random.randint(100, SCREEN_WIDTH - 100)
        well_y = random.randint(100, SCREEN_HEIGHT - 200)

        def draw_gravity_well(obj, screen):
            pygame.draw.circle(screen, (150, 0, 255), (int(obj.x), int(obj.y)), 15)

        def update_gravity_well(obj):
            for bullet in worldstate.bullets:
                dx = obj.x - bullet.x
                dy = obj.y - bullet.y
                dist = math.sqrt(dx**2 + dy**2)
                if dist < 200:  # Affect bullets within a certain radius
                    force = 500 / (dist**2)  # Gravity effect becomes stronger as bullets get closer
                    angle = math.atan2(dy, dx)
                    bullet.x += math.cos(angle) * force
                    bullet.y += math.sin(angle) * force

            obj.timer -= 1
            if obj.timer <= 0:
                worldstate.objects.remove(obj)

        gravity_well_obj = Object(well_x, well_y, draw_gravity_well, update_gravity_well)
        gravity_well_obj.timer = 800  # Gravity well lasts for about 13 seconds
        worldstate.objects.append(gravity_well_obj)

# Summary:
# - Added add_gravity_well: Introduces a gravity well that affects bullet trajectories.