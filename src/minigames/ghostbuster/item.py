import pygame
from .settings import *
from .camera import *

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, item_type):
        super().__init__()
        self.x = x
        self.y = y
        self.size = TILE_SIZE
        self.item_type = item_type
        self.spawn_time = pygame.time.get_ticks()

        if self.item_type == 'bullet':
            self.image = pygame.image.load("src/minigames/ghostbuster/assets/items/item_bullet.png").convert_alpha()
        elif self.item_type == 'health':
            self.image = pygame.image.load("src/minigames/ghostbuster/assets/items/item_health.png").convert_alpha()

        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def update(self, delta_time):
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_time >= ITEM_EXPIRATION_TIME:
            self.kill() 

    def render(self, screen, camera):
        screen.blit(self.image, (self.rect.x - camera.offset_x, self.rect.y - camera.offset_y))
