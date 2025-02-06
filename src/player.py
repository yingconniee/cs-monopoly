import pygame
from settings import TILE_SIZE, FPS, MOVEMENT_PATH

class Player:
    def __init__(self, name, image, pos, offset, is_human=True):
        """Initialize player"""
        self.name = name
        self.image = pygame.transform.scale(image, (TILE_SIZE // 2, TILE_SIZE // 2))  # Fit within tile
        self.pos = pos
        self.offset = offset
        self.is_human = is_human

    def draw(self, screen):
        """Draw player on screen"""
        x = self.pos[1] * TILE_SIZE + self.offset[0]
        y = self.pos[0] * TILE_SIZE + self.offset[1]
        screen.blit(self.image, (x, y))

    def move(self, steps, screen, game_map, players):
        """Move the player step-by-step along the path"""
        for _ in range(steps):
            if tuple(self.pos) in MOVEMENT_PATH:  # Ensure player is in movement path
                current_index = MOVEMENT_PATH.index(tuple(self.pos))
                new_index = (current_index + 1) % len(MOVEMENT_PATH)  # Loop around board
                self.pos = list(MOVEMENT_PATH[new_index])

                # Update the screen after each step
                screen.blit(game_map.background_image, (0, 0))  # Redraw background
                game_map.draw(screen)  # Redraw board
                for player in players:
                    player.draw(screen)  # Redraw all players

                pygame.display.flip()
                pygame.time.delay(300)  # Small delay for smooth animation
