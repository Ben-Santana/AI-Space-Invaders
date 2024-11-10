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