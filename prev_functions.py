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

import random

def add_moving_obstacle(worldstate):  # Introduces moving obstacles that block the player's bullets
    if random.randint(0, 1500) < 2:  # Small chance to generate a moving obstacle each frame
        obstacle_x = random.randint(20, SCREEN_WIDTH - 70)
        obstacle_y = PLAYER_HEIGHT - random.randint(100, 200)
        obstacle_speed = random.choice([-2, 2])  # Random horizontal direction

        def draw_obstacle(obj, screen):
            pygame.draw.rect(screen, (100, 100, 100), (obj.x, obj.y, obj.width, obj.height))

        def update_obstacle(obj):
            obj.x += obstacle_speed
            if obj.x < 20 or obj.x + obj.width > SCREEN_WIDTH - 20:
                obj.x -= obstacle_speed  # Reverse movement direction
                obj.speed = -obj.speed

            for bullet in worldstate.bullets:
                if (
                    bullet.x < obj.x + obj.width and
                    bullet.x + bullet.width > obj.x and
                    bullet.y < obj.y + obj.height and
                    bullet.y + bullet.height > obj.y
                ):
                    worldstate.bullets.remove(bullet)  # Destroy bullet upon collision with obstacle

            obj.timer -= 1
            if obj.timer <= 0:
                worldstate.objects.remove(obj)

        obstacle_obj = Object(obstacle_x, obstacle_y, draw_obstacle, update_obstacle)
        obstacle_obj.width = 50
        obstacle_obj.height = 10
        obstacle_obj.timer = 800  # Obstacle lasts for about 13 seconds
        worldstate.objects.append(obstacle_obj)

# Summary:
# - Added add_moving_obstacle: Introduces moving obstacles that block and destroy the player's bullets.

import random
import math

def add_black_hole(worldstate):  # Creates a black hole that pulls enemies and bullets towards it
    if random.randint(0, 2000) < 2:  # Small chance to generate a black hole each frame
        black_hole_x = random.randint(100, SCREEN_WIDTH - 100)
        black_hole_y = random.randint(100, SCREEN_HEIGHT - 200)

        def draw_black_hole(obj, screen):
            pygame.draw.circle(screen, BLACK, (int(obj.x), int(obj.y)), 20)

        def update_black_hole(obj):
            # Affect nearby enemies
            for enemy in worldstate.enemies:
                dx = obj.x - enemy.x
                dy = obj.y - enemy.y
                dist = math.hypot(dx, dy)
                if dist < 200:  # Pull enemies within a certain radius
                    force = min(5, 1500 / (dist**2))
                    angle = math.atan2(dy, dx)
                    enemy.x += math.cos(angle) * force
                    enemy.y += math.sin(angle) * force

            # Affect nearby bullets
            for bullet in worldstate.bullets[:]:
                dx = obj.x - bullet.x
                dy = obj.y - bullet.y
                dist = math.hypot(dx, dy)
                if dist < 200:  # Pull bullets within a certain radius
                    force = 1500 / (dist**2)
                    angle = math.atan2(dy, dx)
                    bullet.x += math.cos(angle) * force
                    bullet.y += math.sin(angle) * force

            obj.timer -= 1
            if obj.timer <= 0:
                worldstate.objects.remove(obj)

        black_hole_obj = Object(black_hole_x, black_hole_y, draw_black_hole, update_black_hole)
        black_hole_obj.timer = 1000  # Black hole lasts for about 16 seconds
        worldstate.objects.append(black_hole_obj)

# Summary:
# - Added add_black_hole: Creates a black hole pulling enemies and bullets towards it.

import random
import math

def add_meteor_shower(worldstate):  # Initiates a meteor shower that rains meteors down the screen
    if random.randint(0, 100) < 3:  # 3% chance to generate a meteor each frame
        meteor_x = random.randint(20, SCREEN_WIDTH - 50)
        meteor_speed = random.uniform(2, 5)

        def draw_meteor(obj, screen):
            pygame.draw.ellipse(screen, (150, 75, 0), (obj.x, obj.y, 30, 15))

        def update_meteor(obj):
            obj.y += meteor_speed
            if obj.y > SCREEN_HEIGHT:
                worldstate.objects.remove(obj)  # Remove meteor when out of the screen

            player_rect = pygame.Rect(worldstate.player.x, PLAYER_HEIGHT, worldstate.player.width, worldstate.player.height)
            meteor_rect = pygame.Rect(obj.x, obj.y, 30, 15)
            if meteor_rect.colliderect(player_rect):
                worldstate.player.x = SCREEN_WIDTH // 2 - worldstate.player.width // 2  # Reset player to initial position
                worldstate.score -= 50  # Deduct score for getting hit
                worldstate.objects.remove(obj)

        worldstate.objects.append(Object(meteor_x, 0, draw_meteor, update_meteor))

# Summary:
# - Added add_meteor_shower: Initiates meteors that deduct score and reset player on hit.

def add_wandering_mine(worldstate):  # Introduces a wandering mine that follows the player and can explode
    if random.randint(0, 2000) < 2:  # Small chance to generate a wandering mine each frame
        mine_x = random.randint(50, SCREEN_WIDTH - 50)
        mine_speed = 1.5

        def draw_mine(obj, screen):
            pygame.draw.circle(screen, (255, 50, 50), (int(obj.x), int(obj.y)), 15)

        def update_mine(obj): 
            # Make the mine slowly follow the player
            if worldstate.player.x > obj.x:
                obj.x += mine_speed
            elif worldstate.player.x < obj.x:
                obj.x -= mine_speed

            # Check collision with player
            player_rect = pygame.Rect(worldstate.player.x, PLAYER_HEIGHT, worldstate.player.width, worldstate.player.height)
            mine_rect = pygame.Rect(obj.x - 15, obj.y - 15, 30, 30)
            if mine_rect.colliderect(player_rect):
                # Mine explodes on collision with player and deducts score
                worldstate.score -= 100
                worldstate.objects.remove(obj)
                # For changes besides score, add visual effects or sounds if needed

            # Destroy the mine if it goes off screen
            if obj.y > SCREEN_HEIGHT:
                worldstate.objects.remove(obj)

        mine_obj = Object(mine_x, PLAYER_HEIGHT - 100, draw_mine, update_mine)
        worldstate.objects.append(mine_obj)

# Summary:
# - Added add_wandering_mine: Introduces a mine that follows and can explode on the player.

import random

def add_homing_missile(worldstate):  # Introduces homing missiles that target and chase down enemies
    if random.randint(0, 1500) < 2:  # Small chance to spawn a homing missile
        missile_x = worldstate.player.x + worldstate.player.width // 2
        missile_y = PLAYER_HEIGHT
        missile_speed = 5

        def draw_missile(obj, screen):
            pygame.draw.polygon(screen, RED, [(obj.x, obj.y), (obj.x - 5, obj.y + 15), (obj.x + 5, obj.y + 15)])

        def update_missile(obj):
            # Move missile towards the nearest enemy
            if worldstate.enemies:
                target = min(worldstate.enemies, key=lambda e: math.hypot(e.x - obj.x, e.y - obj.y))
                dx = target.x + target.width // 2 - obj.x
                dy = target.y + target.height // 2 - obj.y
                dist = math.hypot(dx, dy)
                if dist != 0:  # Avoid division by zero
                    obj.x += missile_speed * dx / dist
                    obj.y += missile_speed * dy / dist

                missile_rect = pygame.Rect(obj.x - 5, obj.y, 10, 15)
                target_rect = pygame.Rect(target.x, target.y, target.width, target.height)
                if missile_rect.colliderect(target_rect):
                    worldstate.enemies.remove(target)
                    worldstate.score += 20
                    worldstate.objects.remove(obj)

            if obj.y < 0:
                worldstate.objects.remove(obj)

        missile_obj = Object(missile_x, missile_y, draw_missile, update_missile)
        worldstate.objects.append(missile_obj)

# Summary:
# - Added add_homing_missile: Introduces homing missiles that target and chase down enemies.

import random

def deploy_decoy(worldstate):  # Deploys a decoy that temporarily distracts enemies
    if random.randint(0, 1500) < 2:  # Small chance to deploy a decoy each frame
        decoy_x = random.randint(20, SCREEN_WIDTH - worldstate.player.width - 20)

        def draw_decoy(obj, screen):
            pygame.draw.rect(screen, TEAL, (obj.x, PLAYER_HEIGHT - 50, worldstate.player.width, worldstate.player.height))

        def update_decoy(obj):
            # Make enemies attracted to the decoy instead of the player
            for enemy in worldstate.enemies:
                if abs(enemy.x - obj.x) > 5:  # Only adjust enemy position if they're far from the decoy
                    enemy_direction = 1 if enemy.x < obj.x else -1
                    enemy.x += enemy.speed * enemy_direction

                # Check collision with enemies
                if pygame.Rect(obj.x, PLAYER_HEIGHT - 50, worldstate.player.width, worldstate.player.height).colliderect(
                    pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)):
                    worldstate.enemies.remove(enemy)
                    worldstate.score += 5  # Give slight score bonus for each enemy distracted

            obj.timer -= 1
            if obj.timer <= 0:  # Decoy disappears after a certain time
                worldstate.objects.remove(obj)

        decoy_obj = Object(decoy_x, PLAYER_HEIGHT - 50, draw_decoy, update_decoy)
        decoy_obj.timer = 500  # Decoy lasts for about 8 seconds
        worldstate.objects.append(decoy_obj)

# Summary:
# - Added deploy_decoy: Deploys a decoy that distracts enemies and earns small score bonuses.

import random
import math

def add_vortex_trap(worldstate):  # Introduces a vortex trap that pulls enemies and objects and destroys them
    if random.randint(0, 2000) < 2:  # Small chance to create a vortex trap each frame
        vortex_x = random.randint(100, SCREEN_WIDTH - 100)
        vortex_y = random.randint(100, SCREEN_HEIGHT - 200)

        def draw_vortex(obj, screen):
            pygame.draw.circle(screen, (50, 50, 255), (int(obj.x), int(obj.y)), 20, 3)

        def update_vortex(obj):
            # Affect nearby enemies
            for enemy in worldstate.enemies[:]:
                dx = obj.x - enemy.x
                dy = obj.y - enemy.y
                dist = math.hypot(dx, dy)
                if dist < 150:  # Pull and destroy enemies within a certain radius
                    force = min(6, 1000 / (dist**2))
                    angle = math.atan2(dy, dx)
                    enemy.x += math.cos(angle) * force
                    enemy.y += math.sin(angle) * force
                    if dist < 30:  # Destroy enemy when very close
                        worldstate.enemies.remove(enemy)
                        worldstate.score += 20

            # Affect nearby objects
            for obj_item in worldstate.objects[:]:
                dx = obj.x - obj_item.x
                dy = obj.y - obj_item.y
                dist = math.hypot(dx, dy)
                if dist < 150:  # Pull and destroy objects within a certain radius
                    force = min(4, 800 / (dist**2))
                    angle = math.atan2(dy, dx)
                    obj_item.x += math.cos(angle) * force
                    obj_item.y += math.sin(angle) * force
                    if dist < 20:  # Destroy object when very close
                        worldstate.objects.remove(obj_item)

            obj.timer -= 1
            if obj.timer <= 0:
                worldstate.objects.remove(obj)

        vortex_obj = Object(vortex_x, vortex_y, draw_vortex, update_vortex)
        vortex_obj.timer = 1000  # Vortex lasts for about 16 seconds
        worldstate.objects.append(vortex_obj)

# Summary:
# - Added add_vortex_trap: Introduces a vortex that pulls and destroys enemies and objects.

import random

def add_laser_beam(worldstate):  # Introduces a vertical laser beam that damages enemies
    if random.randint(0, 1000) < 2:  # Small chance to generate a laser beam each frame
        laser_x = random.randint(20, SCREEN_WIDTH - 20)
        laser_duration = 180  # Laser lasts for about 3 seconds
        cooldown_time = 600  # Cooldown before next laser can appear
        end_cooldown_after_trigger = 0

        def draw_laser(obj, screen):
            pygame.draw.line(screen, GREEN, (obj.x, 0), (obj.x, SCREEN_HEIGHT), 5)

        def update_laser(obj):
            for enemy in worldstate.enemies[:]:
                enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
                laser_rect = pygame.Rect(obj.x, 0, 5, SCREEN_HEIGHT)
                if enemy_rect.colliderect(laser_rect):
                    worldstate.enemies.remove(enemy)
                    worldstate.score += 10

            obj.timer -= 1
            if obj.timer <= 0:
                worldstate.objects.remove(obj)

        if end_cooldown_after_trigger <= 0:
            laser_obj = Object(laser_x, 0, draw_laser, update_laser)
            laser_obj.timer = laser_duration
            worldstate.objects.append(laser_obj)
            end_cooldown_after_trigger = cooldown_time

        end_cooldown_after_trigger -= 1

# Summary:
# - Added add_laser_beam: Introduces a vertical laser beam that damages enemies.

import random
import pygame

def deploy_shield_drone(worldstate):  # Introduces a shield drone that temporarily protects the player from enemy bullets
    if random.randint(0, 1500) < 2:  # Small chance to deploy a shield drone
        drone_x = worldstate.player.x + worldstate.player.width // 2
        drone_y = PLAYER_HEIGHT

        def draw_drone(obj, screen):
            pygame.draw.circle(screen, GREEN, (int(obj.x), int(obj.y)), 15)
            pygame.draw.circle(screen, WHITE, (int(obj.x), int(obj.y)), 20, 2)

        def update_drone(obj):
            obj.x = worldstate.player.x + worldstate.player.width // 2
            player_rect = pygame.Rect(worldstate.player.x, PLAYER_HEIGHT, worldstate.player.width, worldstate.player.height)

            for bullet in worldstate.bullets[:]:
                bullet_rect = pygame.Rect(bullet.x, bullet.y, bullet.width, bullet.height)
                if bullet_rect.colliderect(player_rect):
                    worldstate.bullets.remove(bullet)  # Destroy enemy bullet before reaching the player

            obj.timer -= 1
            if obj.timer <= 0:
                worldstate.objects.remove(obj)

        drone_obj = Object(drone_x, drone_y, draw_drone, update_drone)
        drone_obj.timer = 500  # The shield lasts for about 8 seconds
        worldstate.objects.append(drone_obj)

# Summary:
# - Added deploy_shield_drone: Introduces a shield drone to protect the player from enemy bullets.

import random

def add_slow_motion_zone(worldstate):  # Introduces a zone that slows down all entities inside it
    if random.randint(0, 1500) < 2:  # Small chance to create a slow motion zone
        zone_x = random.randint(100, SCREEN_WIDTH - 100)
        zone_y = random.randint(100, SCREEN_HEIGHT - 200)

        def draw_slow_motion_zone(obj, screen):
            pygame.draw.circle(screen, (0, 150, 200), (int(obj.x), int(obj.y)), 50, 5)

        def update_slow_motion_zone(obj):
            for enemy in worldstate.enemies:
                if math.hypot(obj.x - enemy.x, obj.y - enemy.y) < 50:
                    enemy.speed = max(0.5, enemy.speed - 0.1)

            for bullet in worldstate.bullets:
                if math.hypot(obj.x - bullet.x, obj.y - bullet.y) < 50:
                    bullet.dy = max(1, bullet.dy + 0.5)

            obj.timer -= 1
            if obj.timer <= 0:
                worldstate.objects.remove(obj)

        slow_motion_zone_obj = Object(zone_x, zone_y, draw_slow_motion_zone, update_slow_motion_zone)
        slow_motion_zone_obj.timer = 600  # Zone lasts for about 10 seconds
        worldstate.objects.append(slow_motion_zone_obj)

# Summary:
# - Added add_slow_motion_zone: Introduces a zone that slows down entities inside it.

import random

def add_bouncing_bomb(worldstate):  # Introduces a bomb that bounces around and explodes near enemies
    if random.randint(0, 1500) < 2:  # Small chance to spawn a bouncing bomb
        bomb_x = random.randint(50, SCREEN_WIDTH - 50)
        bomb_y = random.randint(50, SCREEN_HEIGHT - 200)
        bomb_speed_x = random.choice([-3, 3])
        bomb_speed_y = random.choice([-3, 3])
        bomb_radius = 10

        def draw_bomb(obj, screen):
            pygame.draw.circle(screen, ORANGE, (int(obj.x), int(obj.y)), bomb_radius)

        def update_bomb(obj):
            obj.x += bomb_speed_x
            obj.y += bomb_speed_y
            
            # Reverse direction on screen edge collision
            if obj.x - bomb_radius < 0 or obj.x + bomb_radius > SCREEN_WIDTH:
                obj.x -= bomb_speed_x
                obj.speed_x = -obj.speed_x
            if obj.y - bomb_radius < 0 or obj.y + bomb_radius > SCREEN_HEIGHT:
                obj.y -= bomb_speed_y
                obj.speed_y = -obj.speed_y

            for enemy in worldstate.enemies[:]:
                if math.hypot(obj.x - enemy.x, obj.y - enemy.y) < 50:  # Explode near an enemy
                    worldstate.enemies.remove(enemy)
                    obj.explode()

            obj.timer -= 1
            if obj.timer <= 0:
                worldstate.objects.remove(obj)

        bomb_obj = Object(bomb_x, bomb_y, draw_bomb, update_bomb)
        bomb_obj.timer = 600  # Bomb lasts for about 10 seconds
        worldstate.objects.append(bomb_obj)

# Summary:
# - Added add_bouncing_bomb: Introduces a bomb that bounces and explodes near enemies.

import random
import math

def create_shockwave(worldstate):  # Introduces a shockwave that radiates from a point and disrupts enemies
    if random.randint(0, 1500) < 2:  # Small chance to create a shockwave each frame
        shockwave_x = random.randint(100, SCREEN_WIDTH - 100)
        shockwave_radius = 10
        max_radius = 150
        shockwave_speed = 2

        def draw_shockwave(obj, screen):
            pygame.draw.circle(screen, (200, 200, 0), (int(obj.x), int(SCREEN_HEIGHT // 2)), obj.radius, 3)

        def update_shockwave(obj):
            obj.radius += shockwave_speed
            if obj.radius >= max_radius:
                worldstate.objects.remove(obj)

            # Push away all enemies within the shockwave radius
            for enemy in worldstate.enemies[:]:
                dx = enemy.x + enemy.width // 2 - obj.x
                dy = enemy.y + enemy.height // 2 - (SCREEN_HEIGHT // 2)
                if math.hypot(dx, dy) < obj.radius:
                    angle = math.atan2(dy, dx)
                    enemy.x += math.cos(angle) * 5
                    enemy.y += math.sin(angle) * 5

        shockwave_obj = Object(shockwave_x, SCREEN_HEIGHT // 2, draw_shockwave, update_shockwave)
        shockwave_obj.radius = shockwave_radius
        worldstate.objects.append(shockwave_obj)

# Summary:
# - Added create_shockwave: Introduces a shockwave that pushes enemies outward.

import random

def add_fireball_barrage(worldstate):  # Sends a barrage of fireballs across the screen at random intervals
    if random.randint(0, 2000) < 3:  # Small chance to trigger a fireball barrage
        for _ in range(random.randint(2, 5)):  # Launch 2-5 fireballs in one barrage
            fireball_x = random.randint(20, SCREEN_WIDTH - 50)
            fireball_speed = random.uniform(2, 4)
            fireball_dy = random.choice([-1, 1]) * random.uniform(1, 3)
            fireball_radius = random.randint(10, 20)

            def draw_fireball(obj, screen):
                pygame.draw.ellipse(screen, RED, (obj.x, obj.y, fireball_radius, fireball_radius))

            def update_fireball(obj):
                obj.x += fireball_speed
                obj.y += fireball_dy
                if obj.x < 20 or obj.x > SCREEN_WIDTH - 20:
                    worldstate.objects.remove(obj)  # Remove fireball off screen
                
                # Check collision with player
                player_rect = pygame.Rect(worldstate.player.x, PLAYER_HEIGHT, worldstate.player.width, worldstate.player.height)
                fireball_rect = pygame.Rect(obj.x, obj.y, fireball_radius, fireball_radius)
                if fireball_rect.colliderect(player_rect):
                    worldstate.score -= 20  # Deduct player's score on hit
                    worldstate.objects.remove(obj)
                
            fireball_obj = Object(fireball_x, 0, draw_fireball, update_fireball)
            worldstate.objects.append(fireball_obj)

# Summary:
# - Added add_fireball_barrage: Randomly launches fireballs that can hit the player.

import random
import math

def activate_fog_of_war(worldstate):  # Introduces a fog effect that reduces visibility, hiding enemies
    if random.randint(0, 1500) < 2:  # Small chance to activate fog of war each frame
        fog_intensity = random.choice([100, 150, 200])

        def draw_fog(obj, screen):
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(fog_intensity)  
            overlay.fill((50, 50, 50))  # Gray fog color
            screen.blit(overlay, (0, 0))

        def update_fog(obj):
            obj.timer -= 1
            if obj.timer <= 0:
                worldstate.objects.remove(obj)

        fog_obj = Object(0, 0, draw_fog, update_fog)
        fog_obj.timer = 600  # Fog lasts for about 10 seconds
        worldstate.objects.append(fog_obj)

# Summary:
# - Added activate_fog_of_war: Introduces fog that reduces visibility and hides enemies.

import random
import math

def deploy_orbital_strike(worldstate):  # Deploys an orbital strike that targets random areas
    if random.randint(0, 1500) < 2:  # Small chance to trigger an orbital strike
        strike_x = random.randint(50, SCREEN_WIDTH - 50)
        strike_y = random.randint(50, SCREEN_HEIGHT - 200)
        strike_radius = 30
        strike_duration = 100  # Strike effect lasts briefly

        def draw_strike(obj, screen):
            pygame.draw.circle(screen, TEAL, (int(obj.x), int(obj.y)), int(obj.radius), 1)

        def update_strike(obj):
            if obj.timer > (strike_duration - 50):  # During the first half, increase radius
                obj.radius += 5
            else:  # On second half, check if enemies are within the area
                for enemy in worldstate.enemies[:]:
                    if math.hypot(enemy.x - obj.x, enemy.y - obj.y) < obj.radius:
                        worldstate.enemies.remove(enemy)
                        worldstate.score += 20

            obj.timer -= 1
            if obj.timer <= 0:
                worldstate.objects.remove(obj)

        strike_obj = Object(strike_x, strike_y, draw_strike, update_strike)
        strike_obj.radius = 0
        strike_obj.timer = strike_duration
        worldstate.objects.append(strike_obj)

# Summary:
# - Added deploy_orbital_strike: Deploys a strike targeting random areas, increasing in size.

import random

def add_energy_wave(worldstate):  # Emits an energy wave that disrupts the enemies' directions
    if random.randint(0, 2000) < 2:  # Small chance to emit an energy wave each frame
        wave_x = random.randint(100, SCREEN_WIDTH - 100)
        wave_y = random.randint(50, 300)
        wave_speed = 3
        wave_radius = 30
        max_radius = 200

        def draw_wave(obj, screen):
            pygame.draw.circle(screen, (255, 255, 0), (int(obj.x), int(obj.y)), int(obj.radius), 2)

        def update_wave(obj):
            obj.radius += wave_speed
            if obj.radius >= max_radius:
                worldstate.objects.remove(obj)
                return

            # Reverse the direction of any enemy caught in the wave
            for enemy in worldstate.enemies:
                dx = enemy.x + enemy.width // 2 - obj.x
                dy = enemy.y + enemy.height // 2 - obj.y
                if math.hypot(dx, dy) < obj.radius:
                    enemy.direction *= -1

        wave_obj = Object(wave_x, wave_y, draw_wave, update_wave)
        wave_obj.radius = wave_radius
        worldstate.objects.append(wave_obj)

# Summary:
# - Added add_energy_wave: Emits an energy wave that reverses the direction of nearby enemies.

import random

def deploy_time_freeze(worldstate):  # Temporarily freezes all enemy movements and bullet trajectories
    if random.randint(0, 1500) < 2:  # Small chance to initiate a time freeze each frame
        freeze_duration = 300  # Time freeze effect lasts for 5 seconds

        def draw_freeze_effect(obj, screen):
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)  # Slightly transparent
            overlay.fill((0, 255, 255))  # Cyan freeze effect
            screen.blit(overlay, (0, 0))

        def update_freeze_effect(obj):
            for enemy in worldstate.enemies:
                enemy.frozen_speed = enemy.speed  # Save current speed
                enemy.speed = 0  # Freeze enemy movement

            for bullet in worldstate.bullets:
                bullet.frozen_dy = bullet.dy  # Save current bullet speed
                bullet.dy = 0  # Freeze bullet movement

            obj.timer -= 1
            if obj.timer <= 0:
                for enemy in worldstate.enemies:
                    enemy.speed = enemy.frozen_speed  # Restore enemy speed
                for bullet in worldstate.bullets:
                    bullet.dy = bullet.frozen_dy  # Restore bullet speed
                worldstate.objects.remove(obj)

        freeze_obj = Object(0, 0, draw_freeze_effect, update_freeze_effect)
        freeze_obj.timer = freeze_duration
        worldstate.objects.append(freeze_obj)

# Summary:
# - Added deploy_time_freeze: Temporarily halts all enemy and bullet movements.

import random
import pygame

def add_lightning_storm(worldstate):  # Introduces a random lightning storm that strikes enemies
    if random.randint(0, 1500) < 2:  # Small chance to trigger a lightning storm
        lightning_duration = 180  # Duration of the storm
        strikes_count = random.randint(3, 8)  # Random number of strikes

        def draw_lightning(obj, screen):
            for _ in range(strikes_count):
                strike_x = random.randint(20, SCREEN_WIDTH - 20)
                pygame.draw.line(screen, (255, 255, 0), (strike_x, 0), (strike_x, SCREEN_HEIGHT), 3)

        def update_lightning(obj):
            for enemy in worldstate.enemies[:]:
                for _ in range(strikes_count): 
                    if pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height).colliderect(
                        pygame.Rect(random.randint(20, SCREEN_WIDTH - 20), 0, 3, SCREEN_HEIGHT)):
                        worldstate.enemies.remove(enemy)
                        worldstate.score += 10

            obj.timer -= 1
            if obj.timer <= 0:
                worldstate.objects.remove(obj)

        lightning_obj = Object(0, 0, draw_lightning, update_lightning)
        lightning_obj.timer = lightning_duration
        worldstate.objects.append(lightning_obj)

# Summary:
# - Added add_lightning_storm: Introduces a storm with random lightning strikes damaging enemies.

import random
import math

def deploy_magnetic_field(worldstate):  # Creates a magnetic field that attracts player bullets toward enemies
    if random.randint(0, 1500) < 2:  # Small chance to generate a magnetic field each frame
        field_x = random.randint(100, SCREEN_WIDTH - 100)
        field_y = random.randint(100, SCREEN_HEIGHT - 200)
        field_radius = 150

        def draw_magnetic_field(obj, screen):
            pygame.draw.circle(screen, (0, 100, 255), (int(obj.x), int(obj.y)), field_radius, 3)

        def update_magnetic_field(obj):
            for bullet in worldstate.bullets:
                if bullet.dy < 0:  # Only affect player's bullets moving upwards
                    dx = obj.x - bullet.x
                    dy = obj.y - bullet.y
                    dist = math.hypot(dx, dy)
                    if dist < field_radius:  # Attract bullets within a certain radius
                        attraction_strength = max(1, field_radius - dist) / 10
                        angle = math.atan2(dy, dx)
                        bullet.x += math.cos(angle) * attraction_strength
                        bullet.y += math.sin(angle) * attraction_strength

            obj.timer -= 1
            if obj.timer <= 0:
                worldstate.objects.remove(obj)

        magnetic_field_obj = Object(field_x, field_y, draw_magnetic_field, update_magnetic_field)
        magnetic_field_obj.timer = 800  # Magnetic field lasts for about 13 seconds
        worldstate.objects.append(magnetic_field_obj)

# Summary:
# - Added deploy_magnetic_field: Attracts player bullets toward enemies within a magnetic field.

import random
import pygame

def add_enemy_squadron(worldstate):  # Introduces a squadron of enemies that fly in formation
    if random.randint(0, 1500) < 2:  # Small chance to spawn a squadron each frame
        formation_start_x = random.randint(50, SCREEN_WIDTH - 250)
        formation_y = -40
        formation_speed = 2

        def draw_squadron_member(obj, screen):
            pygame.draw.rect(screen, (255, 0, 0), (obj.x, obj.y, obj.width, obj.height))

        def update_squadron_member(obj):
            # Move the squadron in a zigzag pattern
            obj.x += formation_speed * obj.direction
            obj.y += 1
            if obj.x < 20 or obj.x > SCREEN_WIDTH - obj.width - 20:
                obj.direction *= -1
                obj.x += formation_speed * obj.direction

            # Check if squadron member reaches the bottom of the screen
            if obj.y > SCREEN_HEIGHT:
                worldstate.objects.remove(obj)

        squadron = []
        for i in range(5):  # Create a formation of 5 enemies
            member_x = formation_start_x + i * 50
            squadron_member = Object(member_x, formation_y, draw_squadron_member, update_squadron_member)
            squadron_member.width = 40
            squadron_member.height = 30
            squadron_member.direction = 1 if i % 2 == 0 else -1  # Alternate initial directions for zigzag
            worldstate.objects.append(squadron_member)
            squadron.append(squadron_member)

        # Remove the entire squadron if one member is hit
        def remove_squadron():
            for member in squadron:
                if member in worldstate.objects:
                    worldstate.objects.remove(member)

        for member in squadron:
            member.remove_squadron = remove_squadron

# Summary:
# - Added add_enemy_squadron: Introduces a squad of enemies that fly in a pattern.

import random
import pygame

def add_shadow_cloak(worldstate):  # Introduces a shadow cloak power-up that temporarily makes the player invisible to enemies
    if random.randint(0, 1500) < 2:  # Small chance to generate a shadow cloak each frame
        cloak_x = random.randint(20, SCREEN_WIDTH - 20)
        cloak_speed = random.uniform(1, 3)

        def draw_cloak(obj, screen):
            pygame.draw.circle(screen, (50, 50, 50), (obj.x, obj.y), 10, 1)

        def update_cloak(obj):
            obj.y += cloak_speed
            if obj.y > SCREEN_HEIGHT:
                worldstate.objects.remove(obj)  # Remove cloak when out of screen
            
            player_rect = pygame.Rect(worldstate.player.x, PLAYER_HEIGHT, worldstate.player.width, worldstate.player.height)
            cloak_rect = pygame.Rect(obj.x - 10, obj.y - 10, 20, 20)
            if cloak_rect.colliderect(player_rect):
                # Make player invisible to enemies for a short time
                worldstate.player.invisible_timer = 300  # Invisible for about 5 seconds
                worldstate.objects.remove(obj)

        worldstate.objects.append(Object(cloak_x, 0, draw_cloak, update_cloak))

    # Process invisibility effect
    if hasattr(worldstate.player, 'invisible_timer') and worldstate.player.invisible_timer > 0:
        worldstate.player.invisible_timer -= 1
        for enemy in worldstate.enemies:
            # Enemies don't target the player when invisible
            enemy.x += enemy.speed * enemy.direction * random.choice([-1, 1])
    else:
        # Remove the invisibility attribute if the effect ends
        if hasattr(worldstate.player, 'invisible_timer'):
            del worldstate.player.invisible_timer

# Summary:
# - Added add_shadow_cloak: Gives player temporary invisibility, bypassing enemies.

import random
import math

def deploy_tether_mine(worldstate):  # Introduces a tether mine that links two points with a damaging beam
    if random.randint(0, 1500) < 2:  # Small chance to deploy a tether mine
        tether_x1 = random.randint(50, SCREEN_WIDTH - 50)
        tether_y = random.randint(50, SCREEN_HEIGHT - 200)
        tether_x2 = tether_x1 + random.randint(100, 200)
        tether_timer = 500  # Lasts about 8 seconds

        def draw_tether(obj, screen):
            pygame.draw.line(screen, (255, 0, 0), (obj.x, obj.y), (obj.x2, obj.y), 3)

        def update_tether(obj):
            beam_rect = pygame.Rect(min(obj.x, obj.x2), obj.y - 3, abs(obj.x2 - obj.x), 6)

            for enemy in worldstate.enemies[:]:
                enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
                if enemy_rect.colliderect(beam_rect):
                    worldstate.enemies.remove(enemy)
                    worldstate.score += 10

            obj.timer -= 1
            if obj.timer <= 0:
                worldstate.objects.remove(obj)

        tether_obj = Object(tether_x1, tether_y, draw_tether, update_tether)
        tether_obj.x2 = tether_x2
        tether_obj.timer = tether_timer
        worldstate.objects.append(tether_obj)

# Summary:
# - Added deploy_tether_mine: Places a damaging beam between two tether points.

import random
import math

def add_bounce_shield(worldstate):  # Introduces a shield that reflects the player's bullets in a random direction
    if random.randint(0, 1500) < 2:  # Small chance to generate a bounce shield
        shield_x = random.randint(50, SCREEN_WIDTH - 50)
        shield_y = random.randint(50, SCREEN_HEIGHT - 150)
        shield_radius = 25

        def draw_bounce_shield(obj, screen):
            pygame.draw.circle(screen, (255, 215, 0), (int(obj.x), int(obj.y)), shield_radius, 2)

        def update_bounce_shield(obj):
            for bullet in worldstate.bullets[:]:
                if math.hypot(obj.x - bullet.x, obj.y - bullet.y) <= shield_radius + bullet.width/2:
                    # Calculate a new random direction for the bullet
                    angle = random.uniform(0, 2 * math.pi)
                    speed = math.hypot(bullet.dy, bullet.dy)
                    bullet.dx = speed * math.cos(angle)
                    bullet.dy = speed * math.sin(angle)
                    
                    # Ensure the bullet's trajectory is more horizontal
                    bullet.dy = min(-1, bullet.dy)

            obj.timer -= 1
            if obj.timer <= 0:
                worldstate.objects.remove(obj)

        bounce_shield_obj = Object(shield_x, shield_y, draw_bounce_shield, update_bounce_shield)
        bounce_shield_obj.timer = 800  # Bounce shield lasts for about 13 seconds
        worldstate.objects.append(bounce_shield_obj)

# Summary:
# - Added add_bounce_shield: Introduces a shield that reflects player bullets in a random direction.

def summon_ally_drone(worldstate):  # Summons an ally drone that shoots enemies for a duration
    if random.randint(0, 1500) < 2:  # Small chance to summon an ally drone each frame
        drone_x = worldstate.player.x
        drone_y = PLAYER_HEIGHT - 60
        shoot_interval = 60  # Drone shoots every second

        def draw_drone(obj, screen):
            pygame.draw.rect(screen, GREEN, (obj.x, obj.y, 20, 20))
            pygame.draw.rect(screen, BLACK, (obj.x + 5, obj.y + 5, 10, 10))

        def update_drone(obj):
            obj.timer -= 1
            if obj.timer % shoot_interval == 0:
                if worldstate.enemies:
                    target = random.choice(worldstate.enemies)
                    bullet = Bullet(obj.x + 10, obj.y, -5)
                    worldstate.bullets.append(bullet)
                    # Adjust bullet trajectory
                    dx = target.x - obj.x
                    dy = target.y - obj.y
                    dist = math.hypot(dx, dy)
                    bullet.dx = dx / dist * 5
                    bullet.dy = dy / dist * 5

            if obj.timer <= 0:
                worldstate.objects.remove(obj)

        drone_obj = Object(drone_x, drone_y, draw_drone, update_drone)
        drone_obj.timer = 600  # Drone lasts for 10 seconds
        worldstate.objects.append(drone_obj)

# Summary:
# - Added summon_ally_drone: Allies assist by shooting enemies for a limited time.

import random
import math

def add_tornado_effect(worldstate):  # Sends a tornado across the screen that disrupts enemies
    if random.randint(0, 1500) < 2:  # Small chance to create a tornado effect each frame
        tornado_x = random.choice([-50, SCREEN_WIDTH + 50])  # Start outside the screen
        tornado_speed = 5 if tornado_x < 0 else -5

        def draw_tornado(obj, screen):
            pygame.draw.ellipse(screen, (150, 150, 150), (obj.x, obj.y, 30, 60))

        def update_tornado(obj):
            obj.x += tornado_speed
            # Affect nearby enemies
            for enemy in worldstate.enemies[:]:
                if abs(obj.x + 15 - (enemy.x + enemy.width // 2)) < 60 and abs(obj.y + 30 - (enemy.y + enemy.height // 2)) < 30:
                    force = random.uniform(-5, 5)
                    enemy.x += force
                    enemy.y += abs(force)

            if obj.x < -70 or obj.x > SCREEN_WIDTH + 70:  # Remove after passing off-screen
                worldstate.objects.remove(obj)

        tornado_obj = Object(tornado_x, random.randint(100, SCREEN_HEIGHT - 100), draw_tornado, update_tornado)
        worldstate.objects.append(tornado_obj)

# Summary:
# - Added add_tornado_effect: Sends a tornado that disrupts enemies with random motion.


def generate_acid_rain(worldstate):  # Initiates an acid rain that slowly damages all enemies over time
    if random.randint(0, 1500) < 2:  # Small chance to trigger acid rain
        rain_duration = 600  # Acid rain lasts for about 10 seconds
        damage_frequency = 60  # Apply damage every second

        def draw_acid_rain(obj, screen):
            pygame.draw.rect(screen, (0, 150, 0), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 1)
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 255, 0, 50))  # Translucent green overlay
            screen.blit(overlay, (0, 0))

        def update_acid_rain(obj):
            obj.timer -= 1
            if obj.timer % damage_frequency == 0:
                for enemy in worldstate.enemies:
                    worldstate.score += 1  # Increment score for each enemy damaged
                    # Applying damage over time logic
                    if hasattr(enemy, 'acid_damage'): 
                        enemy.acid_damage += 1
                    else:
                        enemy.acid_damage = 1
                    if enemy.acid_damage >= 5:  # After 5 damage, remove enemy
                        worldstate.enemies.remove(enemy)

            if obj.timer <= 0:
                worldstate.objects.remove(obj)

        acid_rain_obj = Object(0, 0, draw_acid_rain, update_acid_rain)
        acid_rain_obj.timer = rain_duration
        worldstate.objects.append(acid_rain_obj)

# Summary:
# - Added generate_acid_rain: Initiates acid rain that damages enemies over time.

import random
import pygame

def deploy_celestial_barrier(worldstate):  # Deploys a celestial barrier that slows down and damages enemies
    if random.randint(0, 2000) < 3:  # Small chance to create a celestial barrier
        barrier_x = random.randint(50, SCREEN_WIDTH - 50)
        barrier_y = random.randint(50, SCREEN_HEIGHT - 150)
        barrier_radius = 60
        slow_duration = 600  # Barrier effect lasts for about 10 seconds

        def draw_barrier(obj, screen):
            pygame.draw.circle(screen, (0, 255, 150), (int(obj.x), int(obj.y)), barrier_radius, 3)

        def update_barrier(obj):
            for enemy in worldstate.enemies[:]:
                dx = obj.x - enemy.x
                dy = obj.y - enemy.y
                dist = math.hypot(dx, dy)
                if dist < barrier_radius:
                    enemy.speed = max(0.5, enemy.speed - 0.05)  # Slow down enemy within radius
                    worldstate.score += 1  # Optionally, increase score for each affected enemy

            obj.timer -= 1
            if obj.timer <= 0:
                worldstate.objects.remove(obj)

        barrier_obj = Object(barrier_x, barrier_y, draw_barrier, update_barrier)
        barrier_obj.timer = slow_duration
        worldstate.objects.append(barrier_obj)

# Summary:
# - Added deploy_celestial_barrier: Deploys a barrier that slows down and damages enemies over time.

import random
import pygame

def invoke_cosmic_explosion(worldstate):  # Triggers a cosmic explosion that disrupts enemies' formations
    if random.randint(0, 1500) < 2:  # Small chance to trigger a cosmic explosion
        explosion_x = random.randint(100, SCREEN_WIDTH - 100)
        explosion_y = random.randint(100, SCREEN_HEIGHT - 200)
        explosion_radius = 10
        max_radius = 120
        expansion_speed = 5

        def draw_explosion(obj, screen):
            pygame.draw.circle(screen, (255, 69, 0), (int(obj.x), int(obj.y)), int(obj.radius), 2)

        def update_explosion(obj):
            obj.radius += expansion_speed
            if obj.radius >= max_radius:
                worldstate.objects.remove(obj)
                return

            # Push away enemies within the explosion radius
            for enemy in worldstate.enemies:
                dx = enemy.x + enemy.width // 2 - obj.x
                dy = enemy.y + enemy.height // 2 - obj.y
                dist = math.hypot(dx, dy)
                if dist < obj.radius:
                    angle = math.atan2(dy, dx)
                    enemy.x += math.cos(angle) * 8
                    enemy.y += math.sin(angle) * 8

        explosion_obj = Object(explosion_x, explosion_y, draw_explosion, update_explosion)
        explosion_obj.radius = explosion_radius
        worldstate.objects.append(explosion_obj)

# Summary:
# - Added invoke_cosmic_explosion: Creates an explosion to disrupt enemy formations.

import random
import math

def add_asteroid_belt(worldstate):  # Creates an asteroid belt that introduces moving hazards
    if random.randint(0, 1500) < 3:  # Small chance to generate an asteroid belt each frame
        belt_y = random.randint(150, SCREEN_HEIGHT - 150)
        belt_speed = random.uniform(1, 3)
        asteroid_count = random.randint(3, 6)  # Random number of asteroids in the belt

        for _ in range(asteroid_count):
            asteroid_x = random.randint(20, SCREEN_WIDTH - 20)
            direction = random.choice([-1, 1])

            def draw_asteroid(obj, screen):
                pygame.draw.circle(screen, (139, 69, 19), (int(obj.x), int(obj.y)), 12)  # Brown color for asteroid

            def update_asteroid(obj):
                obj.x += belt_speed * direction
                if obj.x < 0 or obj.x > SCREEN_WIDTH:
                    worldstate.objects.remove(obj)  # Remove asteroid if it moves off the screen

                player_rect = pygame.Rect(worldstate.player.x, PLAYER_HEIGHT, worldstate.player.width, worldstate.player.height)
                asteroid_rect = pygame.Rect(obj.x - 12, obj.y - 12, 24, 24)
                if asteroid_rect.colliderect(player_rect):
                    worldstate.player.nuke_available = True  # Grant a nuke upon collision
                    worldstate.objects.remove(obj)

            asteroid_obj = Object(asteroid_x, belt_y, draw_asteroid, update_asteroid)
            worldstate.objects.append(asteroid_obj)

# Summary:
# - Added add_asteroid_belt: Introduces an asteroid belt as moving hazards that grant a nuke on collision.

import random
import math

def unleash_void_rift(worldstate):  # Introduces a void rift that alters gravity and visually obscures part of the screen
    if random.randint(0, 2000) < 2:  # Small chance to open a void rift each frame
        rift_x = random.randint(100, SCREEN_WIDTH - 100)
        rift_y = random.randint(100, SCREEN_HEIGHT - 200)
        rift_radius = 50
        gravity_intensity = 0.9

        def draw_void_rift(obj, screen):
            pygame.draw.circle(screen, (0, 0, 0), (int(obj.x), int(obj.y)), rift_radius)
            pygame.draw.circle(screen, (100, 100, 220), (int(obj.x), int(obj.y)), rift_radius, 3)

        def update_void_rift(obj):
            for enemy in worldstate.enemies[:]:
                dx = obj.x - enemy.x
                dy = obj.y - enemy.y
                dist = math.hypot(dx, dy)
                if dist < rift_radius:
                    enemy.direction *= -1  # Reverse the direction of the enemy
                    enemy.y += gravity_intensity * dy / abs(dy) if dy != 0 else 0
                
            for bullet in worldstate.bullets:
                dx = obj.x - bullet.x
                dy = obj.y - bullet.y
                dist = math.hypot(dx, dy)
                if dist < rift_radius:
                    bullet.dy *= gravity_intensity

            obj.timer -= 1
            if obj.timer <= 0:
                worldstate.objects.remove(obj)

        void_rift_obj = Object(rift_x, rift_y, draw_void_rift, update_void_rift)
        void_rift_obj.timer = 1000  # Void rift lasts for about 16 seconds
        worldstate.objects.append(void_rift_obj)

# Summary:
# - Added unleash_void_rift: Introduces a void rift altering gravity and obscuring screen area.

import random
import pygame
import math

def summon_starfall(worldstate):  # Summons a chain reaction of falling stars to damage enemies
    if random.randint(0, 1500) < 2:  # Small chance to summon starfall each frame
        star_x = random.randint(20, SCREEN_WIDTH - 20)

        def draw_star(obj, screen):
            pygame.draw.polygon(screen, (255, 255, 0), [  # Yellow star
                (obj.x, obj.y), (obj.x - 10, obj.y + 20),
                (obj.x + 10, obj.y + 20)
            ])

        def update_star(obj):
            obj.y += 4
            if obj.y > SCREEN_HEIGHT + 20:  # Remove star if off screen
                worldstate.objects.remove(obj)
                return
            
            # Cause a chain reaction with nearby enemies
            for enemy in worldstate.enemies[:]:
                if pygame.Rect(obj.x - 10, obj.y, 20, 20).colliderect((enemy.x, enemy.y, enemy.width, enemy.height)):
                    worldstate.enemies.remove(enemy)
                    worldstate.score += 10
                    # Generate chain reaction stars
                    for _ in range(3):
                        new_star = Object(enemy.x + random.randint(-30, 30), enemy.y, draw_star, update_star)
                        worldstate.objects.append(new_star)
                    worldstate.objects.remove(obj)
                    break

        initial_star = Object(star_x, 0, draw_star, update_star)
        worldstate.objects.append(initial_star)

# Summary:
# - Added summon_starfall: Introduces falling stars that cause chain reactions among enemies.

import random

def create_wormhole(worldstate):  # Spawns a wormhole that transports enemies to random positions
    if random.randint(0, 1000) < 2:  # Small chance to generate a wormhole each frame
        wormhole_x = random.randint(50, SCREEN_WIDTH - 50)
        wormhole_y = random.randint(50, SCREEN_HEIGHT - 150)

        def draw_wormhole(obj, screen):
            pygame.draw.circle(screen, (0, 0, 255), (int(obj.x), int(obj.y)), 15, 2)

        def update_wormhole(obj):
            for enemy in worldstate.enemies[:]:
                if math.hypot(obj.x - enemy.x, obj.y - enemy.y) < 20:
                    # Transport enemy to a new random position
                    enemy.x = random.randint(20, SCREEN_WIDTH - enemy.width - 20)
                    enemy.y = random.randint(20, PLAYER_HEIGHT - enemy.height - 20)

            obj.timer -= 1
            if obj.timer <= 0:
                worldstate.objects.remove(obj)

        wormhole_obj = Object(wormhole_x, wormhole_y, draw_wormhole, update_wormhole)
        wormhole_obj.timer = 800  # Wormhole lasts for about 13 seconds
        worldstate.objects.append(wormhole_obj)

# Summary:
# - Added create_wormhole: Spawns a wormhole that teleports enemies to random positions.

import random
import math

def trigger_earthquake(worldstate):  # Simulates an earthquake that temporarily shakes the screen and disrupts gameplay
    if random.randint(0, 1500) < 2:  # Small chance to initiate an earthquake each frame
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
# - Added trigger_earthquake: Simulates screen shaking and affects player/enemy positions temporarily.

import random
import pygame

def summon_nebula_worldstate(worldstate):  # Introduces a nebula that obscures part of the screen and slows down enemies
    if random.randint(0, 1500) < 2:  # Small chance to initiate a nebula each frame
        nebula_x = random.randint(100, SCREEN_WIDTH - 200)
        nebula_y = random.randint(50, SCREEN_HEIGHT - 200)
        nebula_width = 200
        nebula_height = 150
        slow_effect = 0.5  # Slow down enemies to 50% speed

        def draw_nebula(obj, screen):
            nebula_surface = pygame.Surface((nebula_width, nebula_height), pygame.SRCALPHA)
            nebula_surface.fill((100, 100, 255, 128))  # Blue semi-transparent overlay
            screen.blit(nebula_surface, (obj.x, obj.y))

        def update_nebula(obj):
            for enemy in worldstate.enemies:
                if obj.x < enemy.x < obj.x + nebula_width and obj.y < enemy.y < obj.y + nebula_height:
                    enemy.speed *= slow_effect  # Apply slowing effect
                
            obj.timer -= 1
            if obj.timer <= 0:
                worldstate.objects.remove(obj)

        nebula_obj = Object(nebula_x, nebula_y, draw_nebula, update_nebula)
        nebula_obj.timer = 600  # Nebula lasts for about 10 seconds
        worldstate.objects.append(nebula_obj)

# Summary:
# - Added summon_nebula_worldstate: Introduces a nebula that obscures screen and slows enemies.