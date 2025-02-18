import pygame

def draw_health_bar(screen, x, y, health, max_health, health_images, scale=2):
    health = max(0, min(health, max_health))

    health_image = health_images[health - 1]

    if scale != 1.0:
        width = int(health_image.get_width() * scale)
        height = int(health_image.get_height() * scale)
        health_image = pygame.transform.scale(health_image, (width, height))

    screen.blit(health_image, (x, y))


def draw_text(screen, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)