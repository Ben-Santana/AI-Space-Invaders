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

import random
import pygame

def add_gravity_well(worldstate):  # Adds gravity wells that attract bullets
    if random.randint(0, 1000) < 5:  # 0.5% chance to generate a gravity well each frame
        well_x = random.randint(50, SCREEN_WIDTH - 50)
        well_y = random.randint(50, SCREEN_HEIGHT - 200)

        def draw_gravity_well(obj, screen):
            pygame.draw.circle(screen, (75, 0, 130), (int(obj.x), int(obj.y)), 30)  # Draw a purple well

        def update_gravity_well(obj):
            for bullet in worldstate.bullets:
                # Calculate the vector from the bullet to the gravity well
                dx = obj.x - bullet.x
                dy = obj.y - bullet.y
                distance = max(1, (dx**2 + dy**2) ** 0.5)  # Ensure no division by zero

                # Calculate the gravitational pull
                gravity_force = max(0.5, 120 / distance)  # stronger force closer to the well
                bullet.x += (dx / distance) * gravity_force  # Change bullet direction towards the well
                bullet.y += (dy / distance) * gravity_force

            if pygame.Rect(obj.x - 30, obj.y - 30, 60, 60).colliderect(worldstate.player.x, PLAYER_HEIGHT, worldstate.player.width, worldstate.player.height):
                worldstate.gameOver = True  # End game if player collides with the gravity well

        worldstate.objects.append(Object(well_x, well_y, draw_gravity_well, update_gravity_well))

# Summary:
# - Added add_gravity_well: Introduces gravity wells that attract bullets and threaten the player.

def add_moving_laser_beam(worldstate):  # Adds a moving laser beam that the player must avoid
    if random.randint(0, 1000) < 5:  # 0.5% chance to generate a laser beam each frame
        beam_x = random.randint(100, SCREEN_WIDTH - 100)
        beam_speed = random.choice([-3, 3])  # Travel left or right

        def draw_laser_beam(obj, screen):
            pygame.draw.rect(screen, RED, (obj.x, SCREEN_HEIGHT - 150, 10, 150))  # Draw a vertical laser beam

        def update_laser_beam(obj):
            obj.x += beam_speed
            if obj.x < 0 or obj.x > SCREEN_WIDTH - 10:
                worldstate.objects.remove(obj)  # Remove laser if it goes off-screen

            # Check collision with player
            if pygame.Rect(obj.x, SCREEN_HEIGHT - 150, 10, 150).colliderect(worldstate.player.x, PLAYER_HEIGHT, worldstate.player.width, worldstate.player.height):
                worldstate.gameOver = True  # End game if player collides with the laser beam

        worldstate.objects.append(Object(beam_x, SCREEN_HEIGHT - 150, draw_laser_beam, update_laser_beam))

# Summary:
# - Added add_moving_laser_beam: Introduces a moving laser beam as a new obstacle for the player.

import random
import pygame

def add_teleporting_mine(worldstate):  # Adds teleporting mines that appear and disappear
    if random.randint(0, 1000) < 5:  # 0.5% chance to generate a mine each frame
        mine_x = random.randint(50, SCREEN_WIDTH - 50)
        mine_y = random.randint(50, PLAYER_HEIGHT - 100)

        def draw_mine(obj, screen):
            pygame.draw.circle(screen, RED, (int(obj.x), int(obj.y)), 15)
            pygame.draw.line(screen, ORANGE, (int(obj.x) - 10, int(obj.y)), (int(obj.x) + 10, int(obj.y)), 3)
            pygame.draw.line(screen, ORANGE, (int(obj.x), int(obj.y) - 10), (int(obj.x), int(obj.y) + 10), 3)

        def update_mine(obj):
            if random.randint(0, 100) < 5:  # 5% chance each frame to teleport
                obj.x = random.randint(50, SCREEN_WIDTH - 50)
                obj.y = random.randint(50, PLAYER_HEIGHT - 100)
                
            if pygame.Rect(obj.x - 15, obj.y - 15, 30, 30).colliderect(worldstate.player.x, PLAYER_HEIGHT, worldstate.player.width, worldstate.player.height):
                worldstate.gameOver = True  # End game if player collides with the mine
                
        worldstate.objects.append(Object(mine_x, mine_y, draw_mine, update_mine))

# Summary:
# - Added add_teleporting_mine: Introduces teleporting mines as a dynamic obstacle.