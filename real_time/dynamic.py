import pygame
from game import WorldState, Obstacle, Player, Boss, Enemy, Bullet, SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, GREEN, RED, screen, clock


import pygame
def deploy_shield_over_player(worldstate):  # Deploys a temporary shield over the player
    shield_duration = 300  # Duration for the shield to stay active
    shield_activation_score = 100  # Score at which the shield is activated

    if worldstate.score >= shield_activation_score:
        current_time = pygame.time.get_ticks()
        if not hasattr(worldstate, 'shield_activated'):
            worldstate.shield_activated = current_time

        if current_time - worldstate.shield_activated < shield_duration:
            # Draw a shield around the player
            shield_color = (0, 255, 0)
            player_x = worldstate.player.x
            player_y = worldstate.player.y
            shield_padding = 5
            shield_rect = (
                player_x - shield_padding,
                player_y - shield_padding,
                worldstate.player.width + 2 * shield_padding,
                worldstate.player.height + 2 * shield_padding
            )
            pygame.draw.rect(worldstate.screen, shield_color, shield_rect, 2)

            # Prevent enemy bullets from hitting the player
            for bullet in worldstate.bullets:
                if (
                    bullet.x > player_x - shield_padding
                    and bullet.x < player_x + worldstate.player.width + shield_padding
                    and bullet.y > player_y - shield_padding
                    and bullet.y < player_y + worldstate.player.height + shield_padding
                ):
                    worldstate.bullets.remove(bullet)

        # Reset shield activation when duration is exceeded
        else:
            delattr(worldstate, 'shield_activated')

# Summary:
# - Added deploy_shield_over_player: Activates a temporary shield above the player at a certain score.