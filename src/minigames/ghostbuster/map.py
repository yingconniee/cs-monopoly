import pygame
from .settings import TILE_SIZE

class Map:
    def __init__(self, layout):
        self.layout = layout
        self.tile_size = TILE_SIZE
        self.width = len(layout[0]) * TILE_SIZE
        self.height = len(layout) * TILE_SIZE

        self.floor_image = pygame.image.load("src/minigames/ghostbuster/assets/map/floor.png").convert_alpha()
        self.wall_images = {
            "left": pygame.image.load("src/minigames/ghostbuster/assets/map/wall_left.png").convert_alpha(),
            "right": pygame.image.load("src/minigames/ghostbuster/assets/map/wall_right.png").convert_alpha(),
            "top": pygame.image.load("src/minigames/ghostbuster/assets/map/wall_top.png").convert_alpha(),
            "bottom": pygame.image.load("src/minigames/ghostbuster/assets/map/wall_bottom.png").convert_alpha(),
            "top_left": pygame.image.load("src/minigames/ghostbuster/assets/map/corner_top_left.png").convert_alpha(),
            "top_right": pygame.image.load("src/minigames/ghostbuster/assets/map/corner_top_right.png").convert_alpha(),
            "bottom_left": pygame.image.load("src/minigames/ghostbuster/assets/map/corner_bottom_left.png").convert_alpha(),
            "bottom_right": pygame.image.load("src/minigames/ghostbuster/assets/map/corner_bottom_right.png").convert_alpha(),
        }

    def render(self, screen, camera):
        for row_index, row in enumerate(self.layout):
            for col_index, tile in enumerate(row):
                x = col_index * self.tile_size - camera.offset_x
                y = row_index * self.tile_size - camera.offset_y

                if row_index == 0 and col_index == 0:
                    screen.blit(self.wall_images["top_left"], (x, y))
                elif row_index == 0 and col_index == len(row) - 1:
                    screen.blit(self.wall_images["top_right"], (x, y))
                elif row_index == len(self.layout) - 1 and col_index == 0:
                    screen.blit(self.wall_images["bottom_left"], (x, y))
                elif row_index == len(self.layout) - 1 and col_index == len(row) - 1:
                    screen.blit(self.wall_images["bottom_right"], (x, y))
                elif row_index == 0:
                    screen.blit(self.wall_images["top"], (x, y))
                elif row_index == len(self.layout) - 1:
                    screen.blit(self.wall_images["bottom"], (x, y))
                elif col_index == 0:
                    screen.blit(self.wall_images["left"], (x, y))
                elif col_index == len(row) - 1:
                    screen.blit(self.wall_images["right"], (x, y))
                elif tile == 1:
                
                    left = self.layout[row_index][col_index - 1] if col_index > 0 else 0
                    right = self.layout[row_index][col_index + 1] if col_index < len(row) - 1 else 0
                    top = self.layout[row_index - 1][col_index] if row_index > 0 else 0
                    bottom = self.layout[row_index + 1][col_index] if row_index < len(self.layout) - 1 else 0

                    if left == 0 and right == 1 and top == 1 and bottom == 1:
                        screen.blit(self.wall_images["left"], (x, y))
                    elif left == 1 and right == 0 and top == 1 and bottom == 1:
                        screen.blit(self.wall_images["right"], (x, y))
                    elif left == 1 and right == 1 and top == 0 and bottom == 1:
                        screen.blit(self.wall_images["top"], (x, y))
                    elif left == 1 and right == 1 and top == 1 and bottom == 0:
                        screen.blit(self.wall_images["bottom"], (x, y))
                    elif left == 0 and right == 1 and top == 0 and bottom == 1:
                        screen.blit(self.wall_images["top_left"], (x, y))
                    elif left == 1 and right == 0 and top == 0 and bottom == 1:
                        screen.blit(self.wall_images["top_right"], (x, y))
                    elif left == 0 and right == 1 and top == 1 and bottom == 0:
                        screen.blit(self.wall_images["bottom_left"], (x, y))
                    elif left == 1 and right == 0 and top == 1 and bottom == 0:
                        screen.blit(self.wall_images["bottom_right"], (x, y))
                    else:
                        screen.blit(self.wall_images["top"], (x, y)) 
                elif tile == 2:
                    pygame.draw.rect(screen, (0, 0, 0), (x, y, self.tile_size, self.tile_size))
                else:
                    screen.blit(self.floor_image, (x, y))

    def is_wall(self, x, y):
        col = x // self.tile_size
        row = y // self.tile_size

        # Boundary check before accessing the map layout
        if 0 <= row < len(self.layout) and 0 <= col < len(self.layout[0]):
            return self.layout[int(row)][int(col)] == 1
        return False