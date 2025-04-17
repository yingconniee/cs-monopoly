import pygame
import random
import asyncio
import sys

from src.game import Game
from src.player import Player
from src.bot import Grudger, Detective, Cheater
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
background_image = pygame.image.load("src/assets/background.png")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load images
player_images = {
    "Player1": pygame.image.load("src/assets/student.png"),
    "Player2": pygame.image.load("src/assets/player2.png"),
    "Player3": pygame.image.load("src/assets/player3.png"),
    "Player4": pygame.image.load("src/assets/player4.png"),
}

starting_pos = [10, 10]
player_offsets = [(5, 5), (35, 5), (5, 35), (35, 35)]

def start_screen(screen, game):
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
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    game_mode = "single"
                    waiting = False
                elif event.key == pygame.K_2:
                    game_mode = "multi"
                    waiting = False

    return game_mode

def choose_singleplayer_ai_mode(screen):
    pygame.font.init()
    font = pygame.font.Font(None, 36)
    title_font = pygame.font.Font(None, 64)

    title_text = title_font.render("Choose Your AI Opponent", True, (0, 0, 0))
    evo_ai_text = font.render("1. Trust of Evolution AI", True, (0, 0, 0))
    qlearn_ai_text = font.render("2. Q-Learning AI", True, (0, 0, 0))

    screen.blit(background_image, (0, 0))
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 3))
    screen.blit(evo_ai_text, (SCREEN_WIDTH // 2 - evo_ai_text.get_width() // 2, SCREEN_HEIGHT // 2))
    screen.blit(qlearn_ai_text, (SCREEN_WIDTH // 2 - qlearn_ai_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
    pygame.display.flip()

    waiting = True
    ai_mode = None
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    ai_mode = "evo"
                    waiting = False
                elif event.key == pygame.K_2:
                    ai_mode = "qlearning"
                    waiting = False

    return ai_mode

def get_number_of_players(screen):
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
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.unicode.isdigit():
                    num_players = int(event.unicode)
                    if 2 <= num_players <= 4:
                        waiting = False

    return num_players

# ================== MAIN GAME LOOP ====================

async def main():
    game = Game(screen, [], background_image)
    game_mode = start_screen(screen, game)
    players = []

    if game_mode == "single":
        ai_mode = choose_singleplayer_ai_mode(screen)
        players.append(Player("Player1", player_images["Player1"], starting_pos, player_offsets[0]))

        if ai_mode == "evo":
            players.append(Grudger("Grudger", player_images["Player2"], starting_pos, player_offsets[1]))
            players.append(Cheater("Cheater", player_images["Player3"], starting_pos, player_offsets[2]))
            players.append(Detective("Detective", player_images["Player4"], starting_pos, player_offsets[3]))
        elif ai_mode == "qlearning":
            from src.bot import QLearnerBot  # Make sure QLearnerBot is implemented
            players.append(QLearnerBot("QLearner", player_images["Player2"], starting_pos, player_offsets[1]))
            players.append(Cheater("Cheater", player_images["Player3"], starting_pos, player_offsets[2]))
            players.append(Grudger("Grudger", player_images["Player4"], starting_pos, player_offsets[3]))

    elif game_mode == "multi":
        num_players = get_number_of_players(screen)
        num_bots = 4 - num_players

        used_images = dict()
        for i in range(num_players):
            player_name = f"Player{i+1}"
            player_image = player_images[player_name]
            used_images[player_name] = player_image
            players.append(Player(player_name, player_image, starting_pos, player_offsets[i]))

        available_images = [img for name, img in player_images.items() if name not in used_images]
        selected_bot_types = random.sample([Grudger, Detective, Cheater], num_bots)

        for i, bot_class in enumerate(selected_bot_types):
            bot = bot_class(bot_class.__name__, available_images[i], starting_pos, player_offsets[i + num_players])
            players.append(bot)

    # Game Setup
    game = Game(screen, players, background_image)
    pygame.font.init()

    screen.blit(background_image, (0, 0))
    game.map.draw(screen)
    for player in players:
        player.draw(screen)
    pygame.display.flip()

    # Main Game Loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(background_image, (0, 0))
        game.map.draw(screen)
        for player in players:
            player.draw(screen)
        game.display_money()
        pygame.display.flip()

        running = game.next_turn()
        await asyncio.sleep(0)

    pygame.quit()

asyncio.run(main())
