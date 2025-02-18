import pygame
import sys
import os
from .level import Level
from .settings import *
from .camera import Camera


class Game:
    def __init__(self, screen, game_font):
        self.screen = screen
        self.bullet_group = pygame.sprite.Group()
        self.ghost_group = pygame.sprite.Group()
        self.item_group = pygame.sprite.Group()
        self.game_font = game_font
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT, MAP_WIDTH, MAP_HEIGHT)
        self.level = Level(self, self.bullet_group, self.ghost_group, self.item_group, self.game_font, screen)
        self.game_over = False
        self.ghost_killed = 0
        self.won = False

    def update(self, delta_time):
        self.level.update(delta_time)
        self.bullet_group.update(delta_time)
        self.item_group.update(delta_time)
        self.camera.update(self.level.player)

        if not self.level.player.alive or self.level.player.health <= 0:
            self.game_over = True
        elif self.ghost_killed >= TOTAL_GHOSTS:
            self.won = True
        else:
            self.level.update(delta_time)

    def render(self):
        if self.game_over:
            self.display_game_over()
        elif self.won:
            self.display_winner()
        else:
            self.screen.fill((0, 0, 0))
            self.level.render(self.screen, self.camera)
            pygame.display.flip()

    def display_game_over(self):
        self.screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 74)
        text = font.render("GAME OVER", True, (255, 0, 0))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()

    def display_winner(self):
        self.screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 74)
        text = font.render("YOU WIN!", True, (0, 255, 0))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
