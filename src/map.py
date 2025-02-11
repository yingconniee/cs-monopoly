import pygame
import random
from settings import BOARD_SIZE, TILE_SIZE, BLUE, PLAYER_COLORS, MOVEMENT_PATH, SCREEN_HEIGHT, SCREEN_WIDTH, PROPERTY_BORDER
from property import Property

class Map:
    def __init__(self):
        """Initialize map with randomly assigned property positions"""
        self.property_positions = set(random.sample(MOVEMENT_PATH, 20))
        self.properties = {}

        # Assign unique property names
        self.property_names = {pos: f"MCS{index:03d}" for index, pos in enumerate(self.property_positions, start=1)}

        # Scale houses
        self.house_images = {
            1: pygame.transform.scale(pygame.image.load("assets/level1.png"), (TILE_SIZE + 50, TILE_SIZE + 50)),  
            2: pygame.transform.scale(pygame.image.load("assets/level2.png"), (TILE_SIZE + 50, TILE_SIZE + 50)),  
            3: pygame.transform.scale(pygame.image.load("assets/level3.png"), (TILE_SIZE + 50, TILE_SIZE + 50)),  
        }

    def draw(self, screen):
        """Draws the board, properties, and player-owned properties"""
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                x, y = col * TILE_SIZE, row * TILE_SIZE

                if (row, col) in self.property_positions:
                    pygame.draw.rect(screen, PROPERTY_BORDER, (x, y, TILE_SIZE, TILE_SIZE), 6)

        # Draw owned properties
        for pos, property_obj in self.properties.items():
            x, y = pos[1] * TILE_SIZE, pos[0] * TILE_SIZE

            if property_obj.owner:
                border_color = PLAYER_COLORS[property_obj.owner]
                pygame.draw.rect(screen, border_color, (x, y, TILE_SIZE, TILE_SIZE), 6)

                if property_obj.level in self.house_images:
                    house_image = self.house_images[property_obj.level]
                    screen.blit(house_image, (x - 25, y - 25))  # Adjusted placement

                self.draw_level_dots(screen, x, y, property_obj.level, border_color)

    def draw_level_dots(self, screen, x, y, level, color):
        """Draws small dots in the top-right corner to indicate property level"""
        dot_radius = 7  
        dot_spacing = 15  

        for i in range(level):  
            pygame.draw.circle(screen, color, (x + TILE_SIZE - 15 - (i * dot_spacing), y + 15), dot_radius)
