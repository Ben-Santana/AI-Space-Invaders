import math
import random
import copy
import pygame
import sys


# from real_time.manage_functions import prepare_next_level

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
PURPLE = (200, 0, 255)
ORANGE = (255, 200, 0)

# Set up the display
pygame.display.set_caption("Space Invaders")

# Clock for controlling the frame rate
clock = pygame.time.Clock()
          
# Define the WorldState class
class WorldState:
    def __init__(self):
        self.player = Player()
        self.enemies = [Enemy(x * 60 + 50, y * 60 + 50) for x in range(8) for y in range(3)]
        self.boss = None
        self.bullets = []
        self.objects = []
        self.score = 0
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.level = 1
        self.boss_frequency = 3

# Define the Player class
class Player:
    def __init__(self):
        self.width = 50
        self.height = 50
        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.y = SCREEN_HEIGHT - self.height - 10
        self.speed = 8
        self.fastFire = False
        self.nuke_available = True

    def draw(self, surface):
        pygame.draw.rect(surface, GREEN, (self.x, self.y, self.width, self.height))
        # Bottom
        pygame.draw.rect(surface, BLACK, (self.x + 5, (self.y + self.height) -5, 40,10))
        pygame.draw.rect(surface, BLACK, (self.x + 10, (self.y + self.height) -10, 30,10))
        # Left Side
        pygame.draw.rect(surface, BLACK, (self.x, self.y, 5,self.height - 10))
        pygame.draw.rect(surface, BLACK, (self.x + 5, self.y, 5,self.height - 15))
        pygame.draw.rect(surface, BLACK, (self.x + 10, self.y, 5,self.height - 30))
        pygame.draw.rect(surface, BLACK, (self.x + 15, self.y, 5,self.height - 40))

        # Right Side
        pygame.draw.rect(surface, BLACK, (self.x + self.width - 5, self.y, 5,self.height - 10))
        pygame.draw.rect(surface, BLACK, ((self.x + self.width) - 10, self.y, 5,self.height - 15))
        pygame.draw.rect(surface, BLACK, ((self.x + self.width) - 15, self.y, 5,self.height - 30))
        pygame.draw.rect(surface, BLACK, ((self.x + self.width) - 20, self.y, 5,self.height - 40))

        #Cockpit
        pygame.draw.rect(surface, BLACK, ((self.x + 20, self.y + 10, 10,10)))
        
class Boss:
    def __init__(self, x, y):
        self.width = 120
        self.height = 90
        self.x = x
        self.y = y
        self.maxHP = 30
        self.health = copy.deepcopy(self.maxHP)  # More health than regular enemies
        self.speed = 2
        self.direction = 1  # 1 for right, -1 for left

    def draw(self, surface):
        # Draw the boss sprite
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

        # Display the health percentage above the boss sprite
        health_percentage = (self.health / self.maxHP) * 100
        font = pygame.font.Font(None, 30)  # Font for displaying the percentage
        health_text = font.render(f"{int(health_percentage)}%", True, WHITE)
        surface.blit(health_text, (self.x + self.width // 2 - health_text.get_width() // 2, self.y - 20))

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
        self.width = 55
        self.height = 40
        self.x = x
        self.y = y
        self.speed = 1
        self.direction = 1  # 1 for right, -1 for left

    def draw(self, surface):
        pygame.draw.rect(surface, PURPLE, (self.x, self.y, self.width, self.height))
        # Middle
        pygame.draw.rect(surface, BLACK, (self.x + 20, (self.y + self.height) - 5, 15, 5))
        pygame.draw.rect(surface, BLACK, (self.x + 25, (self.y + self.height) - 10, 5, 5))
        pygame.draw.rect(surface, BLACK, (self.x + 10, (self.y + self.height) - 15, 35, 5))
        pygame.draw.rect(surface, BLACK, (self.x + 20, (self.y + self.height) - 20, 15, 5))
        # Left Side
        pygame.draw.rect(surface, BLACK, (self.x, (self.y + self.height) - 5, 5, 5))
        pygame.draw.rect(surface, BLACK, (self.x + 5, (self.y + self.height) - 10, 15, 5))
        pygame.draw.rect(surface, BLACK, (self.x, (self.y + self.height) - 20, 5, 10))
        pygame.draw.rect(surface, BLACK, (self.x, self.y, 5, 5))
        pygame.draw.rect(surface, BLACK, (self.x + 10, self.y +5, 7.5, 7.5))
        # Right Side
        pygame.draw.rect(surface, BLACK, ((self.x + self.width) - 5, (self.y + self.height) - 5, 5, 5))
        pygame.draw.rect(surface, BLACK, ((self.x + self.width) - 20, (self.y + self.height) - 10, 15, 5))
        pygame.draw.rect(surface, BLACK, ((self.x + self.width) - 5, (self.y + self.height) - 20, 5, 10))
        pygame.draw.rect(surface, BLACK, ((self.x + self.width) - 5, self.y, 5, 5))
        pygame.draw.rect(surface, BLACK, ((self.x + self.width) - 17.5, self.y +5, 7.5, 7.5))        
        
        
class Object:
    # @params
    #  - draw_function : a function that takes in screen and the obstacle and draws it
    #  - update_function : a function that takes in the obstacle and updates it
    
    def __init__(self, x, y, draw_function, update_function):
        self.x = x
        self.y = y

        self.draw_function = draw_function
        self.update_function = update_function
    
    def draw(self):
        try:
            self.draw_function(self)
        except Exception as e:
            pass

    def update(self):
        try:
            self.update_function(self)
        except Exception as e:
            pass      

        

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
        pygame.draw.rect(surface, ORANGE, (self.x - 1.5, self.y -6.5, 8, 6.5))
        pygame.draw.rect(surface, RED, (self.x + 1.5, self.y + self.height, 2, 10))
        

# Function to handle player movement
def handle_player_movement(worldstate):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and worldstate.player.x > 0:
        worldstate.player.x -= worldstate.player.speed
    if keys[pygame.K_RIGHT] and worldstate.player.x < SCREEN_WIDTH - worldstate.player.width:
        worldstate.player.x += worldstate.player.speed
    if keys[pygame.K_SPACE]:
        handle_player_shooting(worldstate)
    if keys[pygame.K_f]:
        handle_cheats(worldstate)
    if keys[pygame.K_n]:  # Use the N key for the nuke
        use_nuke(worldstate)





# Function to handle shooting
def handle_player_shooting(worldstate):
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

# Gives Cheat 
def handle_cheats(worldstate):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_f] and not worldstate.player.fastFire:        
        worldstate.player.fastFire = True
    elif keys[pygame.K_f] and worldstate.player.fastFire:
        worldstate.player.fastFire = False

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
            display_game_over(worldstate.screen)
            # Restart the game
            worldstate.__init__()  # Reset the world state
            break


#Especial nuke
def use_nuke(worldstate):
    if worldstate.player.nuke_available:
        # Clear all enemies from the game
        worldstate.enemies.clear()
        worldstate.player.nuke_available = False  # Nuke can only be used once
        # Optional: Display a message to the player
        display_message(worldstate.screen, "NUKE Activated!\nAll Enemies Destroyed", duration=1, height = 40)

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


def display_message(surface, text, duration=2, height=None):
    font = pygame.font.Font("nothing-font-5x7.ttf", 48)
    
    # Split text into multiple lines
    lines = text.splitlines()
    
    # Calculate the total height of the text block
    total_height = len(lines) * font.get_height()
    
    # If height is provided, use it; otherwise, center the text vertically
    if height is None:
        start_y = (SCREEN_HEIGHT // 2) - (total_height // 2)
    else:
        # Ensure the message fits within the screen bounds
        start_y = min(height, SCREEN_HEIGHT - total_height)
    
    for i, line in enumerate(lines):
        # Render each line
        message = font.render(line, True, WHITE)
        
        # Center each line horizontally and stack vertically
        text_rect = message.get_rect(center=(SCREEN_WIDTH // 2, start_y + i * font.get_height()))
        
        # Display each line on the surface
        surface.blit(message, text_rect)

    pygame.display.flip()
    
    # Pause for a short duration (in seconds)
    pygame.time.delay(duration * 1000)

global level
level = 1  # Initialize level globally

def display_game_over(surface):
    global level  # Ensure level reset happens only here
    font = pygame.font.Font("nothing-font-5x7.ttf", 48)
    game_over_text = font.render("Game Over!", True, WHITE)
    restart_text = font.render("Press SPACE to Restart", True, WHITE)
    
    # Reset level to 1 only when the game is truly over
    level = 1

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

def update_boss(boss, worldstate):
    boss.move()  # Move boss based on its behavior
    if boss.y + boss.height >= worldstate.player.y:
        worldstate.enemies.clear()  # Clear all enemies to stop the game
        display_game_over(worldstate.screen)
        # Restart the game
        worldstate.__init__()  # Reset the world state

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

def display_menu(surface):
    global level
    font = pygame.font.Font("nothing-font-5x7.ttf", 48)
    menu_options = ["Start Game", "Quit "]
    level = 1
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

def display_summary_message(surface, summary_text):
    """Displays the summary of the new level at the bottom of the screen."""
    font = pygame.font.Font("nothing-font-5x7.ttf", 24)
    max_width = SCREEN_WIDTH - 40
    lines = []
    words = summary_text.split()
    current_line = ""
    for word in words:
        test_line = current_line + " " + word
        text_surface = font.render(test_line, True, WHITE)
        if text_surface.get_width() < max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "
    lines.append(current_line)

    y_offset = SCREEN_HEIGHT - 60 - (len(lines) - 1) * 24
    for line in lines:
        text = font.render(line, True, WHITE)
        surface.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, y_offset))
        y_offset += 24
    pygame.display.flip()

def draw_all_entities(worldstate):
    worldstate.player.draw(worldstate.screen)
    if worldstate.boss:
        worldstate.boss.draw(worldstate.screen)
    else:
        for enemy in worldstate.enemies:
            enemy.draw(worldstate.screen)
    
    for bullet in worldstate.bullets:
        bullet.draw(worldstate.screen)

def spawn_boss(worldstate):
    worldstate.boss = Boss(SCREEN_WIDTH // 2 - 60, 50)  # Center the boss at the top
    base_health = worldstate.boss.health
    worldstate.boss.health = worldstate.base_health + worldstate.level
 
def update_boss(boss, worldstate):
    boss.move()  # Move boss based on its behavior
    if boss.y + boss.height >= worldstate.player.y:
        worldstate.enemies.clear()  # Clear all enemies to stop the game
        display_game_over(worldstate.screen)
        # Restart the game
        worldstate.__init__()  # Reset the world state

def update_boss(worldstate):
        boss.move()  # Move boss based on its behavior

        if boss.y + boss.height >= worldstate.player.y:
            worldstate.enemies.clear()  # Clear all enemies to stop the game
            display_game_over(worldstate.screen)
            # Restart the game
            worldstate.__init__()  # Reset the world state

        handle_collisions_boss(worldstate, boss)

        if boss.health <= 0:  # Boss defeated
            boss = None
            display_message(worldstate.screen, f"Level {level} Complete!\nNext Level!", duration=2)
            level += 1
            #dynamic_functions, level_summary = prepare_next_level(level)  # Load new functions for the next level

def handle_new_level(worldstate):
    worldstate.objects = []
    worldstate.boss = None
    worldstate.enemies = [Enemy(x * 60 + 50, y * 60 + 50) for x in range(8) for y in range(3)]
    display_message(worldstate.screen, f"Level {worldstate.level}\nComplete! Next Level!", duration=2)
    worldstate.level += 1
    #dynamic_functions, level_summary = prepare_next_level(worldstate.level)  # Load new functions for the next level

    if worldstate.level <= 4:
        for enemy in worldstate.enemies:
            enemy.speed += worldstate.level / 5
        else:
            for enemy in worldstate.enemies:
                enemy.speed += worldstate.level / 10

def display_score(worldstate):
    font = pygame.font.Font("nothing-font-5x7.ttf", 36)
    score_text = font.render(f"Score: {worldstate.score}", True, WHITE)
    worldstate.screen.blit(score_text, (10, 10))

def draw_objects(worldstate):
    for obj in worldstate.objects:
        #try:
            obj.draw(worldstate.screen)
        #except Exception as e:
        #    print(f"Error drawing objects: {e}")

def update_objects(worldstate):
    for obj in worldstate.objects:
        try:
            obj.update()
        except Exception as e:
            print(f"Error updating objects: {e}")

def main():
    # Initialize level, dynamic functions, and level summary
    worldstate = WorldState()

    # Display the menu before starting the game
    display_menu(worldstate.screen)
    running = True

    #dynamic_functions, level_summary = prepare_next_level(worldstate.level)

    while running:
        worldstate.screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Spawn the boss if it's a boss level
        if worldstate.level % worldstate.boss_frequency == 0 and worldstate.boss is None:
            spawn_boss(worldstate)

        # Handle player and bullet movements
        handle_player_movement(worldstate)
        handle_player_shooting(worldstate)
        update_bullets(worldstate)
        handle_cheats(worldstate)
        update_enemies(worldstate)
        draw_all_entities(worldstate)

        if worldstate.boss:
            update_boss(worldstate)
        else:
            update_enemies(worldstate)
            handle_collisionsE(worldstate)
            if not worldstate.enemies:
                handle_new_level(worldstate)

        # YOUR FUNCTIONS WILL RUN HERE
        # for func_name, func in dynamic_functions.items():
        #     try:
        #         func(worldstate)  # Execute each function, passing the game state
        #     except Exception as e:
        #         print(f"Error executing {func_name}: {e}")

        display_score(worldstate)
        #display_summary_message(worldstate.screen, level_summary)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()