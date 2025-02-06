import pygame
from dice import Dice
from map import Map
from settings import MOVEMENT_PATH

class Game:
    def __init__(self, screen, players, background_image):
        """Initialize the game"""
        self.screen = screen
        self.players = players
        self.map = Map()
        self.current_player_index = 0
        self.dice = Dice()
        self.background_image = background_image

    def next_turn(self):
        """Process the next player's turn"""
        current_player = self.players[self.current_player_index]

        if current_player.is_human:
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return False
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        roll = self.dice.roll(self.screen)
                        current_player.move(roll, self.screen, self.map, self.players)
                        self.map.get_property(tuple(current_player.pos)).interact(current_player, self.screen, self.map)
                        waiting = False
        else:
            roll = self.dice.roll(self.screen)
            current_player.move(roll, self.screen, self.map, self.players)
            self.map.get_property(tuple(current_player.pos)).interact(current_player, self.screen, self.map)

        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        return True
