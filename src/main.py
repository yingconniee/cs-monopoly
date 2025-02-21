import pygame
from game import Game
from player import Player
from bot import Bot
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from bot import Grudger, Detective, Cheater
import random
import asyncio
import sys

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
background_image = pygame.image.load("assets/background.png")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load images
player_images = {
    "Player1": pygame.image.load("assets/student.png"),
    "Player2": pygame.image.load("assets/player2.png"),
    "Player3": pygame.image.load("assets/player3.png"),
    "Player4": pygame.image.load("assets/player4.png"),
}

starting_pos = [10, 10]
player_offsets = [(5, 5), (35, 5), (5, 35), (35, 35)]

def start_screen(screen, game):
    """Display the start screen and get game mode and number of players"""
    pygame.font.init()
    font = pygame.font.Font(None, 36)
    title_font = pygame.font.Font(None, 72)

    title_text = title_font.render("Monopoly Game", True, (0, 0, 0))
    single_player_text = font.render("1. Single Player", True, (0, 0, 0))
    multiplayer_text = font.render("2. Multiplayer", True, (0, 0, 0))

    screen.blit(background_image, (0, 0))
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 4))
    screen.blit(single_player_text, (SCREEN_WIDTH // 2 - single_player_text.get_width() // 2, SCREEN_HEIGHT // 2))
    screen.blit(multiplayer_text, (SCREEN_WIDTH // 2 - multiplayer_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
    pygame.display.flip()

    waiting = True
    game_mode = None
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    game_mode = "single"
                    waiting = False
                elif event.key == pygame.K_2:
                    game_mode = "multi"
                    waiting = False

    return game_mode

def get_number_of_players(screen):
    """Ask the user for the number of players in multiplayer mode"""
    pygame.font.init()
    font = pygame.font.Font(None, 36)
    prompt_text = font.render("Enter number of players (2-4):", True, (0, 0, 0))

    screen.blit(background_image, (0, 0))
    screen.blit(prompt_text, (SCREEN_WIDTH // 2 - prompt_text.get_width() // 2, SCREEN_HEIGHT // 2))
    pygame.display.flip()

    waiting = True
    num_players = None
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.unicode.isdigit():
                    num_players = int(event.unicode)
                    if 2 <= num_players <= 4:
                        waiting = False

    return num_players

# Initialize game with an empty list of players to draw the map
async def main():
    game = Game(screen, [], background_image)
    game_mode = start_screen(screen, game)

    # Determine number of players and bots
    if game_mode == "single":
        num_players = 1
        num_bots = 3
    else:
        num_players = get_number_of_players(screen)
        num_bots = 4 - num_players

    players = []
    used_images = dict()

    for i in range(num_players):
        player_name = f"Player{i+1}"
        player_image = player_images[player_name]
        used_images[player_name] = player_image  # Mark as used
        players.append(Player(player_name, player_image, starting_pos, player_offsets[i]))

    #for i in range(num_bots):
    # players.append(Bot(f"Bot{i+1}", player_images[f"Player{num_players + i + 1}"], starting_pos, player_offsets[num_players + i]))
    # Add specialized bots based on available slots

    # Filter available images that were not used by human players
    available_images = [img for name, img in player_images.items() if name not in used_images]

    # Randomly select `num_bots` unique bot types
    selected_bot_types = random.sample([Grudger, Detective, Cheater], num_bots)

    # Assign a unique image to each selected bot
    selected_bots = []
    for i, bot_class in enumerate(selected_bot_types):
        bot = bot_class(bot_class.__name__, available_images[i], starting_pos, player_offsets[i + num_players])
        selected_bots.append(bot)

    # Add the required number of bots
    players.extend(selected_bots)  # Ensures the correct number of bots are added

    game = Game(screen, players, background_image)
    pygame.font.init()

    screen.blit(background_image, (0, 0))
    game.map.draw(screen)
    for player in players:
        player.draw(screen)
    pygame.display.flip()
    await asyncio.sleep(0)

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  

        screen.blit(background_image, (0, 0))  # Redraw background
        game.map.draw(screen)  # Redraw board
        for player in players:
            player.draw(screen)  # Draw all players

        game.display_money()  # Show player money

        pygame.display.flip()
        
        running = game.next_turn()  # Move to the next turn and check for game end

    
    pygame.quit()
    return

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())




