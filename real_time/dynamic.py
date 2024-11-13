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

def spawn_shooting_star(worldstate):  # Introduces shooting stars that can be shot by player or hit player
    if random.randint(0, 500) < 3:  # Approximately 0.6% chance to spawn a shooting star per frame
        star_speed = random.randint(3, 6)

        # Initial position of the shooting star
        star_x = random.randint(0, SCREEN_WIDTH - 30)
        star_y = 0
        
        def draw_star(obj, screen):
            pygame.draw.polygon(screen, (255, 255, 0), [
                (obj.x, obj.y),
                (obj.x + 15, obj.y + 30),
                (obj.x + 30, obj.y),
                (obj.x + 30, obj.y + 10),
                (obj.x + 45, obj.y + 10),
                (obj.x + 25, obj.y + 20),
                (obj.x + 35, obj.y + 40),
                (obj.x + 15, obj.y + 25),
                (obj.x - 5, obj.y + 40),
                (obj.x + 5, obj.y + 20),
                (obj.x - 15, obj.y + 10),
                (obj.x, obj.y + 10)
            ])
        
        def update_star(obj):
            obj.y += star_speed
            if obj.y > SCREEN_HEIGHT:  # Remove the star if it goes off screen
                worldstate.objects.remove(obj)
            elif pygame.Rect(obj.x, obj.y, 30, 40).colliderect(worldstate.player.x, PLAYER_HEIGHT, worldstate.player.width, worldstate.player.height):
                worldstate.gameOver = True  # End game if shooting star hits player
                worldstate.objects.remove(obj)

            # Handle bullet collision
            for bullet in worldstate.bullets[:]:
                if pygame.Rect(obj.x, obj.y, 30, 40).colliderect(bullet.x, bullet.y, bullet.width, bullet.height):
                    worldstate.bullets.remove(bullet)  # Remove the bullet upon collision
                    worldstate.objects.remove(obj)  # Remove the star upon collision
            
        shooting_star = Object(star_x, star_y, draw_star, update_star)
        worldstate.objects.append(shooting_star)

# Summary:
# - Added spawn_shooting_star: Shooting stars appear and can be destroyed by player.

import pygame
import random

def deploy_space_mines(worldstate):  # Spawns static mines that explode on collision and can be destroyed
    if random.randint(0, 500) < 2:  # Approximately 0.4% chance to spawn a mine per frame
        mine_x = random.randint(50, SCREEN_WIDTH - 50)
        mine_y = random.randint(50, PLAYER_HEIGHT - 100)

        def draw_mine(obj, screen):
            pygame.draw.circle(screen, (255, 0, 0), (obj.x, obj.y), 15)
            pygame.draw.circle(screen, (255, 150, 150), (obj.x, obj.y), 20, 2)

        def update_mine(obj):
            mine_rect = pygame.Rect(obj.x - 15, obj.y - 15, 30, 30)
            player_rect = pygame.Rect(worldstate.player.x, PLAYER_HEIGHT, worldstate.player.width, worldstate.player.height)

            if mine_rect.colliderect(player_rect):
                worldstate.gameOver = True
                worldstate.objects.remove(obj)

            for bullet in worldstate.bullets[:]:
                bullet_rect = pygame.Rect(bullet.x, bullet.y, bullet.width, bullet.height)
                if mine_rect.colliderect(bullet_rect):
                    worldstate.bullets.remove(bullet)
                    worldstate.objects.remove(obj)
                    break

        worldstate.objects.append(Object(mine_x, mine_y, draw_mine, update_mine))

# Summary:
# - Added deploy_space_mines: Mines can kill or be killed, adding a new challenge element.

import pygame
import random

def summon_blackhole(worldstate):  # Introduces a black hole that pulls in player and bullets
    if random.randint(0, 600) < 2:  # About 0.33% chance to spawn a black hole each frame
        blackhole_radius = 60
        effect_radius = 150
        blackhole_x = random.randint(0, SCREEN_WIDTH - blackhole_radius * 2)
        blackhole_y = random.randint(0, SCREEN_HEIGHT - PLAYER_HEIGHT - blackhole_radius * 2)

        def draw_blackhole(blackhole, screen):
            pygame.draw.circle(screen, (0, 0, 0), (blackhole.x + blackhole_radius, blackhole.y + blackhole_radius), blackhole_radius)
            pygame.draw.circle(screen, (80, 80, 255), (blackhole.x + blackhole_radius, blackhole.y + blackhole_radius), blackhole_radius, 5)

        def update_blackhole(obj):
            player_rect = pygame.Rect(worldstate.player.x, PLAYER_HEIGHT, worldstate.player.width, worldstate.player.height)
            blackhole_center = (obj.x + blackhole_radius, obj.y + blackhole_radius)

            if player_rect.colliderect(pygame.Rect(obj.x, obj.y, blackhole_radius * 2, blackhole_radius * 2)):
                worldstate.gameOver = True
                worldstate.objects.remove(obj)

            def pull_towards(object_x, object_y, center_x, center_y):
                dx, dy = center_x - object_x, center_y - object_y
                distance = (dx ** 2 + dy ** 2) ** 0.5
                if distance < effect_radius:
                    magnitude = min((effect_radius - distance) / effect_radius, 1)
                    return dx * magnitude / 10, dy * magnitude / 10
                return 0, 0

            # Pull player towards black hole
            px_pull, py_pull = pull_towards(worldstate.player.x, PLAYER_HEIGHT, *blackhole_center)
            worldstate.player.x += px_pull

            # Pull bullets towards black hole
            for bullet in worldstate.bullets[:]:
                bx_pull, by_pull = pull_towards(bullet.x, bullet.y, *blackhole_center)
                bullet.x += bx_pull
                bullet.y += by_pull
                if bullet.x < obj.x or bullet.x > obj.x + blackhole_radius * 2 or bullet.y < obj.y or bullet.y > obj.y + blackhole_radius * 2:
                    continue
                worldstate.bullets.remove(bullet)

        blackhole = Object(blackhole_x, blackhole_y, draw_blackhole, update_blackhole)
        worldstate.objects.append(blackhole)

# Summary:
# - Added summon_blackhole: Introduces black holes that pull in player and bullets.

import pygame
import random

def deploy_galactic_wormhole(worldstate):  # Creates a wormhole that temporarily teleports enemies to random positions
    if random.randint(0, 1000) < 3:  # Approximately 0.3% chance to create a wormhole each frame
        wormhole_x = random.randint(50, SCREEN_WIDTH - 150)
        wormhole_y = random.randint(50, SCREEN_HEIGHT - 150)
        lifespan = 200  # Wormhole exists for about 3 seconds at 60 FPS

        def draw_wormhole(obj, screen):
            pygame.draw.ellipse(screen, PURPLE, (obj.x, obj.y, 100, 100))
            pygame.draw.ellipse(screen, TEAL, (obj.x + 10, obj.y + 10, 80, 80))
            pygame.draw.ellipse(screen, PURPLE, (obj.x + 20, obj.y + 20, 60, 60))

        def update_wormhole(obj):
            obj.timer -= 1
            if obj.timer <= 0:
                worldstate.objects.remove(obj)  # Remove wormhole after time lapses

            for enemy in worldstate.enemies:
                enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
                wormhole_rect = pygame.Rect(obj.x, obj.y, 100, 100)
                if enemy_rect.colliderect(wormhole_rect):
                    enemy.x = random.randint(0, SCREEN_WIDTH - enemy.width)
                    enemy.y = random.randint(0, PLAYER_HEIGHT - 200)

        wormhole = Object(wormhole_x, wormhole_y, draw_wormhole, update_wormhole)
        wormhole.timer = lifespan
        worldstate.objects.append(wormhole)

# Summary:
# - Added deploy_galactic_wormhole: Creates a wormhole teleporting enemies randomly.

import pygame
import random

def unleash_photon_storm(worldstate):  # Summons a storm of energy orbs that the player must dodge
    if random.randint(0, 500) < 3:  # 0.6% chance to trigger per frame
        storm_duration = 180  # Lasts for approximately 3 seconds at 60 FPS
        orb_speed = 8
        orb_count = 10

        def draw_photon_orb(obj, screen):
            pygame.draw.circle(screen, (255, 255, 102), (obj.x, obj.y), 10)
            pygame.draw.circle(screen, WHITE, (obj.x, obj.y), 10, 1)

        def update_photon_orb(obj):
            obj.y += orb_speed
            if obj.y > SCREEN_HEIGHT:
                worldstate.objects.remove(obj)
            elif pygame.Rect(obj.x - 10, obj.y - 10, 20, 20).colliderect(
                worldstate.player.x, PLAYER_HEIGHT, worldstate.player.width, worldstate.player.height):
                worldstate.gameOver = True
                worldstate.objects.remove(obj)

        for _ in range(orb_count):
            orb_x = random.randint(0, SCREEN_WIDTH - 20)
            orb_y = random.randint(-SCREEN_HEIGHT, -20)
            photon_orb = Object(orb_x, orb_y, draw_photon_orb, update_photon_orb)
            worldstate.objects.append(photon_orb)

# Summary:
# - Added unleash_photon_storm: Summons energy orbs for the player to dodge, adding difficulty.

def boss_energy_barrier(worldstate):  # Adds a temporary shield around the boss that blocks player bullets
    if worldstate.boss and not any(isinstance(obj, type('EnergyBarrier', (), {})) for obj in worldstate.objects):
        barrier_lifespan = 120  # Lasts for 2 seconds

        def draw_barrier(obj, screen):
            pygame.draw.ellipse(screen, (200, 200, 255, 127), (worldstate.boss.x - 20, worldstate.boss.y - 20, worldstate.boss.width + 40, worldstate.boss.height + 40), 5)

        def update_barrier(obj):
            obj.timer -= 1
            if obj.timer <= 0:
                worldstate.objects.remove(obj)

            for bullet in worldstate.bullets[:]:
                barrier_rect = pygame.Rect(worldstate.boss.x - 20, worldstate.boss.y - 20, worldstate.boss.width + 40, worldstate.boss.height + 40)
                bullet_rect = pygame.Rect(bullet.x, bullet.y, bullet.width, bullet.height)
                if barrier_rect.colliderect(bullet_rect):
                    worldstate.bullets.remove(bullet)

        shield = Object(worldstate.boss.x - 20, worldstate.boss.y - 20, draw_barrier, update_barrier)
        shield.timer = barrier_lifespan
        type(shield).__name__ = 'EnergyBarrier'  # Unique type name to ensure single instance
        worldstate.objects.append(shield)

# Summary:
# - Added boss_energy_barrier: Temporarily shields boss from bullets with an energy barrier.

import pygame
import random

def deploy_holo_decoys(worldstate):  # Generates holographic decoys to distract enemy bullets
    if random.randint(0, 600) < 3:  # About 0.5% chance to spawn decoys each frame
        decoy_duration = 120  # Duration for which decoys last (2 seconds at 60 FPS)
        decoy_x = random.randint(50, SCREEN_WIDTH - 100)
        decoy_y = SCREEN_HEIGHT - PLAYER_HEIGHT - 100

        def draw_decoy(obj, screen):
            pygame.draw.rect(screen, (150, 150, 255), (obj.x, PLAYER_HEIGHT, 50, 50), 1)  # Faint outline indicating hologram
            pygame.draw.circle(screen, (0, 75, 150, 75), (obj.x + 25, PLAYER_HEIGHT + 25), 25, 1)  # Light glow effect
        
        def update_decoy(obj):
            obj.timer -= 1
            if obj.timer <= 0:
                worldstate.objects.remove(obj)  # Remove decoy when duration ends
            else:
                for bullet in worldstate.bullets[:]:
                    if bullet.dy > 0:  # Check only for downward bullets
                        if pygame.Rect(obj.x, PLAYER_HEIGHT, 50, 50).colliderect(bullet.x, bullet.y, bullet.width, 3 * bullet.height):
                            worldstate.bullets.remove(bullet)  # Absorb enemy bullet that hits the decoy

        decoy = Object(decoy_x, PLAYER_HEIGHT, draw_decoy, update_decoy)
        decoy.timer = decoy_duration
        worldstate.objects.append(decoy)

# Summary:
# - Added deploy_holo_decoys: Generates holographic decoys that distract enemy bullets.

import pygame
import random

def deploy_cosmic_vortex(worldstate):  # Creates a vortex that alters the trajectory of bullets
    if random.randint(0, 700) < 2:  # About 0.28% chance to deploy a vortex each frame
        vortex_x = random.randint(100, SCREEN_WIDTH - 100)
        vortex_y = random.randint(50, SCREEN_HEIGHT // 2)  # Position the vortex in the upper half

        def draw_vortex(obj, screen):
            pygame.draw.circle(screen, (128, 0, 128), (obj.x, obj.y), 60, 5)
            pygame.draw.circle(screen, (100, 0, 100), (obj.x, obj.y), 40, 3)

        def update_vortex(obj):
            for bullet in worldstate.bullets[:]:
                bullet_rect = pygame.Rect(bullet.x, bullet.y, bullet.width, bullet.height)
                vortex_rect = pygame.Rect(obj.x - 60, obj.y - 60, 120, 120)
                if bullet_rect.colliderect(vortex_rect):
                    # Alter bullet trajectory slightly to simulate a vortex pull
                    bullet.x += random.choice([-2, -1, 0, 1, 2])

            if random.randint(0, 200) == 1:  # Randomly remove the vortex after some time
                worldstate.objects.remove(obj)

        vortex = Object(vortex_x, vortex_y, draw_vortex, update_vortex)
        worldstate.objects.append(vortex)

# Summary:
# - Added deploy_cosmic_vortex: Alters bullet trajectories creating challenging dynamics.

def boss_fire_projectiles(worldstate):  # Enhances the boss with projectile-firing capabilities
    if worldstate.boss and random.randint(0, 600) < 3:  # About 0.5% chance each frame to launch projectiles
        projectile_speed = 6
        projectile_width, projectile_height = 10, 20

        def draw_projectile(obj, screen):
            pygame.draw.rect(screen, (255, 0, 0), (obj.x, obj.y, projectile_width, projectile_height))  # Red projectile

        def update_projectile(obj):
            obj.y += projectile_speed
            if obj.y > SCREEN_HEIGHT:
                worldstate.objects.remove(obj)  # Remove if out of screen

            # Check collision with player
            player_rect = pygame.Rect(worldstate.player.x, PLAYER_HEIGHT, worldstate.player.width, worldstate.player.height)
            projectile_rect = pygame.Rect(obj.x, obj.y, projectile_width, projectile_height)
            if projectile_rect.colliderect(player_rect):
                worldstate.gameOver = True  # End game if hits player
                worldstate.objects.remove(obj)

        # Generate projectiles from boss's current position
        projectile_x = random.randint(worldstate.boss.x, worldstate.boss.x + worldstate.boss.width - projectile_width)
        projectile = Object(projectile_x, worldstate.boss.y + worldstate.boss.height, draw_projectile, update_projectile)
        worldstate.objects.append(projectile)

# Summary:
# - Added boss_fire_projectiles: Enhances the boss with a projectile attack capability.

import pygame
import random

def activate_hyperdrive(worldstate):  # Increases player's speed and temporarily slows down enemies and bullets
    if random.randint(0, 500) < 3:  # Approximately 0.6% chance to activate hyperdrive each frame
        hyperdrive_duration = 180  # Duration for approximately 3 seconds at 60 FPS
        original_player_speed = worldstate.player.speed
        worldstate.player.speed *= 2  # Double the player's speed

        def draw_hyperdrive(obj, screen):
            pygame.draw.rect(screen, (0, 255, 0), (worldstate.player.x, PLAYER_HEIGHT, worldstate.player.width, worldstate.player.height), 2)

        def update_hyperdrive(obj):
            obj.timer -= 1
            if obj.timer <= 0:
                worldstate.player.speed = original_player_speed
                worldstate.objects.remove(obj)

            for bullet in worldstate.bullets:
                if bullet.dy > 0:  # Only slow down enemy bullets
                    bullet.dy = max(1, bullet.dy / 2)

            for enemy in worldstate.enemies:
                enemy.speed = max(0.5, enemy.speed / 2)

        hyperdrive = Object(worldstate.player.x, PLAYER_HEIGHT, draw_hyperdrive, update_hyperdrive)
        hyperdrive.timer = hyperdrive_duration
        worldstate.objects.append(hyperdrive)

# Summary:
# - Added activate_hyperdrive: Temporarily boosts player's speed while slowing enemies and bullets.

import pygame
import random

def enchant_nova_waves(worldstate):  # Summons waves of energy that ripple through the play area
    if random.randint(0, 400) < 2:  # Approximately 0.5% chance to trigger nova waves each frame
        wave_count = 3
        wave_spacing = 150
        wave_speed = 3

        def draw_wave(obj, screen):
            pygame.draw.arc(screen, (255, 215, 0), (obj.x, obj.y, 200, 100), 0, math.pi, 5)  # Draw the wave arc

        def update_wave(obj):
            obj.y += wave_speed
            if obj.y > SCREEN_HEIGHT:
                worldstate.objects.remove(obj)

            # Check for collision with player's y-range
            if pygame.Rect(obj.x, obj.y, 200, 5).colliderect(worldstate.player.x, PLAYER_HEIGHT, worldstate.player.width, worldstate.player.height):
                worldstate.gameOver = True  # End game if player hit by a wave

        for i in range(wave_count):
            wave_y = -wave_spacing * i  # Position waves apart
            wave_x = random.randint(0, SCREEN_WIDTH - 200)
            nova_wave = Object(wave_x, wave_y, draw_wave, update_wave)
            worldstate.objects.append(nova_wave)

# Summary:
# - Added enchant_nova_waves: Summons waves of energy that ripple downward hazardously.

def initiate_quantum_jump(worldstate):  # Introduces a feature allowing the player to teleport to a random location temporarily
    import random
    if random.randint(0, 500) < 3:  # Approximately 0.6% chance to initiate a quantum jump each frame
        teleport_duration = 160  # Teleport lasts for about 2.6 seconds
        initial_x = worldstate.player.x

        def draw_teleport_effect(obj, screen):
            color_phase = 255 if obj.timer % 15 < 7 else 0
            pygame.draw.rect(screen, (color_phase, 255, color_phase), (worldstate.player.x, PLAYER_HEIGHT, worldstate.player.width, worldstate.player.height), 2)

        def update_teleport(obj):
            obj.timer -= 1
            if obj.timer == teleport_duration // 2:
                worldstate.player.x = random.randint(20, SCREEN_WIDTH - 20 - worldstate.player.width)  # Teleport to new location around halfway
            if obj.timer <= 0:
                worldstate.player.x = initial_x  # Reset to initial position
                worldstate.objects.remove(obj)

        teleport_effect = Object(worldstate.player.x, PLAYER_HEIGHT, draw_teleport_effect, update_teleport)
        teleport_effect.timer = teleport_duration
        worldstate.objects.append(teleport_effect)

# Summary:
# - Added initiate_quantum_jump: Temporarily teleports the player to a random location.

import pygame
import random

def initiate_crimson_fog(worldstate):  # Brings forth a foggy ambience that reduces visibility for a few seconds
    if random.randint(0, 600) < 2:  # Approximately 0.33% chance to activate crimson fog each frame
        fog_duration = 180  # Fog lasts for approximately 3 seconds

        def draw_fog(obj, screen):
            fog_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            fog_overlay.set_alpha(150)  # Set transparency level
            fog_overlay.fill((153, 0, 0))  # Dark red fog
            screen.blit(fog_overlay, (0, 0))

        def update_fog(obj):
            obj.timer -= 1
            if obj.timer <= 0:
                worldstate.objects.remove(obj)

        crimson_fog = Object(0, 0, draw_fog, update_fog)
        crimson_fog.timer = fog_duration
        worldstate.objects.append(crimson_fog)

# Summary:
# - Added initiate_crimson_fog: Temporarily reduces visibility with a crimson fog.

def deploy_ion_cannon(worldstate):  # Periodically fires a large beam that clears bullets and damages enemies
    if random.randint(0, 400) < 2:  # About 0.5% chance to deploy ion cannon each frame
        cannon_duration = 100  # Cannon fires for approximately 1.6 seconds

        def draw_cannon(obj, screen):
            pygame.draw.rect(screen, (0, 255, 255), (obj.x, 0, 10, SCREEN_HEIGHT))

        def update_cannon(obj):
            obj.timer -= 1
            if obj.timer <= 0:
                worldstate.objects.remove(obj)

            # Clear player bullets
            for bullet in worldstate.bullets[:]:
                if obj.x - 5 < bullet.x < obj.x + 5:
                    worldstate.bullets.remove(bullet)

            # Damage enemies
            for enemy in worldstate.enemies[:]:
                if obj.x - 5 < enemy.x < obj.x + 5:
                    worldstate.enemies.remove(enemy)
                    worldstate.score += 10

            # Handle boss collision
            if worldstate.boss and obj.x - 5 < worldstate.boss.x + worldstate.boss.width / 2 < obj.x + 5:
                worldstate.boss.health -= 1

        cannon_x = random.randint(50, SCREEN_WIDTH - 50)
        ion_cannon = Object(cannon_x, 0, draw_cannon, update_cannon)
        ion_cannon.timer = cannon_duration
        worldstate.objects.append(ion_cannon)

# Summary:
# - Added deploy_ion_cannon: Fires a periodic beam clearing bullets and damaging enemies. 