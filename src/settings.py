# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
BOARD_SIZE = 11  # 11x11 grid
TILE_SIZE = 70
PLAYER_SIZE_SMALL = 30
PLAYER_SIZE_LARGE = 40
FPS = 5  # Slower FPS for better visibility

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
PROPERTY_BORDER = (255, 255, 255)  
OWNED_PROPERTY_COLOR = (255, 255, 255, 128)  

# Map
MOVEMENT_PATH = (
    [(10, i) for i in range(10, -1, -1)] +
    [(i, 0) for i in range(9, -1, -1)] +
    [(0, i) for i in range(1, 11)] +
    [(i, 10) for i in range(1, 11)]
)

# Players

PLAYER_COLORS = { 
    "Player1": (255, 0, 0),  
    "Bot2": (0, 255, 0),    
    "Bot3": (252, 15, 192), 
    "Bot4": (255, 255, 0)  
}