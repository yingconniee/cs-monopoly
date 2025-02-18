import pygame
from .settings import *
from .bullet import *
from .utility import *

class Player(pygame.sprite.Sprite):
    def __init__(self, PLAYER_START_X, PLAYER_START_Y, PLAYER_SPEED, bullet_group, map, current_level, game_font):
        super().__init__()
        self.size = TILE_SIZE 
        self.speed = PLAYER_SPEED 
        self.pos = pygame.math.Vector2(PLAYER_START_X, PLAYER_START_Y) 
        self.health = PLAYER_HEALTH
        self.game_font = game_font

        self.animations = {
            "front": [pygame.image.load(f"minigames/ghostbuster/assets/player/front_{i}.png").convert_alpha() for i in range(1,5)],
            "back": [pygame.image.load(f"minigames/ghostbuster/assets/player/back_{i}.png").convert_alpha() for i in range(1,5)],
            "left": [pygame.image.load(f"minigames/ghostbuster/assets/player/left_{i}.png").convert_alpha() for i in range(1,5)],
            "right": [pygame.image.load(f"minigames/ghostbuster/assets/player/right_{i}.png").convert_alpha() for i in range(1,5)],
        }

        self.shooting_images = {
            "front": pygame.image.load("minigames/ghostbuster/assets/player/shooting_front.png").convert_alpha(),
            "back": pygame.image.load("minigames/ghostbuster/assets/player/shooting_back.png").convert_alpha(),
            "right": pygame.image.load("minigames/ghostbuster/assets/player/shooting_right.png").convert_alpha(),
            "left": pygame.transform.flip(pygame.image.load("minigames/ghostbuster/assets/player/shooting_right.png").convert_alpha(), True, False)
        }

        self.face_image = pygame.image.load("minigames/ghostbuster/assets/player/face.png").convert_alpha()

        self.health_images = [
            pygame.image.load(f"minigames/ghostbuster/assets/player/health_bar_{i}.png").convert_alpha() for i in range(5, 0, -1)
        ]

        # Initial image setup
        self.current_animation = self.animations["front"]
        self.image = self.current_animation[0]
        self.rect = self.image.get_rect(center=self.pos)
        self.hitbox_rect = self.rect.copy()
        self.velocity = pygame.math.Vector2(0, 0)  # Player velocity

        self.frame_index = 0
        self.animation_speed = 0.1  # Speed of animation cycling
        self.time_since_last_frame = 0  # Time tracker for animation updates
        self.is_moving = False
        self.is_shooting_animation = False
        self.shooting_timer = 0

        self.bullet_group = bullet_group
        self.shoot_cooldown = 0
        self.bullet_count = PLAYER_INITIAL_BULLET_COUNT
        self.angle = 0
        self.gun_barrel_offset = pygame.math.Vector2(GUN_OFFSET_X, GUN_OFFSET_Y)
        self.map = map
        self.current_level = current_level

    def user_input(self):
        self.velocity.x = 0
        self.velocity.y = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.velocity.y = -self.speed
        if keys[pygame.K_s]:
            self.velocity.y = self.speed
        if keys[pygame.K_a]:
            self.velocity.x = -self.speed
        if keys[pygame.K_d]:
            self.velocity.x = self.speed

        if self.velocity.length() > 0:
            self.velocity = self.velocity.normalize() * self.speed
        
        self.is_moving = self.velocity.length() > 0
    
    def is_shooting(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.shoot_cooldown == 0 and self.bullet_count > 0:
            self.shoot_cooldown = SHOOT_COOLDOWN
            self.bullet_count -= 1

            if self.angle == 0:  # Facing right
                offset = pygame.math.Vector2(self.rect.width // 2, 0)
                self.image = self.shooting_images["right"]
            elif self.angle == 180:  # Facing left
                offset = pygame.math.Vector2(-self.rect.width // 2, 0)
                self.image = self.shooting_images["left"]
            elif self.angle == 90:  # Facing down
                offset = pygame.math.Vector2(0, self.rect.height // 2)
                self.image = self.shooting_images["front"]
            elif self.angle == 270:  # Facing up
                offset = pygame.math.Vector2(0, -self.rect.height // 2)
                self.image = self.shooting_images["back"]
            else:  # Default 
                offset = pygame.math.Vector2(0, 0)

            spawn_bullet_pos = self.pos + offset
            bullet = Bullet(spawn_bullet_pos.x, spawn_bullet_pos.y, self.angle, self.current_level)
            # print(f"Player position: {self.pos}, Angle: {self.angle}, Gun Offset: {self.gun_barrel_offset}")
            # print(f"Bullet spawned at {spawn_bullet_pos} with angle {self.angle}")
            self.bullet_group.add(bullet)
            self.is_shooting_animation = True
            self.shooting_timer = 0.2


    def update_direction(self):
        if self.is_shooting_animation:
            return
        if self.velocity.x > 0 and self.velocity.y == 0:  # Moving right
            self.current_animation = self.animations["right"]
            self.angle = 0
        elif self.velocity.x < 0 and self.velocity.y == 0:  # Moving left
            self.current_animation = self.animations["left"]
            self.angle = 180
        elif self.velocity.y > 0 and self.velocity.x == 0:  # Moving down
            self.current_animation = self.animations["front"]
            self.angle = 90
        elif self.velocity.y < 0 and self.velocity.x == 0:  # Moving up
            self.current_animation = self.animations["back"]
            self.angle = 270
        elif self.velocity.length() > 0:  # Moving diagonally
            self.angle = (pygame.math.Vector2(1, 0).angle_to(self.velocity))


    def animate(self, delta_time):
        self.time_since_last_frame += delta_time
        if self.is_shooting_animation:
            self.shooting_timer -= delta_time
            if self.shooting_timer <= 0:
                self.is_shooting_animation = False
                self.update_direction() 
        elif self.is_moving:
            if self.time_since_last_frame >= self.animation_speed:
                self.time_since_last_frame = 0
                self.frame_index = (self.frame_index + 1) % len(self.current_animation)
                self.image = self.current_animation[self.frame_index]
        else:
            self.image = self.current_animation[0]
    
    def take_damage(self):
        self.health -= 1
        print(f"Player hit! Health remaining: {self.health}")
        if self.health <= 0:
            self.kill()

    def update(self, delta_time):
        self.user_input()  
        new_pos = self.pos + self.velocity  
        
        if not self.map.is_wall(new_pos.x, self.pos.y):
            self.pos.x = new_pos.x
        if not self.map.is_wall(self.pos.x, new_pos.y):
            self.pos.y = new_pos.y

        self.hitbox_rect.center = self.pos  
        self.rect.center = self.pos  
        self.update_direction()  
        self.animate(delta_time)
        self.is_shooting()

        self.rect.clamp_ip(pygame.Rect(0, 0, MAP_WIDTH, MAP_HEIGHT))

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1


    def render(self, screen, camera):
        # Draw the player image
        screen.blit(self.image, (self.rect.x - camera.offset_x, self.rect.y - camera.offset_y))

        # Draw the Player Face
        face_image_scaled = pygame.transform.scale(self.face_image, (100, 120))
        face_x = 10
        face_y = 10
        screen.blit(face_image_scaled, (face_x, face_y))

        # Draw a border around the face image
        border_color = (0, 0, 0)  
        border_rect = face_image_scaled.get_rect(topleft=(face_x, face_y))
        pygame.draw.rect(screen, border_color, border_rect, 2)

        # Draw the health bar
        health_bar_x = face_x + self.face_image.get_width() - 50
        health_bar_y = face_y
        draw_health_bar(screen, health_bar_x, health_bar_y, self.health, PLAYER_HEALTH, self.health_images, scale=3)

        # Draw the bullet count
        bullet_count_x = health_bar_x + 20
        bullet_count_y = health_bar_y + 40
        bullet_text = self.game_font.render(f"Bullets: {self.bullet_count}", True, (255, 255, 255))
        screen.blit(bullet_text, (bullet_count_x, bullet_count_y))
