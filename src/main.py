import pygame
from game import Game
from player import Player
from bot import Bot
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
background_image = pygame.image.load("assets/background.tiff")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load images
player_images = {
    "Player1": pygame.image.load("assets/student.png"),
    "Bot2": pygame.image.load("assets/player2.png"),
    "Bot3": pygame.image.load("assets/player3.png"),
    "Bot4": pygame.image.load("assets/player4.png"),
}

starting_pos = [10, 10]
player_offsets = [(5, 5), (35, 5), (5, 35), (35, 35)]

players = [
    Player("Player1", player_images["Player1"], starting_pos, player_offsets[0]),
    Bot("Bot2", player_images["Bot2"], starting_pos, player_offsets[1]),
    Bot("Bot3", player_images["Bot3"], starting_pos, player_offsets[2]),
    Bot("Bot4", player_images["Bot4"], starting_pos, player_offsets[3]),
]

game = Game(screen, players, background_image)
pygame.font.init()

# Main loop
running = True
while running:
    game.map.draw(screen)  
    for player in players:
        player.draw(screen)

    pygame.display.flip()
    running = game.next_turn()

pygame.quit()
