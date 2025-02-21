import pygame
from .settings import *
from .utility import *
import random
from .item import *

class Ghost(pygame.sprite.Sprite):
    def __init__(self, x, y, item_group, game):
        super().__init__()
        self.size = GHOST_SIZE
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(x, y)) 
        self.speed = GHOST_SPEED 
        self.health = GHOST_HEALTH
        self.last_attack_time = 0
        self.attack_cooldown = GHOST_ATTACK_COOLDOWN
        self.item_group = item_group
        self.game = game  # Add game instance

        self.animations = {
            "front": [pygame.transform.scale(pygame.image.load(f"src/minigames/ghostbuster/assets/ghost/front_{i}.png").convert_alpha(), (self.size, self.size)) for i in range(1, 5)],
            "back": [pygame.transform.scale(pygame.image.load(f"src/minigames/ghostbuster/assets/ghost/back_{i}.png").convert_alpha(), (self.size, self.size)) for i in range(1, 5)],
            "left": [pygame.transform.scale(pygame.image.load(f"src/minigames/ghostbuster/assets/ghost/left_{i}.png").convert_alpha(), (self.size, self.size)) for i in range(1, 5)],
            "right": [pygame.transform.scale(pygame.image.load(f"src/minigames/ghostbuster/assets/ghost/right_{i}.png").convert_alpha(), (self.size, self.size)) for i in range(1, 5)],
            "attack_left": [pygame.transform.scale(pygame.image.load(f"src/minigames/ghostbuster/assets/ghost/attack_left_{i}.png").convert_alpha(), (self.size, self.size)) for i in range(1, 5)],
            "attack_right": [pygame.transform.scale(pygame.image.load(f"src/minigames/ghostbuster/assets/ghost/attack_right_{i}.png").convert_alpha(), (self.size, self.size)) for i in range(1, 5)],
            "die": [pygame.transform.scale(pygame.image.load(f"src/minigames/ghostbuster/assets/ghost/die_{i}.png").convert_alpha(), (self.size, self.size)) for i in range(1, 5)],
            "hit": [pygame.transform.scale(pygame.image.load(f"src/minigames/ghostbuster/assets/ghost/ghost_hit_{i}.png").convert_alpha(), (self.size, self.size)) for i in range(1, 7)]
        }

        self.health_images = [
            pygame.image.load(f"src/minigames/ghostbuster/assets/ghost/health_bar_{i}.png").convert_alpha() for i in range(3, 0, -1)
        ]

        self.current_animation = self.animations["front"]
        self.image = self.current_animation[0]
        self.rect = self.image.get_rect(center=(x, y))
        self.hitbox_rect = self.rect.copy()
        self.velocity = pygame.math.Vector2(0, 0)  

        self.frame_index = 0
        self.animation_speed = 0.2 
        self.time_since_last_frame = 0  
        self.is_attacking = False
        self.is_dying = False
        self.is_hit = False
        self.hit_frame_index = 0
        self.hit_time_since_last_frame = 0

    def update(self, player, delta_time):
        if self.game.game_over or self.game.won:
            return
        
        if not self.is_dying:
            # Move ghost towards the player
            direction = pygame.math.Vector2(player.pos) - pygame.math.Vector2(self.rect.center)
            if direction.length() > 0:
                direction = direction.normalize()
            self.rect.center += direction * self.speed
            # print(f"Ghost position: {self.rect.center}, Moving towards: {player.pos}")

            self.update_direction(direction)
        self.animate(delta_time)
    
    def update_direction(self, direction):
        if self.is_attacking or self.is_dying or self.is_hit:
            return
        if direction.x > 0 and direction.y == 0:  # Moving right
            self.current_animation = self.animations["right"]
        elif direction.x < 0 and direction.y == 0:  # Moving left
            self.current_animation = self.animations["left"]
        elif direction.y > 0 and direction.x == 0:  # Moving down
            self.current_animation = self.animations["front"]
        elif direction.y < 0 and direction.x == 0:  # Moving up
            self.current_animation = self.animations["back"]
        elif direction.x > 0 and direction.y > 0:  # Moving bottom right
            self.current_animation = self.animations["right"]
        elif direction.x > 0 and direction.y < 0:  # Moving top right
            self.current_animation = self.animations["right"]
        elif direction.x < 0 and direction.y > 0:  # Moving bottom left
            self.current_animation = self.animations["left"]
        elif direction.x < 0 and direction.y < 0:  # Moving top left
            self.current_animation = self.animations["left"]
    
    def animate(self, delta_time):
        self.time_since_last_frame += delta_time
        if self.time_since_last_frame >= self.animation_speed:
            self.time_since_last_frame = 0
            self.frame_index = (self.frame_index + 1) % len(self.current_animation)
            self.image = self.current_animation[self.frame_index]

            # Reset attack animation
            if self.is_attacking and self.frame_index == 0:
                self.is_attacking = False
                self.update_direction(self.velocity) 

            # Check if dying animation is complete
            if self.is_dying and self.frame_index == len(self.current_animation) - 1:
                self.kill()
                self.game.ghost_killed += 1
                print(self.game.ghost_killed)

        # Update hit animation frame index based on time
        if self.is_hit:
            self.hit_time_since_last_frame += delta_time
            if self.hit_time_since_last_frame >= self.animation_speed:
                self.hit_time_since_last_frame = 0
                self.hit_frame_index = (self.hit_frame_index + 1) % len(self.animations["hit"])
                if self.hit_frame_index == 0:
                    self.is_hit = False  

    def can_attack(self):
        current_time = pygame.time.get_ticks()
        return current_time - self.last_attack_time >= self.attack_cooldown
    
    def attack(self, player):
        if self.can_attack():
            self.last_attack_time = pygame.time.get_ticks()
            self.is_attacking = True
            if self.current_animation == self.animations["left"]:
                self.current_animation = self.animations["attack_left"]
            elif self.current_animation == self.animations["right"]:
                self.current_animation = self.animations["attack_right"]
            self.frame_index = 0  
            player.take_damage()

    def take_damage(self):
        self.health -= 1
        print(f"Ghost hit! Health remaining: {self.health}")
        if self.health > 0:
            self.is_hit = True
            self.hit_frame_index = 0 
        else:
            print("Ghost defeated!")
            self.is_dying = True
            self.current_animation = self.animations["die"]
            self.frame_index = 0  
            drop_chance = random.random()
            if 0 <= drop_chance < 0.25:
                for _ in range(3):
                    bullet_item = Item(self.rect.x, self.rect.y, 'bullet')
                    self.item_group.add(bullet_item)
            elif 0.25 <= drop_chance < 0.50:
                health_item = Item(self.rect.x, self.rect.y, 'health')
                self.item_group.add(health_item)

    def render(self, screen, camera):
        screen.blit(self.image, (self.rect.x - camera.offset_x, self.rect.y - camera.offset_y))
        if self.is_hit:
            hit_image = self.animations["hit"][self.hit_frame_index]
            screen.blit(hit_image, (self.rect.x - camera.offset_x, self.rect.y - camera.offset_y))
        if not self.is_dying:
            health_bar_width = TILE_SIZE
            health_bar_height = 10
            health_bar_x = self.rect.x - camera.offset_x + (self.rect.width - health_bar_width) // 2
            health_bar_y = self.rect.y - camera.offset_y - health_bar_height - 5
            draw_health_bar(screen, health_bar_x, health_bar_y, self.health, GHOST_HEALTH, self.health_images)