import math
import pygame
import sys
import random
sys.path.append('../')
from game import WorldState, Object, Player, Boss, Enemy, Bullet, SCREEN_WIDTH, SCREEN_HEIGHT, clock, PLAYER_HEIGHT, BLACK, WHITE, BLUE, ORANGE, PURPLE, RED, GREEN


def add_power_up_portal(worldstate):  # Creates a portal that grants player a temporary shield
    if random.randint(0, 1000) < 3:  # 0.3% chance to generate a portal every frame
        portal_x = random.randint(0, SCREEN_WIDTH - 50)

        def draw_portal(obj, screen):
            pygame.draw.ellipse(screen, BLUE, (obj.x, obj.y, 50, 20))
            pygame.draw.arc(screen, ORANGE, (obj.x, obj.y, 50, 20), 0, math.pi*2, 5)

        def update_portal(obj):
            if pygame.Rect(obj.x, obj.y, 50, 20).colliderect(worldstate.player.x, PLAYER_HEIGHT, worldstate.player.width, worldstate.player.height):
                worldstate.player.shield_active = True  # Activate shield
                # Optionally: Start a timer to deactivate shield
                worldstate.objects.remove(obj)

        worldstate.objects.append(Object(portal_x, PLAYER_HEIGHT - 40, draw_portal, update_portal))

# Summary:
# - Added add_power_up_portal: Introduces a portal with a temporary shield effect for the player.