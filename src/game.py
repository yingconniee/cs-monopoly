import pygame
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from map import Map
from dice import Dice

class Game:
    def __init__(self, screen, players, background_image):
        """Initialize the game"""
        self.screen = screen
        self.players = players
        self.background_image = background_image
        self.current_turn = 0
        self.max_rounds = 10
        self.running = True

        # Initialize the game map
        self.map = Map()

        # Initialize dice
        self.dice = Dice()

        # Give each player $10,000 at the start
        for player in self.players:
            player.money = 10000

    def next_turn(self):
        """Advances to the next player's turn and checks for win condition"""
        # if self.current_turn >= self.max_rounds:
        #     self.show_winner_popup()
        #     return False  # End game

        if len(self.players) == 1:  # If only one player is left, they win
            self.show_winner_popup()
            return False

        current_player = self.players[self.current_turn % len(self.players)]
        current_player.take_turn(self.screen, self)  # Player takes their turn

        self.current_turn += 1  # Move to next turn
        return True  # Continue game

    def get_winner(self):
        """Determines the player with the most money"""
        return max(self.players, key=lambda player: player.money)  # Find the richest player

    def get_player_by_name(self, name):
        """Find player by name"""
        for player in self.players:
            if player.name == name:
                return player
        return None

    def remove_player(self, player):
        """Removes a player if they go bankrupt"""
        self.players.remove(player)
        self.show_popup(f"{player.name} has lost!")

    def show_popup(self, message):
        """Displays a popup message"""
        font = pygame.font.Font(None, 32)
        popup_surface = pygame.Surface((400, 120))
        popup_surface.fill((255, 255, 255))
        pygame.draw.rect(popup_surface, (0, 0, 0), popup_surface.get_rect(), 3)

        text_surface = font.render(message, True, (0, 0, 0))
        popup_surface.blit(text_surface, (20, 50))

        self.screen.blit(popup_surface, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 60))
        pygame.display.flip()
        pygame.time.wait(2000)  # Show for 2 seconds before continuing

    def display_money(self):
        """Display players' money in four boxes under the dice"""
        font = pygame.font.Font(None, 30)  # Font for text
        box_width = 130  # Width of each box
        box_height = 60  # Height of each box
        box_spacing = 20  # Space between boxes

        # Calculate starting position for centering boxes
        total_width = (box_width * len(self.players)) + (box_spacing * (len(self.players) - 1))
        start_x = (SCREEN_WIDTH - total_width) // 2  # Centered horizontally
        box_y = SCREEN_HEIGHT - 200  # Position above bottom

        for i, player in enumerate(self.players):
            box_x = start_x + (i * (box_width + box_spacing))  # Position each box

            # Draw rectangle box
            pygame.draw.rect(self.screen, (200, 200, 200), (box_x, box_y, box_width, box_height), border_radius=8)
            pygame.draw.rect(self.screen, (0, 0, 0), (box_x, box_y, box_width, box_height), 3, border_radius=8)  # Black border

            # Render player name
            name_text = font.render(player.name, True, (0, 0, 0))
            self.screen.blit(name_text, (box_x + 10, box_y + 10))

            # Render player money
            money_text = font.render(f"${player.money}", True, (0, 0, 0))
            self.screen.blit(money_text, (box_x + 10, box_y + 35))
