import pygame
from .settings import *
from .game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("MCS Ghostbusters")
    clock = pygame.time.Clock()
    game_font = pygame.font.Font(FONT_PATH, FONT_SIZE)

    # background_image = pygame.image.load("assets/building/mcs_building.png").convert()
    # background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # pygame.mixer.music.load("assets/bgm/MCS_Ghostbuster_BGM.mp3")
    # pygame.mixer.music.play(-1)  # Play the music in a loop

    # pygame.mixer.music.stop()

    # pygame.mixer.music.load("assets/bgm/Game_BGM.mp3")
    # pygame.mixer.music.play(-1)

    game = Game(screen, game_font)

    running = True
    while running:
        clock.tick(FPS)
        delta_time = clock.tick(60) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if game.game_over:
                running = False
                game.display_game_over()
                pygame.time.delay(3000)
                return game.won
            elif game.won:
                running = False
                game.display_winner()
                pygame.time.delay(3000)
                return game.won
                
        game.update(delta_time)
        game.render()

    pygame.quit()


if __name__ == "__main__":
    main()
