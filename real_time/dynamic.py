import math
import pygame
import sys
import random
sys.path.append('../')
from game import WorldState, Object, Player, Boss, Enemy, Bullet, SCREEN_WIDTH, SCREEN_HEIGHT, clock, PLAYER_HEIGHT, BLACK, WHITE, BLUE, ORANGE, PURPLE, RED, GREEN


def add_black_hole(worldstate):  # Introduces a black hole that pulls player and bullets towards its center
    if random.randint(0, 1000) < 5:  # 0.5% chance to spawn a black hole frame
        black_hole_x = random.randint(100, SCREEN_WIDTH - 100)
        black_hole_y = random.randint(100, SCREEN_HEIGHT - 200)
        black_hole_radius = 50

        def draw_black_hole(obj, screen):
            pygame.draw.circle(screen, (0, 0, 0), (int(obj.x), int(obj.y)), int(black_hole_radius * (1 + 0.1 * math.sin(pygame.time.get_ticks() / 200))))

        def update_black_hole(obj):
            for bullet in worldstate.bullets:
                dx = obj.x - bullet.x
                dy = obj.y - bullet.y
                distance = math.hypot(dx, dy)
                if distance < black_hole_radius * 3:
                    bullet.x += dx * 0.05
                    bullet.y += dy * 0.05
                
            dx = obj.x - worldstate.player.x
            if abs(dx) < black_hole_radius * 3:
                worldstate.player.x += dx * 0.05

            if pygame.Rect(obj.x - black_hole_radius, obj.y - black_hole_radius, black_hole_radius * 2, black_hole_radius * 2).colliderect(worldstate.player.x, PLAYER_HEIGHT, worldstate.player.width, worldstate.player.height):
                worldstate.gameOver = True
            
            if pygame.time.get_ticks() % 500 == 0:  # Disappear after some time 
                worldstate.objects.remove(obj)

        worldstate.objects.append(Object(black_hole_x, black_hole_y, draw_black_hole, update_black_hole))

# Summary:
# - Added add_black_hole: Introduces a black hole pulling player and bullets.

import random
import pygame

def add_portals(worldstate):  # Adds portals that teleport the player across the screen
    def draw_portal(obj, screen):
        pygame.draw.ellipse(screen, (0, 255, 255), (int(obj.x), int(obj.y), 50, 100))

    def update_portal(obj):
        player_rect = pygame.Rect(worldstate.player.x, PLAYER_HEIGHT, worldstate.player.width, worldstate.player.height)
        portal_rect = pygame.Rect(obj.x, obj.y, 50, 100)
        
        if player_rect.colliderect(portal_rect):
            worldstate.player.x = SCREEN_WIDTH - worldstate.player.x - worldstate.player.width  # Teleport to the opposite side
            worldstate.objects.remove(obj)  # Remove the portal after use

    if len([(obj.x, obj.y) for obj in worldstate.objects if isinstance(obj, Object) and hasattr(obj.draw_function, '__call__')]) < 2:  # Limit to two portals
        portal_x = random.choice([0, SCREEN_WIDTH - 50])  # Portals appear randomly at the far sides of the screen
        portal_y = random.randint(PLAYER_HEIGHT - 100, PLAYER_HEIGHT - 50)
        worldstate.objects.append(Object(portal_x, portal_y, draw_portal, update_portal))

# Summary:
# - Added add_portals: Introduces portals that teleport the player across the screen.

import random
import pygame

def add_shield_pickup(worldstate):  # Introduces a shield pickup that grants temporary invincibility
    if random.randint(0, 2000) < 1:  # 0.05% chance to spawn a shield pickup frame
        shield_x = random.randint(20, SCREEN_WIDTH - 70)
        shield_y = random.randint(100, SCREEN_HEIGHT - 150)
        shield_duration = 5000  # Shield lasts for 5 seconds

        def draw_shield(obj, screen):
            pygame.draw.ellipse(screen, (0, 255, 0), (int(obj.x), int(obj.y), 50, 50))

        def update_shield(obj):
            player_rect = pygame.Rect(worldstate.player.x, PLAYER_HEIGHT, worldstate.player.width, worldstate.player.height)
            shield_rect = pygame.Rect(obj.x, obj.y, 50, 50)

            if player_rect.colliderect(shield_rect):
                worldstate.player.invincible = True

                def remove_invincibility():
                    worldstate.player.invincible = False
                
                pygame.time.set_timer(pygame.USEREVENT, shield_duration)
                worldstate.enemies = [enemy for enemy in worldstate.enemies]
                worldstate.objects.remove(obj)

        def check_events():
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT:
                    remove_invincibility()

        worldstate.objects.append(Object(shield_x, shield_y, draw_shield, update_shield))
        check_events()

# Summary:
# - Added add_shield_pickup: Introduces a shield pickup for temporary invincibility.

import random
import pygame
import math

def add_sine_wave_movement(worldstate):  # Adds enemies that move in a sine wave pattern for increased challenge
    for enemy in worldstate.enemies:
        enemy.original_y = hasattr(enemy, 'original_y') and enemy.original_y or enemy.y
        sine_wave_amplitude = 30
        sine_wave_frequency = 0.05
        enemy.y = enemy.original_y + sine_wave_amplitude * math.sin(worldstate.score * sine_wave_frequency)

    if worldstate.level >= 2:  # Implement sine wave movement starting from level 2
        for enemy in worldstate.enemies:
            enemy.direction = -1 if enemy.x >= SCREEN_WIDTH - enemy.width - 20 else (1 if enemy.x <= 20 else enemy.direction)
            enemy.x += enemy.speed * enemy.direction

# Summary:
# - Added add_sine_wave_movement: Enemies move in a sine wave pattern for increased challenge.

import random
import pygame

def deploy_space_mines(worldstate):  # Deploys space mines that explode when approached, damaging nearby enemies or the player
    if random.randint(0, 1000) < 5:  # 0.5% chance to deploy a space mine frame
        mine_x = random.randint(50, SCREEN_WIDTH - 70)
        mine_y = random.randint(100, SCREEN_HEIGHT - 150)
        mine_radius = 20

        def draw_mine(obj, screen):
            pygame.draw.circle(screen, (200, 200, 0), (int(obj.x), int(obj.y)), mine_radius)

        def update_mine(obj):
            player_rect = pygame.Rect(worldstate.player.x, PLAYER_HEIGHT, worldstate.player.width, worldstate.player.height)
            mine_rect = pygame.Rect(obj.x - mine_radius, obj.y - mine_radius, mine_radius * 2, mine_radius * 2)

            if player_rect.colliderect(mine_rect):
                worldstate.gameOver = True
            else:
                # Check collision with enemies
                for enemy in worldstate.enemies[:]:
                    enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
                    if mine_rect.colliderect(enemy_rect):
                        worldstate.enemies.remove(enemy)

            if random.randint(0, 100) < 3:  # Random chance for mine to explode
                if enemy in worldstate.enemies[:]:
                    worldstate.enemies.remove(enemy)
                worldstate.objects.remove(obj)

        worldstate.objects.append(Object(mine_x, mine_y, draw_mine, update_mine))

# Summary:
# - Added deploy_space_mines: Deploys space mines that explode on approach, affecting enemies or the player.

import random
import pygame

def add_powerup_asteroid(worldstate):  # Adds asteroids that drop power-ups when destroyed
    if random.randint(0, 1000) < 5:  # 0.5% chance to spawn an asteroid per frame
        asteroid_x = random.randint(50, SCREEN_WIDTH - 70)
        asteroid_y = -20  # Start off-screen
        asteroid_radius = 30

        def draw_asteroid(obj, screen):
            pygame.draw.circle(screen, (128, 128, 128), (int(obj.x), int(obj.y)), asteroid_radius)

        def update_asteroid(obj):
            obj.y += 2  # Asteroids move downwards
            if obj.y > SCREEN_HEIGHT:
                worldstate.objects.remove(obj)

            # Check collision with bullets
            for bullet in worldstate.bullets[:]:
                if pygame.Rect(bullet.x, bullet.y, bullet.width, bullet.height).colliderect(obj.x - asteroid_radius, obj.y - asteroid_radius, asteroid_radius * 2, asteroid_radius * 2):
                    worldstate.bullets.remove(bullet)
                    worldstate.objects.remove(obj)
                    spawn_powerup(worldstate, obj.x, obj.y)

        worldstate.objects.append(Object(asteroid_x, asteroid_y, draw_asteroid, update_asteroid))

def spawn_powerup(worldstate, x, y):
    powerup_type = random.choice(["fast_fire", "invincibility"])
    powerup_duration = 1000

    def draw_powerup(obj, screen):
        color = (0, 255, 0) if obj.type == "invincibility" else (255, 165, 0)
        pygame.draw.ellipse(screen, color, (obj.x, obj.y, 20, 20))

    def update_powerup(obj):
        obj.y += 1  # Power-up slowly descends
        if obj.y > SCREEN_HEIGHT:
            worldstate.objects.remove(obj)

        player_rect = pygame.Rect(worldstate.player.x, PLAYER_HEIGHT, worldstate.player.width, worldstate.player.height)
        powerup_rect = pygame.Rect(obj.x, obj.y, 20, 20)

        if player_rect.colliderect(powerup_rect):
            if obj.type == "fast_fire":
                worldstate.player.fastFire = True
            elif obj.type == "invincibility":
                worldstate.player.invincible = True

            def deactivate_powerup():
                if obj.type == "fast_fire":
                    worldstate.player.fastFire = False
                elif obj.type == "invincibility":
                    worldstate.player.invincible = False

            pygame.time.set_timer(pygame.USEREVENT, powerup_duration)
            worldstate.objects.remove(obj)
            check_events = lambda: None  

            def check_events():
                for event in pygame.event.get():
                    if event.type == pygame.USEREVENT:
                        deactivate_powerup()
            
            worldstate.dynamic_function = check_events

    powerup_obj = Object(x, y, draw_powerup, update_powerup)
    powerup_obj.type = powerup_type
    worldstate.objects.append(powerup_obj)

# Summary:
# - Added add_powerup_asteroid: Asteroids drop power-ups when destroyed, enhancing gameplay.

import random
import pygame

def add_time_warp(worldstate):  # Introduces time warp objects that temporarily slow down enemy movement
    if random.randint(0, 1000) < 3:  # 0.3% chance to spawn a time warp per frame
        warp_x = random.randint(50, SCREEN_WIDTH - 70)
        warp_y = random.randint(100, SCREEN_HEIGHT - 150)
        
        def draw_time_warp(obj, screen):
            pygame.draw.circle(screen, (0, 0, 255), (int(obj.x), int(obj.y)), 20)  # Blue circle
        
        def update_time_warp(obj):
            player_rect = pygame.Rect(worldstate.player.x, PLAYER_HEIGHT, worldstate.player.width, worldstate.player.height)
            warp_rect = pygame.Rect(obj.x - 20, obj.y - 20, 40, 40)
            
            if player_rect.colliderect(warp_rect):
                for enemy in worldstate.enemies:
                    enemy.speed = max(0.5, enemy.speed / 2)  # Slow down enemies
                worldstate.objects.remove(obj)

            if pygame.time.get_ticks() % 500 == 0:  # Time warp effect expires after a short duration
                for enemy in worldstate.enemies:
                    enemy.speed = min(2, enemy.speed * 2)  # Restore speed
                worldstate.objects.remove(obj)
                
        worldstate.objects.append(Object(warp_x, warp_y, draw_time_warp, update_time_warp))

# Summary:
# - Added add_time_warp: Introduces time warp objects that slow enemy movement temporarily.