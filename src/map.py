import pygame
import random
from settings import BOARD_SIZE, TILE_SIZE, BLUE, PLAYER_COLORS, MOVEMENT_PATH, SCREEN_HEIGHT, SCREEN_WIDTH, PROPERTY_BORDER
from property import Property

class Map:
    def __init__(self):
        """Initialize map with randomly assigned property positions"""
        self.property_positions = set(random.sample(MOVEMENT_PATH, 20))  # Randomly selected property spots
        self.properties = {}  # No properties at the start
        self.house_images = {
            1: pygame.transform.scale(pygame.image.load("assets/level1.png"), (int(TILE_SIZE * 0.6), int(TILE_SIZE * 0.6))),
            2: pygame.transform.scale(pygame.image.load("assets/level2.png"), (int(TILE_SIZE * 0.8), int(TILE_SIZE * 0.8))),
            3: pygame.transform.scale(pygame.image.load("assets/level3.png"), (TILE_SIZE - 10, TILE_SIZE - 10)),
        }
        self.background_image = pygame.image.load("assets/background.jpg")
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def draw(self, screen):
        """Draws the board, properties, and player-owned properties"""
        screen.blit(self.background_image, (0, 0))  # Background image

        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                x, y = col * TILE_SIZE, row * TILE_SIZE

                # Draw board edges only
                if row == 0 or row == BOARD_SIZE - 1 or col == 0 or col == BOARD_SIZE - 1:
                    pygame.draw.rect(screen, BLUE, (x, y, TILE_SIZE, TILE_SIZE), 6)

                if (row, col) in self.property_positions:
                    pygame.draw.rect(screen, PROPERTY_BORDER, (x, y, TILE_SIZE, TILE_SIZE), 6)  # White border by default

        # Draw owned properties
        for pos, property_obj in self.properties.items():
            x, y = pos[1] * TILE_SIZE, pos[0] * TILE_SIZE

            if property_obj.owner:
                border_color = PLAYER_COLORS[property_obj.owner]  # Get the owner's color
                pygame.draw.rect(screen, border_color, (x, y, TILE_SIZE, TILE_SIZE), 6)  # Draw property border

                # Draw house if upgraded
                if property_obj.level in self.house_images:
                    house_image = self.house_images[property_obj.level]
                    screen.blit(house_image, (x + 10, y + 10))

    def get_property(self, pos):
        """Return a property if it exists at the position, otherwise create one"""
        if pos not in self.properties:
            self.properties[pos] = Property(pos)  # Create property when landed on for the first time
        return self.properties[pos]
