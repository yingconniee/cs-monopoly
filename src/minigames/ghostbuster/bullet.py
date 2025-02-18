import pygame
import math
from .settings import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, current_level):
        super().__init__()
        self.original_image = pygame.image.load("minigames/ghostbuster/assets/bullet/bullet.png").convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (40, 20))  # Adjust dimensions as needed
        self.image = pygame.transform.rotate(self.original_image, -angle)  # Rotate the image based on the angle
        self.rect = self.image.get_rect(center=(x, y))
        self.angle = angle
        self.speed = BULLET_SPEED
        self.velocity = pygame.math.Vector2(
            math.cos(math.radians(self.angle)),
            math.sin(math.radians(self.angle))
        ) * self.speed

        self.animations = {
            "hit": [pygame.transform.scale(pygame.image.load(f"minigames/ghostbuster/assets/ghost/ghost_hit_{i}.png").convert_alpha(), (40, 40)) for i in range(1, 7)]
        }
        self.is_hit = False
        self.hit_frame_index = 0
        self.hit_time_since_last_frame = 0
        self.animation_speed = 0.1  
        self.current_level = current_level

    def update(self, delta_time):
        if not self.is_hit:

            self.rect.center += self.velocity

            if not pygame.Rect(0, 0, MAP_WIDTH, MAP_HEIGHT).colliderect(self.rect):
                self.kill()
                return

            tile_x = self.rect.centerx // TILE_SIZE
            tile_y = self.rect.centery // TILE_SIZE
            curr_map_layout = MAP_LAYOUTS[self.current_level]

 
            if 0 <= tile_y < len(curr_map_layout) and 0 <= tile_x < len(curr_map_layout[0]):
                if curr_map_layout[tile_y][tile_x] == 1 or curr_map_layout[tile_y][tile_x] == 2:
                    self.is_hit = True
                    self.hit_frame_index = 0
                    self.hit_time_since_last_frame = 0
            else:
                self.kill()  
        else:
            self.hit_time_since_last_frame += delta_time
            if self.hit_time_since_last_frame >= self.animation_speed:
                self.hit_time_since_last_frame = 0
                self.hit_frame_index += 1
                if self.hit_frame_index >= len(self.animations["hit"]):
                    self.kill() 

    def render(self, screen, camera):
        if self.is_hit:
            hit_image = self.animations["hit"][self.hit_frame_index]
            screen.blit(hit_image, (self.rect.x - camera.offset_x, self.rect.y - camera.offset_y))
        else:
            screen.blit(self.image, (self.rect.x - camera.offset_x, self.rect.y - camera.offset_y))