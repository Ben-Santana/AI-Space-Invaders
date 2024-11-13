import math
import pygame
import sys
import random
sys.path.append('../')
from game import WorldState, Object, Player, Boss, Enemy, Bullet, SCREEN_WIDTH, SCREEN_HEIGHT, clock, PLAYER_HEIGHT, BLACK, WHITE, BLUE, ORANGE, PURPLE, RED, GREEN

def trigger_earthquake(worldstate):  # Simulates an earthquake that temporarily shakes the screen and disrupts gameplay
    if random.randint(0, 500) < 2:  # Small chance to initiate an earthquake each frame
        shake_intensity = 5
        duration = 100

        def draw_earthquake(obj, screen):
            offset_x = random.randint(-shake_intensity, shake_intensity)
            offset_y = random.randint(-shake_intensity, shake_intensity)
            screen.blit(screen, (offset_x, offset_y))

        def update_earthquake(obj):
            # Interfere with player and enemy positions
            if random.random() > 0.5:
                worldstate.player.x += random.choice([-shake_intensity, shake_intensity])
            for enemy in worldstate.enemies:
                enemy.x += random.choice([-shake_intensity, shake_intensity])
                enemy.y += random.choice([-shake_intensity, shake_intensity])
            
            # Decrease timer until the earthquake effect finishes
            obj.timer -= 1
            if obj.timer <= 0:
                worldstate.objects.remove(obj)

        earthquake_obj = Object(0, 0, draw_earthquake, update_earthquake)
        earthquake_obj.timer = duration
        worldstate.objects.append(earthquake_obj)

# Summary:
# - Added trigger_earthquake: Simulates screen shaking and affects player/enemy positions temporarily.

def add_portal(worldstate):  # Introduces a portal that teleports player across the screen
    if random.randint(0, 300) == 1:  # 0.33% chance to generate a portal each frame
        portal_x = random.randint(50, SCREEN_WIDTH - 50)

        def draw_portal(obj, screen):
            pygame.draw.ellipse(screen, (0, 255, 255), (obj.x, PLAYER_HEIGHT, 30, 60))
            pygame.draw.ellipse(screen, (0, 128, 128), (obj.x+5, PLAYER_HEIGHT+5, 20, 50))

        def update_portal(obj):
            player_rect = pygame.Rect(worldstate.player.x, PLAYER_HEIGHT, worldstate.player.width, worldstate.player.height)
            portal_rect = pygame.Rect(obj.x, PLAYER_HEIGHT, 30, 60)

            if player_rect.colliderect(portal_rect):
                worldstate.player.x = SCREEN_WIDTH - worldstate.player.x - worldstate.player.width

            if random.randint(0, 200) == 1:  # 0.5% chance to remove portal each frame
                worldstate.objects.remove(obj)

        worldstate.objects.append(Object(portal_x, PLAYER_HEIGHT, draw_portal, update_portal))

# Summary:
# - Added add_portal: Introduces a portal that teleports player across the screen.

def activate_time_freeze(worldstate):  # Temporarily freezes enemies and bullets for a few seconds occasionally
    if random.randint(0, 700) < 2:  # Roughly 0.28% chance to trigger time freeze per frame
        freeze_duration = 120  # Duration in frames (approximately 2 seconds at 60 FPS)

        # Stop movement of bullets enemies, and boss during freeze period
        for bullet in worldstate.bullets:
            if bullet.dy < 0:
                bullet.dy = 0
        for enemy in worldstate.enemies:
            enemy.speed = 0
        worldstate.boss.speed = 0

        def draw_freeze(obj, screen):
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(120)  # Set transparency to create an icy effect
            overlay.fill((0, 255, 255))  # Light blue color overlay
            screen.blit(overlay, (0, 0))

        def update_freeze(obj):
            obj.timer -= 1
            if obj.timer <= 0:
                # Restore normal movement
                for bullet in worldstate.bullets:
                    bullet.dy = -10
                for enemy in worldstate.enemies:
                    enemy.speed = 1  # Restore to default speed
                worldstate.boss.speed = 2
                worldstate.objects.remove(obj)

        freeze_obj = Object(0, 0, draw_freeze, update_freeze)
        freeze_obj.timer = freeze_duration
        worldstate.objects.append(freeze_obj)

# Summary:
# - Added activate_time_freeze: Temporarily freezes all enemies and bullets for a few seconds.

import pygame
import random

def deploy_replicating_mines(worldstate):  # Spawns mines that replicate if not destroyed in time
    if random.randint(0, 700) < 2:  # About 0.28% chance to deploy mines each frame
        mine_lifespan = 180  # Duration in frames (3 seconds at 60 FPS)
        mine_impact_radius = 40

        mine_x = random.randint(50, SCREEN_WIDTH - 50)
        mine_y = random.randint(50, SCREEN_HEIGHT - 200)

        def draw_mine(obj, screen):
            pygame.draw.circle(screen, (255, 75, 75), (obj.x, obj.y), 15)  # Mine core
            pygame.draw.circle(screen, (255, 105, 105), (obj.x, obj.y), 20, 1)  # Outer ring

        def update_mine(obj):
            obj.timer -= 1
            if obj.timer <= 0:
                worldstate.objects.remove(obj)
                mine_replicate(obj)  # Trigger replication if time runs out
            elif pygame.Rect(obj.x - mine_impact_radius, obj.y - mine_impact_radius, 2 * mine_impact_radius, 2 * mine_impact_radius).colliderect(
                worldstate.player.x, PLAYER_HEIGHT, worldstate.player.width, worldstate.player.height):
                worldstate.gameOver = True  # Game over if player collides with a mine
                worldstate.objects.remove(obj)

        def mine_replicate(obj):
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # Four directions for replication
            for dx, dy in directions:
                new_mine_x = obj.x + dx * 40
                new_mine_y = obj.y + dy * 40
                if 0 < new_mine_x < SCREEN_WIDTH and 0 < new_mine_y < SCREEN_HEIGHT:
                    new_mine = Object(new_mine_x, new_mine_y, draw_mine, update_mine)
                    new_mine.timer = mine_lifespan
                    worldstate.objects.append(new_mine)

        initial_mine = Object(mine_x, mine_y, draw_mine, update_mine)
        initial_mine.timer = mine_lifespan
        worldstate.objects.append(initial_mine)

# Summary:
# - Added deploy_replicating_mines: Mines spawn and replicate if not destroyed in time.