import pygame
import random
from src.settings import BOARD_SIZE, TILE_SIZE, BLUE, PLAYER_COLORS, MOVEMENT_PATH, SCREEN_HEIGHT, SCREEN_WIDTH, PROPERTY_BORDER, BLACK
from src.property import Property

class Map:
    def __init__(self):
        """Initialize map with randomly assigned property positions"""
        self.property_positions = set(random.sample(MOVEMENT_PATH, 20))
        self.properties = {pos: Property(pos) for pos in self.property_positions}

        # Assign unique property names
        self.property_names = {pos: f"MCS{index:03d}" for index, pos in enumerate(self.property_positions, start=1)}

        # Identify available positions for minigames
        available_positions = [pos for pos in MOVEMENT_PATH if pos not in self.property_positions]
        self.minigame_positions = set(random.sample(available_positions, 5))  # Randomly select 5 positions for minigames

        # Load minigame marker image
        self.minigame_marker = pygame.transform.scale(pygame.image.load("src/assets/ghost.png"), (TILE_SIZE, TILE_SIZE))

        # Scale houses
        self.house_images = {
            1: pygame.transform.scale(pygame.image.load("src/assets/level1_2.png"), (TILE_SIZE + 20, TILE_SIZE + 20)),  
            2: pygame.transform.scale(pygame.image.load("src/assets/level2.png"), (TILE_SIZE + 20, TILE_SIZE + 20)),  
            3: pygame.transform.scale(pygame.image.load("src/assets/level3.png"), (TILE_SIZE + 20, TILE_SIZE + 20)),  
        }

    def draw(self, screen):
        """Draws the board, properties, and player-owned properties"""
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                x, y = col * TILE_SIZE, row * TILE_SIZE

                if row == 0 or row == BOARD_SIZE - 1 or col == 0 or col == BOARD_SIZE - 1:
                    if (row, col) in self.property_positions:
                        pygame.draw.rect(screen, PROPERTY_BORDER, (x, y, TILE_SIZE, TILE_SIZE), 6)
                    else:
                        pygame.draw.rect(screen, BLACK, (x, y, TILE_SIZE, TILE_SIZE), 6)

        # Draw minigame markers
        for pos in self.minigame_positions:
            x, y = pos[1] * TILE_SIZE, pos[0] * TILE_SIZE
            screen.blit(self.minigame_marker, (x, y))

        # Draw owned properties
        for pos, property_obj in self.properties.items():
            x, y = pos[1] * TILE_SIZE, pos[0] * TILE_SIZE

            if property_obj.owner:
                border_color = PLAYER_COLORS[property_obj.owner]
                pygame.draw.rect(screen, border_color, (x, y, TILE_SIZE, TILE_SIZE), 6)

                if property_obj.level in self.house_images:
                    house_image = self.house_images[property_obj.level]
                    screen.blit(house_image, (x - 10, y - 15))  # Adjusted placement

                self.draw_level_dots(screen, x, y, property_obj.level, border_color)

    def draw_level_dots(self, screen, x, y, level, color):
        """Draws small dots in the top-right corner to indicate property level"""
        dot_radius = 7  
        dot_spacing = 15  

        for i in range(level):  
            pygame.draw.circle(screen, color, (x + TILE_SIZE - 15 - (i * dot_spacing), y + 15), dot_radius)
