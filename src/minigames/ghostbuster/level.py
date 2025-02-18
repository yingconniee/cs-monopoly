import pygame
from .player import Player
from .ghost import Ghost
from .item import Item
import random
from .settings import *
from .map import Map
import sys
from .utility import draw_text

class Level:
    def __init__(self, game, bullet_group, ghost_group, item_group, game_font, screen):
        # Initialize player
        self.bullet_group = bullet_group

        # Ghost settings
        self.ghost_group = ghost_group
        self.max_ghosts = MAX_GHOSTS
        
        self.ghost_spawn_cooldown = GHOST_SPAWN_COOLDOWN
        self.last_ghost_spawn_time = pygame.time.get_ticks()

        # Generate items
        self.item_group = item_group

        # Initialize map
        self.screen = screen
        self.map = Map(MAP_LAYOUTS[0])  # Use the first layout
        
        # Game Font
        self.game_font = game_font
        player_start_pos_x, player_start_pos_y = PLAYER_START_POSITIONS[0]
        self.player = Player(player_start_pos_x, player_start_pos_y, PLAYER_SPEED, bullet_group, self.map, 0, self.game_font)

        self.game = game
        self.ghost_killed = 0

        self.spawn_initial_ghosts()

    def generate_random_ghost_position(self):
        while True:
            x = random.randint(40, SCREEN_WIDTH - 40)
            y = random.randint(40, SCREEN_HEIGHT - 40)
            
            if abs(x - self.player.pos.x) > 100 and abs(y - self.player.pos.y) > 100:
                return x, y
    
    def spawn_ghost(self):
        if len(self.ghost_group) < self.max_ghosts:
            x, y = self.generate_random_ghost_position()
            ghost = Ghost(x, y, self.item_group, self.game)
            self.ghost_group.add(ghost)
    
    def spawn_initial_ghosts(self):
        for _ in range(self.max_ghosts):
            self.spawn_ghost()

    def update(self, delta_time):
        if self.game.game_over or self.game.won:
            return
        
        # Check if player is alive
        if self.player.health > 0:
            self.player.update(delta_time)
            self.ghost_group.update(self.player, delta_time)

            # Check for collisions between player and ghosts, attack if colliding
            for ghost in self.ghost_group:
                if pygame.sprite.collide_rect(self.player, ghost):
                    ghost.attack(self.player)

            # Check for collisions between ghosts and bullets, take damage if colliding
            collisions = pygame.sprite.groupcollide(self.bullet_group, self.ghost_group, True, False)
            for bullet, hit_ghosts in collisions.items():
                for ghost in hit_ghosts:
                    ghost.take_damage()

            # Check for collisions between player and items
            item_collisions = pygame.sprite.spritecollide(self.player, self.item_group, True)
            for item in item_collisions:
                if item.item_type == 'bullet':
                    self.player.bullet_count += 1
                elif item.item_type == 'health':
                    self.player.health = min(self.player.health + 1, PLAYER_HEALTH)

            self.bullet_group.update(delta_time)

            # Spawn new ghosts based on cooldown
            current_time = pygame.time.get_ticks()
            if current_time - self.last_ghost_spawn_time > self.ghost_spawn_cooldown:
                self.spawn_ghost()
                self.last_ghost_spawn_time = current_time

    def render(self, screen, camera):
        self.map.render(screen, camera)
        self.player.render(screen, camera)
        for bullet in self.bullet_group:
            bullet.render(screen, camera)
        for ghost in self.ghost_group:
            ghost.render(screen, camera)
        for item in self.item_group:
            item.render(screen, camera)


