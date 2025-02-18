import pygame
import os

# settings.py
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
FPS = 120

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Other settings
TILE_SIZE = 64

# Player Settings
PLAYER_START_POSITIONS = {
    0: (700, 700),
    1: (100, 100),
    2: (100, 100),
    3: (100, 100)
}
PLAYER_SIZE = 0.35
PLAYER_SPEED = 5
PLAYER_HEALTH = 5
GUN_OFFSET_X = 45
GUN_OFFSET_Y = 20
PLAYER_INITIAL_BULLET_COUNT = 100

# Bullet settings
BULLET_SPEED = 25
SHOOT_COOLDOWN = 20  # Frames between shots
SCREEN_RECT = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)  # Screen bounds

# Ghost settings
GHOST_SIZE = 100
GHOST_HEALTH = 3
GHOST_SPEED = 2
MAX_GHOSTS = 3
TOTAL_GHOSTS = 10
GHOST_SPAWN_COOLDOWN = 3000
GHOST_ATTACK_COOLDOWN = 5000

# Map settings
MAP_LAYOUT_0 = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]


MAP_LAYOUTS = [MAP_LAYOUT_0]

MAP_0_CHECKPOINT = [(9, 3), (10, 3), (9, 2), (10, 2)]
MAP_1_CHECKPOINT = [(40, 18), (40, 19), (40, 20), (40, 21), (40, 22), (40, 23), (40, 24)]
MAP_2_CHECKPOINT = [(1, 20), (1, 21), (1, 22), (1, 23)]
MAP_3_CHECKPOINT = [(13, 9), (13, 10), (13, 11)]

MAPS_CHECKPOINTS = [MAP_0_CHECKPOINT, MAP_1_CHECKPOINT, MAP_2_CHECKPOINT, MAP_3_CHECKPOINT]

MAP_WIDTH = len(MAP_LAYOUT_0[0]) * TILE_SIZE
MAP_HEIGHT = len(MAP_LAYOUT_0) * TILE_SIZE

# Item settings
ITEM_EXPIRATION_TIME = 10000

# Font settings
FONT_PATH = 'minigames/ghostbuster/assets/fonts/antiquity-print.ttf'
FONT_SIZE = 24

# background_image = pygame.image.load("minigames/ghostbuster/assets/background.tiff").convert()
# background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
