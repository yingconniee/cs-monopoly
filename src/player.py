import pygame
from settings import TILE_SIZE, MOVEMENT_PATH
from minigames.ghostbuster.main import main as ghostbuster_main
from settings import SCREEN_HEIGHT, SCREEN_WIDTH

background_image = pygame.image.load("assets/background.tiff")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

class Player:
    def __init__(self, name, image, pos, offset, is_human=True):
        """Initialize player"""
        self.name = name
        self.image = pygame.transform.scale(image, (TILE_SIZE // 2, TILE_SIZE // 2))  
        self.pos = pos
        self.offset = offset
        self.is_human = is_human
        self.money = 10000  # Start money

    def take_turn(self, screen, game):
        """Handles player's turn with keyboard input"""
        if self.is_human:
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:  # Press SPACE to roll dice
                            roll = game.dice.roll(screen)
                            print(f"{self.name} rolled {roll}")
                            self.move(roll, screen, game)
                            waiting = False  # End turn after moving
                        if tuple(self.pos) in game.map.minigame_positions:
                                self.play_minigame(screen, game)

    
    def draw(self, screen):
        """Draws the player on the screen at the correct position"""
        x, y = self.pos[1] * TILE_SIZE + self.offset[0], self.pos[0] * TILE_SIZE + self.offset[1]
        screen.blit(self.image, (x, y))

    def move(self, steps, screen, game):
        """Move the player step-by-step along the path"""
        for _ in range(steps):
            if tuple(self.pos) in MOVEMENT_PATH:  # Ensure player is in movement path
                current_index = MOVEMENT_PATH.index(tuple(self.pos))
                new_index = (current_index + 1) % len(MOVEMENT_PATH)  # Loop around board
                self.pos = list(MOVEMENT_PATH[new_index])

                # Update the screen after each step
                screen.blit(game.background_image, (0, 0))  # Redraw background
                game.map.draw(screen)  # Redraw board
                for player in game.players:
                    player.draw(screen)  # Redraw all players

                pygame.display.flip()
                pygame.time.delay(300)  # Small delay for smooth animation
        
        property = game.map.properties.get(tuple(self.pos))
        if property:
            property.interact(self, screen, game.map, game)

    def play_minigame(self, screen, game):
        game_won = ghostbuster_main()

        if game_won:
            self.money += 500
        else:
            self.money -= 500
        
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(background_image, (0, 0))
        game.map.draw(screen)  
        for player in game.players:
            player.draw(screen)  

        pygame.display.flip()