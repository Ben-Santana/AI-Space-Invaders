import math
import random
import copy
import pygame
import sys

from real_time.manage_functions import prepare_boss_level, prepare_next_level, reset_functions

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
PLAYER_HEIGHT = SCREEN_HEIGHT - 150

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (200, 0, 255)
ORANGE = (255, 200, 0)
BLUE = (0, 0, 255)
TEAL = (0, 255, 255)

# Bar properties
BAR_WIDTH = SCREEN_WIDTH - 40
BAR_HEIGHT = 15
BAR_X = 20
BAR_Y = SCREEN_HEIGHT - 5

# Colors for skins
PLAYER_SKINS = [GREEN, BLUE, ORANGE, TEAL]  # Define more colors as needed

# Set up the display
#screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
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
        self.gameOver = False
        self.dynamic_function, self.level_summary = prepare_next_level(1)
        self.running = True
        self.stars = generate_stars(100)

    def reset(self):
        self.player = Player()
        self.enemies = [Enemy(x * 60 + 50, y * 60 + 50) for x in range(8) for y in range(3)]
        self.boss = None
        self.bullets = []
        self.objects = []
        self.score = 0
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.level = 1
        self.boss_frequency = 3
        self.gameOver = False
        self.running = True
        self.stars = generate_stars(100)


# Define the Player class
class Player:
    def __init__(self, color=GREEN):
        self.width = 50
        self.height = 50
        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.fireRate = 1
        self.speed = 8
        self.nuke_available = True
        self.color = color  # Add color attribute for the skin

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, PLAYER_HEIGHT, self.width, self.height))  # Use the selected color for the skin
        # Bottom
        pygame.draw.rect(surface, BLACK, (self.x + 5, (PLAYER_HEIGHT + self.height) -5, 40,10))
        pygame.draw.rect(surface, BLACK, (self.x + 10, (PLAYER_HEIGHT + self.height) -10, 30,10))
        # Left Side
        pygame.draw.rect(surface, BLACK, (self.x, PLAYER_HEIGHT, 5,self.height - 10))
        pygame.draw.rect(surface, BLACK, (self.x + 5, PLAYER_HEIGHT, 5,self.height - 15))
        pygame.draw.rect(surface, BLACK, (self.x + 10, PLAYER_HEIGHT, 5,self.height - 30))
        pygame.draw.rect(surface, BLACK, (self.x + 15, PLAYER_HEIGHT, 5,self.height - 40))

        # Right Side
        pygame.draw.rect(surface, BLACK, (self.x + self.width - 5, PLAYER_HEIGHT, 5,self.height - 10))
        pygame.draw.rect(surface, BLACK, ((self.x + self.width) - 10, PLAYER_HEIGHT, 5,self.height - 15))
        pygame.draw.rect(surface, BLACK, ((self.x + self.width) - 15, PLAYER_HEIGHT, 5,self.height - 30))
        pygame.draw.rect(surface, BLACK, ((self.x + self.width) - 20, PLAYER_HEIGHT, 5,self.height - 40))

        #Cockpit
        pygame.draw.rect(surface, BLACK, ((self.x + 20, PLAYER_HEIGHT + 10, 10,10)))
        
class Boss:
    def __init__(self, x, y):
        self.width = 200
        self.height = 60
        self.x = x
        self.y = y
        self.maxHP = 30
        self.health = copy.deepcopy(self.maxHP)  # More health than regular enemies
        self.speed = 2
        self.direction = 1  # 1 for right, -1 for left

    def draw(self, surface):
        # Draw the main body in a retro, pixelated shape
        pygame.draw.rect(surface, PURPLE, (self.x, self.y, self.width, self.height))  # Body

        # Left Side
        pygame.draw.rect(surface, BLACK, (self.x, self.y, 50, 5))
        pygame.draw.rect(surface, BLACK, (self.x, self.y, 40, 10))
        pygame.draw.rect(surface, BLACK, (self.x, self.y + 10, 25, 10))
        pygame.draw.rect(surface, BLACK, (self.x, self.y + 20, 10, 10))
        pygame.draw.rect(surface, BLACK, (self.x, self.y + 40, 10, 10))
        pygame.draw.rect(surface, BLACK, (self.x, self.y + 50, 20, 10))
        pygame.draw.rect(surface, BLACK, (self.x + 30, self.y + 50, 40, 10))
        pygame.draw.rect(surface, BLACK, (self.x + 40, self.y + 45, 20, 10))
        pygame.draw.rect(surface, BLACK, (self.x + 30, self.y + 55, 50, 5))
        # Left Windows
        pygame.draw.rect(surface, BLACK, (self.x + 50, self.y + 20, 15, 15))
        pygame.draw.rect(surface, BLACK, (self.x + 92.5, self.y + 20, 15, 15))

        # Right Side
        pygame.draw.rect(surface, BLACK, ((self.x + self.width) - 50, self.y, 50, 5))
        pygame.draw.rect(surface, BLACK, ((self.x + self.width) - 40, self.y, 40, 10))
        pygame.draw.rect(surface, BLACK, ((self.x + self.width) - 25, self.y + 10, 25, 10))
        pygame.draw.rect(surface, BLACK, ((self.x + self.width) - 10, self.y + 20, 10, 10))
        pygame.draw.rect(surface, BLACK, ((self.x + self.width) - 10, self.y + 40, 10, 10))
        pygame.draw.rect(surface, BLACK, ((self.x + self.width) - 20, self.y + 50, 20, 10))
        pygame.draw.rect(surface, BLACK, ((self.x + self.width) - 70, self.y + 50, 40, 10))
        pygame.draw.rect(surface, BLACK, ((self.x + self.width) - 60, self.y + 45, 20, 10))
        pygame.draw.rect(surface, BLACK, ((self.x + self.width) - 80, self.y + 55, 30, 5))
        # Right Windows
        pygame.draw.rect(surface, BLACK, ((self.x + self.width) - 65, self.y + 20, 15, 15))
        

    def move(self):
        # Boss bounces left and right and moves down slowly
        if self.x <= 20 or self.x + self.width >= SCREEN_WIDTH - 20:
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
        pygame.draw.rect(surface, BLACK, (self.x + 15, (self.y + self.height) - 5, 25, 5))
        pygame.draw.rect(surface, BLACK, (self.x + 20, (self.y + self.height) - 10, 15, 5))
        pygame.draw.rect(surface, BLACK, (self.x + 10, (self.y + self.height) - 15, 35, 5))
        pygame.draw.rect(surface, BLACK, (self.x + 20, (self.y + self.height) - 20, 15, 5))
        # Left Side
        pygame.draw.rect(surface, BLACK, (self.x, (self.y + self.height) - 5, 5, 5))
        pygame.draw.rect(surface, BLACK, (self.x + 5, (self.y + self.height) - 10, 10, 5))
        pygame.draw.rect(surface, BLACK, (self.x, (self.y + self.height) - 20, 5, 10))
        pygame.draw.rect(surface, BLACK, (self.x, self.y, 5, 5))
        pygame.draw.rect(surface, BLACK, (self.x + 10, self.y +5, 7.5, 7.5))
        # Right Side
        pygame.draw.rect(surface, BLACK, ((self.x + self.width) - 5, (self.y + self.height) - 5, 5, 5))
        pygame.draw.rect(surface, BLACK, ((self.x + self.width) - 15, (self.y + self.height) - 10, 10, 5))
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
    
    def draw(self, screen):
        try:
            self.draw_function(self, screen)
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
        pygame.draw.ellipse(surface, WHITE, (self.x, self.y, self.width, self.height * 3))
        
class Star:
    def __init__(self, x, y, dy, size, color):
        self.x = x
        self.y = y
        self.dy = dy
        self.size = size
        self.color = color
    
    def update(self):
        self.y += self.dy
        if(self.y > SCREEN_HEIGHT): 
            self.y = 0
    
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.size)
    

def generate_stars(num_stars):
    stars = []
    for _ in range(num_stars):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        colorRandom = random.randint(0, 50) + 130
        color = pygame.Color(colorRandom + random.randint(0, 25), 
                             colorRandom + random.randint(0, 25), 
                             colorRandom + random.randint(0, 25))
        size = random.randint(1, 4)  # Random size for the star
        dy = size
        stars.append(Star(x, y, dy, size, color))
    return stars
    
    
# Draw stars on the screen
def draw_stars(worldstate):
    for star in worldstate.stars:
        star.draw(worldstate.screen)

def move_stars(worldstate):
    for star in worldstate.stars:
        star.update()

# Function to handle player movement
def handle_player_movement(worldstate):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and worldstate.player.x > 20:
        worldstate.player.x -= worldstate.player.speed
    if keys[pygame.K_RIGHT] and worldstate.player.x < SCREEN_WIDTH - worldstate.player.width - 20:
        worldstate.player.x += worldstate.player.speed
    if keys[pygame.K_SPACE]:
        handle_player_shooting(worldstate)
    if keys[pygame.K_n]:  # Use the N key for the nuke
        use_nuke(worldstate)

# Function to handle shooting
def handle_player_shooting(worldstate):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        # Limit to fireRate amount of bullets on screen
        if len(list(bullet.dy < 0 for bullet in worldstate.bullets)) < worldstate.player.fireRate:
            bullet = Bullet(worldstate.player.x + worldstate.player.width // 2, PLAYER_HEIGHT, -15)
            worldstate.bullets.append(bullet)

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
    if rightmost >= SCREEN_WIDTH - 20 or leftmost <= 20:
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
        if enemy.y + enemy.height >= PLAYER_HEIGHT:
            worldstate.gameOver = True
            break

# Special nuke
def use_nuke(worldstate):
    if worldstate.player.nuke_available:
        # Clear all enemies from the game
        worldstate.enemies.clear()
        #worldstate.player.nuke_available = False  # Nuke can only be used once
        # Optional: Display a message to the player
        display_message(worldstate.screen, "NUKE ACTIVATED!\nALL ENEMIES DESTROYED!", duration=1, height = 40)

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
    font = pygame.font.Font("contest.ttf", 48)
    
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

def display_game_over(worldstate):
    font = pygame.font.Font("contest.ttf", 48)
    game_over_text = font.render("GAME OVER!", True, WHITE)
    restart_text = font.render("PRESS SPACE TO RESTART", True, WHITE)

    worldstate.reset()

    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))

    worldstate.screen.blit(game_over_text, game_over_rect)
    worldstate.screen.blit(restart_text, restart_rect)
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
                worldstate.gameOver = False
                display_loading(worldstate)
                get_new_function(worldstate)



def update_boss(boss, worldstate):
    boss.move()  # Move boss based on its behavior
    if boss.y + boss.height >= worldstate.player.y:
        worldstate.enemies.clear()  # Clear all enemies to stop the game
        display_game_over(worldstate)
        # Restart the game
        worldstate.__init__()  # Reset the world state

def handle_collisions_boss(worldstate):
    for bullet in worldstate.bullets[:]:
        if (
            bullet.x < worldstate.boss.x + worldstate.boss.width and
            bullet.x + bullet.width > worldstate.boss.x and
            bullet.y < worldstate.boss.y + worldstate.boss.height and
            bullet.y + bullet.height > worldstate.boss.y
        ):
            worldstate.boss.health -= 1  # Decrease boss health
            worldstate.bullets.remove(bullet)

# Function to display the main menu with a skin change option
def display_menu(worldstate):

    menu_options = ["START", "CHOOSE COLOR", "QUIT", "RESET"]
    selected_option = 0

    while True:
        worldstate.screen.fill(BLACK)

        # Display title
        font = pygame.font.Font("contest.ttf", 86)
        title = font.render("TOMO", True, pygame.Color(255, 255, 255))
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        worldstate.screen.blit(title, title_rect)

        # Render menu options
        font = pygame.font.Font("contest.ttf", 32)
        for i, option in enumerate(menu_options):
            color = WHITE if i == selected_option else (180, 180, 180)
            text = font.render(option, True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 50))
            worldstate.screen.blit(text, text_rect)

        draw_stars(worldstate)
        move_stars(worldstate)

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
                    if selected_option == 0:
                        return  # Start the game
                    elif selected_option == 1:
                        display_skin_menu(worldstate.screen)  # Open the skin selection menu
                    elif selected_option == 2:
                        pygame.quit()
                        sys.exit()
                    elif selected_option == 3:
                        reset_functions()

# Function to display the skin selection menu
def display_skin_menu(surface):
    global PLAYER_SKINS
    font = pygame.font.Font("contest.ttf", 48)
    selected_skin = 0

    while True:
        surface.fill(BLACK)

        # Render skin options
        for i, color in enumerate(PLAYER_SKINS):
            skin_text = font.render("STARSHIP " + str(i+1), True, color)
            text_rect = skin_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 50))
            surface.blit(skin_text, text_rect)
            if i == selected_skin:
                # Highlight selected skin
                pygame.draw.rect(surface, WHITE, text_rect.inflate(10, 10), 2)

        pygame.display.flip()

        # Handle skin menu input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_skin = (selected_skin - 1) % len(PLAYER_SKINS)
                elif event.key == pygame.K_DOWN:
                    selected_skin = (selected_skin + 1) % len(PLAYER_SKINS)
                elif event.key == pygame.K_RETURN:
                    # Set the chosen color as the player's skin
                    selected_color = PLAYER_SKINS[selected_skin]
                    set_player_skin(selected_color)
                    return  # Return to the main menu

# Function to set the player's skin color
def set_player_skin(color):
    global player_skin
    player_skin = color  # Store the selected skin color globally

# Initialize player skin color
player_skin = GREEN  # Default color

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
    worldstate.boss.maxHP =  15 + (15 * worldstate.level)
    worldstate.boss.health = copy.deepcopy(worldstate.boss.maxHP)

def update_boss(worldstate):
        worldstate.boss.move()  # Move boss based on its behavior

        if worldstate.boss.y + worldstate.boss.height >= PLAYER_HEIGHT:
            worldstate.enemies.clear()  # Clear all enemies to stop the game
            display_game_over(worldstate)
            # Restart the game
            worldstate.__init__()  # Reset the world state

        handle_collisions_boss(worldstate)  # Load new functions for the next level

def handle_new_level(worldstate):
    worldstate.objects = []
    worldstate.boss = None
    worldstate.enemies = [Enemy(x * 60 + 50, y * 60 + 50) for x in range(8) for y in range(3)]
    display_message(worldstate.screen, f"LEVEL {worldstate.level} COMPLETE!\nNEXT LEVEL!", duration=2)
    worldstate.level += 1
    display_loading(worldstate)
    if not worldstate.gameOver:
        get_new_function(worldstate)

    if worldstate.level <= 4:
        for enemy in worldstate.enemies:
            enemy.speed += worldstate.level / 5
        else:
            for enemy in worldstate.enemies:
                enemy.speed += worldstate.level / 10

def get_new_function(worldstate):
    if worldstate.level % worldstate.boss_frequency == 0:
            worldstate.dynamic_function, worldstate.level_summary = prepare_boss_level()
    else: 
        worldstate.dynamic_function, worldstate.level_summary = prepare_next_level(worldstate.level)

def display_score(worldstate):
    font = pygame.font.Font("contest.ttf", 36)
    score_text = font.render(f"SCORE: {worldstate.score}", True, WHITE)
    worldstate.screen.blit(score_text, (10, 10))

def draw_objects(worldstate):
    for obj in worldstate.objects:
        try:
            obj.draw(worldstate.screen)
        except Exception as e:
            print(f"Error drawing objects: {e}")

def update_objects(worldstate):
    counter = 0
    for obj in worldstate.objects:
        try:
            obj.update()
            counter += 1
        except Exception as e:
            print(f"Error updating objects: {e}")

def draw_enemy_bar(surface, total_enemies, remaining_enemies):
    # Calculate the width of the filled portion of the bar based on remaining enemies
    if total_enemies > 0:
        fill_ratio = remaining_enemies / total_enemies
    else:
        fill_ratio = 0
    filled_width = int(BAR_WIDTH * fill_ratio)
    
    # Draw the background of the bar
    pygame.draw.rect(surface, pygame.Color(50, 50, 50), (BAR_X, BAR_Y, BAR_WIDTH, BAR_HEIGHT))
    
    # Draw the filled portion of the bar
    pygame.draw.rect(surface, WHITE, (BAR_X, BAR_Y, filled_width, BAR_HEIGHT))


def display_loading(worldstate):
    font = pygame.font.Font("contest.ttf", 48)
    worldstate.screen.fill(BLACK)
    draw_stars(worldstate)
    move_stars(worldstate)
    text = font.render("LOADING...", True, pygame.Color(255, 255, 255))
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT //2))
    worldstate.screen.blit(text, text_rect)
    pygame.display.flip()

def main():
    global player_skin
    # Initialize level, dynamic functions, and level summary
    worldstate = WorldState()

    # Display the menu before starting the game
    display_menu(worldstate)
    worldstate.player.color = player_skin

    while worldstate.running:
        worldstate.screen.fill(BLACK)

        # Draw stars in the background
        draw_stars(worldstate)

        # Move stars
        move_stars(worldstate)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                worldstate.running = False

        # Spawn the boss if it's a boss level
        if worldstate.level % worldstate.boss_frequency == 0 and worldstate.boss is None:
            spawn_boss(worldstate)

        # Handle player and bullet movements
        handle_player_movement(worldstate)
        handle_player_shooting(worldstate)
        update_bullets(worldstate)
        draw_all_entities(worldstate)
        draw_objects(worldstate)
        update_objects(worldstate)

        if worldstate.boss:
            draw_enemy_bar(worldstate.screen, worldstate.boss.maxHP, worldstate.boss.health)
            update_boss(worldstate)
            if worldstate.boss.health <= 0:  # Boss defeated
                worldstate.boss = None
                display_message(worldstate.screen, f"LEVEL {worldstate.level} COMPLETE!\nNEXT LEVEL!", duration=1)
                worldstate.level += 1
                get_new_function(worldstate)
        else:
            draw_enemy_bar(worldstate.screen, 24, len(worldstate.enemies))
            update_enemies(worldstate)
            handle_collisionsE(worldstate)
            if not worldstate.enemies:
                handle_new_level(worldstate)

        # YOUR FUNCTION WILL RUN HERE
        try:
            worldstate.dynamic_function(worldstate)  # Execute function, passing the game state
        except Exception as e:
            print(f"Error executing {worldstate.dynamic_function}: {e}")

        display_score(worldstate)
        display_summary_message(worldstate.screen, worldstate.level_summary)

        if worldstate.gameOver:
            display_game_over(worldstate)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()