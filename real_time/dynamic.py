import math
import pygame
import sys
import random
sys.path.append('../')
from game import WorldState, Object, Player, Boss, Enemy, Bullet, SCREEN_WIDTH, SCREEN_HEIGHT, clock, PLAYER_HEIGHT, BLACK, WHITE, BLUE, ORANGE, PURPLE, RED, GREEN

def create_random_portals(worldstate):  # Introduces portals that teleport the player
    if len(worldstate.objects) == 0 and random.randint(0, 1000) < 5:  # 0.5% chance to spawn portals
        portal_x = [random.randint(20, SCREEN_WIDTH - 70) for _ in range(2)]  # Two portals at random positions

        def draw_portal1(obj, screen):
            pygame.draw.ellipse(screen, BLUE, (obj.x, obj.y, 40, 60))
            pygame.draw.ellipse(screen, ORANGE, (obj.x + 10, obj.y + 10, 20, 40))

        def draw_portal2(obj, screen):
            pygame.draw.ellipse(screen, BLUE, (obj.x, obj.y, 40, 60))
            pygame.draw.ellipse(screen, PURPLE, (obj.x + 10, obj.y + 10, 20, 40))

        def update_portal1(obj):
            if pygame.Rect(obj.x, obj.y, 40, 60).colliderect(worldstate.player.x, PLAYER_HEIGHT, worldstate.player.width, worldstate.player.height):
                worldstate.player.x = portal_x[1]  # Teleport player to second portal when entering first
                worldstate.objects.clear()  # Remove portals after use

        def update_portal2(obj):
            if pygame.Rect(obj.x, obj.y, 40, 60).colliderect(worldstate.player.x, PLAYER_HEIGHT, worldstate.player.width, worldstate.player.height):
                worldstate.player.x = portal_x[0]  # Teleport player to first portal when entering second
                worldstate.objects.clear()  # Remove portals after use

        # Create and append two portal objects
        worldstate.objects.append(Object(portal_x[0], PLAYER_HEIGHT, draw_portal1, update_portal1))
        worldstate.objects.append(Object(portal_x[1], PLAYER_HEIGHT, draw_portal2, update_portal2))

# Summary:
# - Added create_random_portals: Introduces a pair of portals that the player can use to teleport.

def add_homing_missiles(worldstate):  # Adds enemy homing missiles for increased difficulty
    if random.randint(0, 1000) < 5:  # 0.5% chance for an enemy to fire a homing missile
        enemy = random.choice(worldstate.enemies)
        missile_speed = 3

        def draw_missile(obj, screen):
            pygame.draw.circle(screen, RED, (obj.x, obj.y), 5)

        def update_missile(obj):
            dx = worldstate.player.x + worldstate.player.width // 2 - obj.x
            dy = PLAYER_HEIGHT + worldstate.player.height // 2 - obj.y
            dist = max(1, (dx**2 + dy**2)**0.5)
            obj.x += missile_speed * dx / dist
            obj.y += missile_speed * dy / dist
            if pygame.Rect(obj.x, obj.y, 5, 5).colliderect(
                worldstate.player.x, PLAYER_HEIGHT, worldstate.player.width, worldstate.player.height
            ):
                worldstate.gameOver = True
            if obj.y > SCREEN_HEIGHT or obj.x < 0 or obj.x > SCREEN_WIDTH:
                worldstate.objects.remove(obj)

        worldstate.objects.append(Object(enemy.x + enemy.width // 2, enemy.y + enemy.height, draw_missile, update_missile))

# Summary:
# - Added add_homing_missiles: Introduces homing missiles that track the player.

import random
import pygame

def add_shields(worldstate):  # Introduces protective shields for the player
    if len([obj for obj in worldstate.objects if getattr(obj, 'is_shield', False)]) == 0 and random.randint(0, 1000) < 5:  # 0.5% chance to spawn a shield
        shield_duration = 300  # Duration of the shield in frames

        def draw_shield(obj, screen):
            pygame.draw.ellipse(screen, (0, 255, 255), (worldstate.player.x - 10, PLAYER_HEIGHT - 10, worldstate.player.width + 20, worldstate.player.height + 20), 2)

        def update_shield(obj):
            nonlocal shield_duration
            shield_duration -= 1
            if shield_duration <= 0:
                worldstate.objects.remove(obj)

        shield_obj = Object(worldstate.player.x, PLAYER_HEIGHT, draw_shield, update_shield)
        shield_obj.is_shield = True
        worldstate.objects.append(shield_obj)

# Summary:
# - Added add_shields: Introduces temporary protective shields around the player.

def add_energy_orbs(worldstate):  # Introduces energy orbs that grant temporary speed boost
    if random.randint(0, 1000) < 10:  # 1% chance to spawn an energy orb
        orb_x = random.randint(20, SCREEN_WIDTH - 40)
        orb_y = random.randint(20, SCREEN_HEIGHT - 80)
        orb_speed_boost_duration = 180  # Duration of speed boost in frames
        orb_collected = False

        def draw_orb(obj, screen):
            pygame.draw.circle(screen, (255, 255, 0), (obj.x, obj.y), 10)  # Draws a yellow orb

        def update_orb(obj):
            nonlocal orb_collected
            if not orb_collected:
                if pygame.Rect(obj.x, obj.y, 20, 20).colliderect(worldstate.player.x, PLAYER_HEIGHT, worldstate.player.width, worldstate.player.height):
                    orb_collected = True
                    worldstate.player.speed += 4
            else:
                orb_speed_boost_duration -= 1
                if orb_speed_boost_duration <= 0:
                    worldstate.objects.remove(obj)
                    worldstate.player.speed -= 4

        worldstate.objects.append(Object(orb_x, orb_y, draw_orb, update_orb))

# Summary:
# - Added add_energy_orbs: Introduces energy orbs that boost player speed temporarily.

import pygame
import random

def add_meteor_shower(worldstate):  # Adds a meteor shower to increase difficulty
    if random.randint(0, 100) < 2:  # 2% chance to generate a meteor per frame
        meteor_x = random.randint(0, SCREEN_WIDTH - 30)
        meteor_speed = random.uniform(2, 5)

        def draw_meteor(obj, screen):
            pygame.draw.ellipse(screen, (150, 150, 150), (obj.x, obj.y, 30, 15))  # Gray meteor color
            pygame.draw.line(screen, (255, 0, 0), (obj.x + 5, obj.y + 7.5), (obj.x + 25, obj.y + 7.5), 1)  # Add a line representing flame

        def update_meteor(obj):
            obj.y += meteor_speed
            if obj.y > SCREEN_HEIGHT:
                worldstate.objects.remove(obj)  # Remove meteor when out of screen
            if pygame.Rect(obj.x, obj.y, 30, 15).colliderect(worldstate.player.x, PLAYER_HEIGHT, worldstate.player.width, worldstate.player.height):
                worldstate.gameOver = True

        worldstate.objects.append(Object(meteor_x, 0, draw_meteor, update_meteor))

# Summary:
# - Added add_meteor_shower: Introduces a meteor shower that can collide with the player.

def add_gravitational_pull(worldstate):  # Introduces a dynamic gravitational pull affecting player and bullets
    center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
    gravitational_force = 0.2

    def apply_gravity(x, y, obj_x, obj_y):
        dx = center_x - obj_x
        dy = center_y - obj_y
        distance = max(1, math.hypot(dx, dy))
        force_x = gravitational_force * dx / distance
        force_y = gravitational_force * dy / distance
        return x + force_x, y + force_y

    def update_physics(obj):
        if isinstance(obj, Bullet):
            obj.x, obj.y = apply_gravity(obj.x, obj.y, obj.x, obj.y)
        elif isinstance(obj, Player):
            worldstate.player.x, _ = apply_gravity(worldstate.player.x, PLAYER_HEIGHT, worldstate.player.x, PLAYER_HEIGHT)

    for bullet in worldstate.bullets:
        update_physics(bullet)
    update_physics(worldstate.player)

# Summary:
# - Added add_gravitational_pull: Players and bullets are affected by gravitational pull towards the center.

def add_rainbow_bonus(worldstate):  # Introduces bonus orbs that increase player's score
    if len([obj for obj in worldstate.objects if getattr(obj, 'is_bonus', False)]) == 0 and random.randint(0, 1000) < 3:
        bonus_x = random.randint(20, SCREEN_WIDTH - 40)
        bonus_y = random.randint(20, SCREEN_HEIGHT - 80)
        bonus_lifetime = 300

        def draw_bonus(obj, screen):
            pygame.draw.circle(screen, random.choice([RED, GREEN, BLUE, ORANGE, PURPLE, WHITE]), (obj.x, obj.y), 15)

        def update_bonus(obj):
            nonlocal bonus_lifetime
            bonus_lifetime -= 1
            if bonus_lifetime <= 0 or pygame.Rect(obj.x, obj.y, 15, 15).colliderect(worldstate.player.x, PLAYER_HEIGHT, worldstate.player.width, worldstate.player.height):
                if pygame.Rect(obj.x, obj.y, 15, 15).colliderect(worldstate.player.x, PLAYER_HEIGHT, worldstate.player.width, worldstate.player.height):
                    worldstate.score += 50
                worldstate.objects.remove(obj)

        bonus_obj = Object(bonus_x, bonus_y, draw_bonus, update_bonus)
        bonus_obj.is_bonus = True
        worldstate.objects.append(bonus_obj)

# Summary:
# - Added add_rainbow_bonus: Introduces orbs that increase player's score if collected.

import random
import pygame

def add_black_hole(worldstate):  # Introduces a black hole that pulls enemies towards it
    if len([obj for obj in worldstate.objects if getattr(obj, 'is_black_hole', False)]) == 0 and random.randint(0, 1000) < 3:  # 0.3% chance to spawn a black hole
        black_hole_x = random.randint(100, SCREEN_WIDTH - 100)
        black_hole_y = random.randint(100, SCREEN_HEIGHT - 200)
        pull_force = 0.5

        def draw_black_hole(obj, screen):
            pygame.draw.circle(screen, (0, 0, 0), (obj.x, obj.y), 25)
            pygame.draw.circle(screen, (100, 0, 255), (obj.x, obj.y), 30, 2)

        def update_black_hole(obj):
            for enemy in worldstate.enemies:
                dx = obj.x - (enemy.x + enemy.width // 2)
                dy = obj.y - (enemy.y + enemy.height // 2)
                dist = max(1, math.hypot(dx, dy))
                if dist < 150:  # Only pull enemies within a certain range
                    enemy.x += pull_force * dx / dist
                    enemy.y += pull_force * dy / dist

        black_hole_obj = Object(black_hole_x, black_hole_y, draw_black_hole, update_black_hole)
        black_hole_obj.is_black_hole = True
        worldstate.objects.append(black_hole_obj)

# Summary:
# - Added add_black_hole: Introduces a black hole that pulls nearby enemies toward it.