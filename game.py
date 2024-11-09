import math
import random

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
GREEN = (0, 255, 0)
RED = (255, 0, 0)

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
        self.speed = 8
        self.fastFire = False

    def draw(self, surface):
        pygame.draw.rect(surface, GREEN, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(surface, GREEN, (self.x, self.y,35,40))
        pygame.draw.rect(surface, GREEN, (self.x, self.y,15,100))
# Define the Boss Class
class Boss:
    def __init__(self, x, y):
        self.width = 120
        self.height = 90
        self.x = x
        self.y = y
        self.health = 30  # More health than regular enemies
        self.speed = 2
        self.direction = 1  # 1 for right, -1 for left

    def draw(self, surface):
        pygame.draw.rect(surface, RED, (self.x, self.y, self.width, self.height))
        # Eyes (small black squares)
        eye_size = 30
        # Left eye
        pygame.draw.rect(surface, BLACK, (self.x + self.width // 4 - eye_size // 2, self.y + self.height // 4, eye_size, eye_size))
        # Right eye
        pygame.draw.rect(surface, BLACK, (self.x + 3 * self.width // 4 - eye_size // 2, self.y + self.height // 4, eye_size, eye_size))

        # Mouth (larger black square)
        mouth_width = 60
        mouth_height = 20
        mouth_x = self.x + self.width // 2 - mouth_width // 2
        mouth_y = self.y + 3 * self.height // 4

        # Draw the mouth outline
        pygame.draw.rect(surface, BLACK, (mouth_x, mouth_y, mouth_width, mouth_height))

        # Draw sharp teeth
        num_teeth = 5
        tooth_width = mouth_width // num_teeth
        tooth_height = mouth_height

        for i in range(num_teeth):
            # Each tooth is a triangle
            tooth_x = mouth_x + i * tooth_width
            pygame.draw.polygon(surface, WHITE, [
                (tooth_x, mouth_y),  # Top point of the triangle
                (tooth_x + tooth_width // 2, mouth_y + tooth_height),  # Bottom middle point
                (tooth_x + tooth_width, mouth_y)  # Top right point of the triangle
            ])
            # Draw health bar
            health_ratio = self.health / 30
            pygame.draw.rect(surface, GREEN, (self.x, self.y - 10, self.width * health_ratio, 5))

    def move(self):
        # Boss bounces left and right and moves down slowly
        if self.x <= 0 or self.x + self.width >= SCREEN_WIDTH:
            self.direction *= -1
        self.x += self.speed * self.direction
        if random.randint(1, 100) > 98:  # Small chance to move down
            self.y += 10


# Define the Enemy class
class Enemy:
    def __init__(self, x, y):

        self.width = 40
        self.height = 40
        self.x = x
        self.y = y
        self.speed = 1
        self.direction = 1  # 1 for right, -1 for left

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, (self.x, self.y, self.width, self.height))
        # Eyes (small black squares)
        eye_size = 10
        # Left eye
        pygame.draw.rect(surface, BLACK, (self.x + self.width // 4 - eye_size // 2, self.y + self.height // 4, eye_size, eye_size))
        # Right eye
        pygame.draw.rect(surface, BLACK, (self.x + 3 * self.width // 4 - eye_size // 2, self.y + self.height // 4, eye_size, eye_size))

        # Mouth (larger black square)
        mouth_width = 20
        pygame.draw.rect(surface, BLACK, (self.x + self.width // 2 - mouth_width // 2, self.y + 3 * self.height // 4, mouth_width, eye_size))

        

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
        if(worldstate.player.fastFire):
            bullet = Bullet(worldstate.player.x + worldstate.player.width // 2, worldstate.player.y, -10)
            worldstate.bullets.append(bullet)
        else:
            if not any(bullet.dy < 0 for bullet in worldstate.bullets):
                bullet = Bullet(worldstate.player.x + worldstate.player.width // 2, worldstate.player.y, -10)
                worldstate.bullets.append(bullet)

def cheat_FF(worldstate):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_f]:        
        worldstate.player.fastFire = True

# Function to update bullets
def update_bullets(worldstate):
    for bullet in worldstate.bullets[:]:
        bullet.y += bullet.dy
        if bullet.y < 0 or bullet.y > SCREEN_HEIGHT:
            worldstate.bullets.remove(bullet)

def update_enemies(worldstate):
    if not worldstate.enemies:
        return  # No enemies to update

    # Calculate the boundaries of the entire enemy group
    leftmost = min(enemy.x for enemy in worldstate.enemies)
    rightmost = max(enemy.x + enemy.width for enemy in worldstate.enemies)

    # Check if the entire group hits the wall
    move_down = False
    change_direction = False
    if rightmost >= SCREEN_WIDTH or leftmost <= 0:
        change_direction = True
        move_down = True

    # Update enemies positions
    for enemy in worldstate.enemies:
        if change_direction:
            enemy.direction *= -1
        enemy.x += enemy.speed * enemy.direction
        if move_down:
            enemy.y += 10
        
        # Check if any enemy reaches the bottom of the screen
        if enemy.y + enemy.height >= worldstate.player.y:
            worldstate.enemies.clear()  # Clear all enemies to stop the game
            display_game_over(screen)
            # Restart the game
            worldstate.__init__()  # Reset the world state
            break



# Function to handle collisions
def handle_collisionsE(worldstate):
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

def display_message(surface, text, duration=2):
    font = pygame.font.SysFont(None, 48)
    message = font.render(text, True, WHITE)
    text_rect = message.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    
    surface.blit(message, text_rect)
    pygame.display.flip()
    
    # Pause for a short duration (in seconds)
    pygame.time.delay(duration * 1000)

def display_game_over(surface):
    font = pygame.font.SysFont(None, 48)
    game_over_text = font.render("Game Over!", True, WHITE)
    restart_text = font.render("Press SPACE to Restart", True, WHITE)
    
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
    
    surface.blit(game_over_text, game_over_rect)
    surface.blit(restart_text, restart_rect)
    pygame.display.flip()
    
    # Wait for the player to press the space bar to restart
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False

def update_boss(boss):
    boss.move()  # Move boss based on its behavior

def handle_collisions_boss(worldstate, boss):
    for bullet in worldstate.bullets[:]:
        if (
            bullet.x < boss.x + boss.width and
            bullet.x + bullet.width > boss.x and
            bullet.y < boss.y + boss.height and
            bullet.y + bullet.height > boss.y
        ):
            boss.health -= 1  # Decrease boss health
            worldstate.bullets.remove(bullet)
            worldstate.score += 50  # Higher score for hitting boss

def display_menu(surface):
    font = pygame.font.SysFont(None, 48)
    menu_options = ["Start Game", "Quit"]
    selected_option = 0

    while True:
        surface.fill(BLACK)

        # Render menu options
        for i, option in enumerate(menu_options):
            if i == selected_option:
                color = (0, 255, 0)  # Highlight selected option in green
            else:
                color = WHITE

            text = font.render(option, True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 50))
            surface.blit(text, text_rect)

        pygame.display.flip()

        # Handle menu input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    # If "Start Game" is selected
                    if selected_option == 0:
                        return  # Exit the menu and start the game
                    # If "Quit" is selected
                    elif selected_option == 1:
                        pygame.quit()
                        sys.exit()


def main():
    # Display the menu before starting the game
    display_menu(screen)
    running = True
    level = 1
    worldstate = WorldState()
    boss = None
    bossCounter = 0

    while running:
        screen.fill(BLACK)
        boss_level = (level % 3) == 0  # Boss level every 3 levels

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if boss_level and boss is None:  # Spawn the boss if it's a boss level
            boss = Boss(SCREEN_WIDTH // 2 - 60, 50)  # Center the boss at the top
            base_health = boss.health
            boss.health = base_health + bossCounter*2



        handle_player_movement(worldstate)
        handle_shooting(worldstate)
        update_bullets(worldstate)
        cheat_FF(worldstate)

        if boss:
            update_boss(boss)
            handle_collisions_boss(worldstate, boss)
            if boss.health <= 0:  # Boss defeated
                boss = None
                display_message(screen, f"Level {level} Complete! Next Level", duration=2)
                level += 1
        else:
            update_enemies(worldstate)
            handle_collisionsE(worldstate)
            if not worldstate.enemies:
                display_message(screen, f"Level {level} Complete! Next Level", duration=2)
                level += 1
                worldstate.enemies = [Enemy(x * 60 + 50, y * 60 + 50) for x in range(8) for y in range(3)]
                if(level <= 4):
                    for enemy in worldstate.enemies:
                        enemy.speed += level
                else:
                    for enemy in worldstate.enemies:
                        enemy.speed += level / 2

        worldstate.player.draw(screen)
        if boss:
            boss.draw(screen)
        else:
            for enemy in worldstate.enemies:
                enemy.draw(screen)
        
        for bullet in worldstate.bullets:
            bullet.draw(screen)

        font = pygame.font.Font("nothing-font-5x7.ttf", 36)
        score_text = font.render(f"Score: {worldstate.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()