<<<<<<< HEAD
import math
import random
import WorldState

=======
>>>>>>> 54d15a9b1972ba912d23198504810ea65100f414

import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 500

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Define the WorldState class
class WorldState:
    def __init__(self):
        self.player = Player()
        self.enemies = [Enemy(x * 60 + 50, y * 60 + 50) for x in range(8) for y in range(3)]
        self.bullets = []
        self.score = 0

# Define the Player class
class Player:
    def __init__(self):
        self.width = 50
        self.height = 30
        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.y = SCREEN_HEIGHT - self.height - 10
        self.speed = 5

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, (self.x, self.y, self.width, self.height))

# Define the Enemy class
class Enemy:
    def __init__(self, x, y):
        self.width = 40
        self.height = 30
        self.x = x
        self.y = y
        self.speed = 1
        self.direction = 1  # 1 for right, -1 for left

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, (self.x, self.y, self.width, self.height))

# Define the Bullet class
class Bullet:
    def __init__(self, x, y, dy):
        self.width = 5
        self.height = 10
        self.x = x
        self.y = y
        self.dy = dy  # Direction and speed of bullet

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, (self.x, self.y, self.width, self.height))

# Function to handle player movement
def handle_player_movement(worldstate):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and worldstate.player.x > 0:
        worldstate.player.x -= worldstate.player.speed
    if keys[pygame.K_RIGHT] and worldstate.player.x < SCREEN_WIDTH - worldstate.player.width:
        worldstate.player.x += worldstate.player.speed

# Function to handle shooting
def handle_shooting(worldstate):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        # Limit to one bullet on screen
        if not any(bullet.dy < 0 for bullet in worldstate.bullets):
            bullet = Bullet(worldstate.player.x + worldstate.player.width // 2, worldstate.player.y, -10)
            worldstate.bullets.append(bullet)

# Function to update bullets
def update_bullets(worldstate):
    for bullet in worldstate.bullets[:]:
        bullet.y += bullet.dy
        if bullet.y < 0 or bullet.y > SCREEN_HEIGHT:
            worldstate.bullets.remove(bullet)

# Function to update enemies
def update_enemies(worldstate):
    move_down = False
    for enemy in worldstate.enemies:
        enemy.x += enemy.speed * enemy.direction
        if enemy.x <= 0 or enemy.x + enemy.width >= SCREEN_WIDTH:
            enemy.direction *= -1
            move_down = True
    if move_down:
        for enemy in worldstate.enemies:
            enemy.y += 10

# Function to handle collisions
def handle_collisions(worldstate):
    for bullet in worldstate.bullets[:]:
        for enemy in worldstate.enemies[:]:
            if (
                bullet.x < enemy.x + enemy.width and
                bullet.x + bullet.width > enemy.x and
                bullet.y < enemy.y + enemy.height and
                bullet.y + bullet.height > enemy.y
            ):
                worldstate.enemies.remove(enemy)
                worldstate.bullets.remove(bullet)
                worldstate.score += 10
                break

# Main game loop
def main():
    worldstate = WorldState()
    running = True
    while running:
        screen.fill(BLACK)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update game state
        handle_player_movement(worldstate)
        handle_shooting(worldstate)
        update_bullets(worldstate)
        update_enemies(worldstate)
        handle_collisions(worldstate)

        # Draw everything
        worldstate.player.draw(screen)
        for enemy in worldstate.enemies:
            enemy.draw(screen)
        for bullet in worldstate.bullets:
            bullet.draw(screen)

        # Display score
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {worldstate.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Update the display
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
