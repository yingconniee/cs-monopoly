import pygame
import random
from settings import SCREEN_HEIGHT, SCREEN_WIDTH

class Property:
    def __init__(self, position):
        """Initialize property"""
        self.position = position
        self.owner = None  # No owner at start
        self.level = 0  # No house at start

    def buy(self, player):
        """Allows a player to buy the property if it's unowned"""
        if self.owner is None:  # If not owned, allow purchase
            self.owner = player.name
            self.level = 1

    def upgrade(self, player, screen):
        """Ask the player if they want to upgrade (max level 3)"""
        if self.owner == player.name and self.level < 3:
            if player.is_human:
                self.show_upgrade_popup(screen, player)
            else:
                self.level += 1

    def interact(self, player, screen, game_map):
        """Handles interaction when a player lands on a property"""
        pos = tuple(player.pos)

        if pos in game_map.property_positions:  # 🔥 Only allow buying/upgrading on valid property positions
            if self.owner is None:  
                if player.is_human:
                    self.show_buy_popup(screen, player)
                else:    
                    self.buy(player)
            elif self.owner == player.name and self.level < 3:  
                self.upgrade(player, screen)

    def show_buy_popup(self, screen, player):
        """Display a popup asking the player if they want to buy the property"""
        self.show_popup(screen, f"{player.name}, Buy this property?", "Y/N", lambda: self.buy(player))

    def show_upgrade_popup(self, screen, player):
        """Display a popup asking the player if they want to upgrade"""
        self.show_popup(screen, f"{player.name}, Upgrade property to Level {self.level + 1}?", "Y/N", lambda: self.level_up())

    def show_popup(self, screen, message, instructions, on_confirm):
        """Reusable function for buy/upgrade popups"""
        pygame.font.init()
        font = pygame.font.Font(None, 28)  
        popup_width, popup_height = 420, 140  
        popup_surface = pygame.Surface((popup_width, popup_height))
        popup_surface.fill((255, 255, 255))
        pygame.draw.rect(popup_surface, (0, 0, 0), popup_surface.get_rect(), 3)

        # Text Wrapping Function
        def wrap_text(text, font, max_width):
            words = text.split(' ')
            lines = []
            current_line = ""

            for word in words:
                test_line = f"{current_line} {word}".strip()
                if font.size(test_line)[0] < max_width:
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = word
            lines.append(current_line)

            return lines

        wrapped_lines = wrap_text(message, font, popup_width - 40)
        wrapped_lines.append(instructions)  

        y_offset = 20
        for line in wrapped_lines:
            text_surface = font.render(line, True, (0, 0, 0))
            popup_surface.blit(text_surface, (20, y_offset))
            y_offset += font.get_height() + 5  

        screen.blit(popup_surface, (SCREEN_WIDTH // 2 - popup_width // 2, SCREEN_HEIGHT // 2 - popup_height // 2))
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:  
                        on_confirm()
                        waiting = False
                    elif event.key == pygame.K_n:  
                        waiting = False

    def level_up(self):
        """Increase property level"""
        if self.level < 3:
            self.level += 1
