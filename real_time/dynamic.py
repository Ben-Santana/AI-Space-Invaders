import pygame
import sys
import random
sys.path.append('../')
from game import WorldState, Object, Player, Boss, Enemy, Bullet, SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, GREEN, RED, clock


import random

def add_teleport_portal(worldstate):  # Adds teleport portals that randomly switch player position
    if len(worldstate.objects) < 2:  # Ensure only 2 portals exist at a time
        portal_x = random.randint(0, SCREEN_WIDTH - 30)
        portal_y = random.randint(0, SCREEN_HEIGHT - 30)

        def draw_portal(obj, screen):
            pygame.draw.ellipse(screen, (0, 100, 200), (obj.x, obj.y, 30, 30))

        def update_portal(obj):
            if pygame.Rect(obj.x, obj.y, 30, 30).colliderect(worldstate.player.x, worldstate.player.y, worldstate.player.width, worldstate.player.height):
                portal = random.choice(worldstate.objects)
                worldstate.player.x, worldstate.player.y = portal.x, portal.y + 35  # Teleport player to the other portal

        worldstate.objects.append(Object(portal_x, portal_y, draw_portal, update_portal))

# Summary:
# - Added add_teleport_portal: Introduces portals that teleport the player between locations.

import random

def add_blackhole_portal(worldstate):  # Introduces blackholes as portals affecting bullet trajectory
    if random.randint(0, 1000) < 3:  # 0.3% chance to generate a blackhole each frame
        portal_x = random.randint(0, SCREEN_WIDTH - 40)
        portal_y = random.randint(0, SCREEN_HEIGHT // 2)  # Ensure portal is in the upper half of the screen
        portal_speed = 1

        def draw_portal(obj, screen):
            pygame.draw.circle(screen, (0, 0, 0), (int(obj.x), int(obj.y)), 20)
            pygame.draw.circle(screen, (255, 0, 255), (int(obj.x), int(obj.y)), 15, 1)

        def update_portal(obj):
            obj.y += portal_speed
            if obj.y > SCREEN_HEIGHT:
                worldstate.objects.remove(obj)
            else:
                for bullet in worldstate.bullets:
                    if pygame.Rect(bullet.x, bullet.y, 10, 30).colliderect(obj.x - 20, obj.y - 20, 40, 40):
                        bullet.speed_y *= -1  # Reverse bullet's vertical speed

        worldstate.objects.append(Object(portal_x, portal_y, draw_portal, update_portal))

# Summary:
# - Added add_blackhole_portal: Creates blackholes that reverse bullet direction.

import random
import pygame

def add_time_warp_portal(worldstate):  # Adds a time warp portal that slows down enemies for a short duration
   if random.randint(0, 1000) < 5:  # Small chance to generate a portal
       portal_x = random.randint(0, SCREEN_WIDTH - 40)
       portal_y = random.randint(0, SCREEN_HEIGHT - 40)
       effect_duration = 200  # Frames

       def draw_portal(obj, screen):
           pygame.draw.ellipse(screen, (0, 0, 200), (obj.x, obj.y, 40, 40))

       def update_portal(obj):
           nonlocal effect_duration
           effect_duration -= 1
           if effect_duration == 0:
               worldstate.objects.remove(obj)  # Remove portal after effect duration
            
           for enemy in worldstate.enemies:
               enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
               portal_rect = pygame.Rect(obj.x, obj.y, 40, 40)
               if enemy_rect.colliderect(portal_rect):
                   enemy.speed *= 0.5  # Halve enemy speed
           
       worldstate.objects.append(Object(portal_x, portal_y, draw_portal, update_portal))

# Summary:
# - Added add_time_warp_portal: Introduces portals that temporarily slow down enemies.