import pygame

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
BOARD_SIZE = 11  # 11x11 grid
TILE_SIZE = 70
PLAYER_SIZE = 30
FPS = 30

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Setup the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Monopoly Game Board with Background")

# Load background image
background_path = "C:\\User\\Download\\background.jpg"  # Replace with your image path
background_image = pygame.image.load(background_path)
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Scale to fit screen

# Draw the board
def draw_board():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            x = col * TILE_SIZE
            y = row * TILE_SIZE
            if row == 0 or row == BOARD_SIZE - 1 or col == 0 or col == BOARD_SIZE - 1:
                pygame.draw.rect(screen, BLUE, (x, y, TILE_SIZE, TILE_SIZE), 2)  # Grid
                font = pygame.font.Font(None, 24)
                label = f"({row}, {col})"
                text = font.render(label, True, BLACK)
                screen.blit(text, (x + 10, y + 10))

# Player
player_pos = [10 * TILE_SIZE, 10 * TILE_SIZE]

def draw_player():
    pygame.draw.rect(screen, RED, (player_pos[0] + 20, player_pos[1] + 20, PLAYER_SIZE, PLAYER_SIZE))

# Game Loop
def main():
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Handle movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and player_pos[1] > TILE_SIZE:
            player_pos[1] -= TILE_SIZE
        if keys[pygame.K_DOWN] and player_pos[1] < SCREEN_HEIGHT - 2 * TILE_SIZE:
            player_pos[1] += TILE_SIZE
        if keys[pygame.K_LEFT] and player_pos[0] > TILE_SIZE:
            player_pos[0] -= TILE_SIZE
        if keys[pygame.K_RIGHT] and player_pos[0] < SCREEN_WIDTH - 2 * TILE_SIZE:
            player_pos[0] += TILE_SIZE

        # Draw everything
        screen.blit(background_image, (0, 0))  # Background
        draw_board()  # Board
        draw_player()  # Player
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
