import pygame
import random
from settings import SCREEN_HEIGHT, SCREEN_WIDTH

class Property:
    def __init__(self, position):
        """Initialize property"""
        self.position = position
        self.owner = None  # No owner at start
        self.level = 0  # No house at start
        self.just_bought = False  # Flag to track if the property was just bought
        self.player_1_cheat_store = dict()
        self.players = ['Cheater', 'Grudger', 'Detective']

        for player in self.players: # to be fixed here, currently only player 1
            self.player_1_cheat_store[player] = False

    def buy(self, player):
        """Allows a player to buy the property if it's unowned"""
        if self.owner is None:  # If not owned, allow purchase
            self.owner = player.name
            self.level = 1  # Start with Level 1 house
            self.just_bought = True  # Set the just_bought flag0
            print('Property bought!')

    def upgrade(self, player, screen, game):
        """Ask the player if they want to upgrade (max level 3)"""
        if self.owner == player.name and self.level < 3:
            if player.is_human:
                self.show_upgrade_popup(screen, player, game)  # Show popup for humans
            else:
                self.level += 1  # Auto-upgrade for bots

    def interact(self, player, screen, game_map, game):
        """Handles interaction when a player lands on a property"""
        pos = tuple(player.pos)

        if pos in game_map.property_positions:
            property_name = game_map.property_names.get(pos, "Unknown")  # Get property name

            if self.owner is None:  
                if player.is_human:
                    self.show_buy_popup(screen, player, property_name, game)  # Human players get a buy option
                else:
                    if hasattr(player, "interact_with_property"):
                        player.interact_with_property(self, screen, game)  # Call bot-specific interaction
                    else:
                        self.buy(player)  # Default behavior for generic bots

            elif self.owner != player.name:  # If player steps on someone else's property, pay rent
                owner = game.get_player_by_name(self.owner)
                print(game.cooperation_map)
                # Check if cooperation already exists
                if owner and player.name in game.cooperation_map[owner.name] and owner.name in game.cooperation_map[player.name]:
                    cheat = self.cheat_popup(screen, player, owner, game)
                    if cheat:
                        if player.name == "player1":
                            self.player_1_cheat_store[owner.name] = True
                        print(f'{player.name} cheated on {owner.name} and charged rent.')
                        rent_amount = self.calculate_rent()
                        player.money -= rent_amount
                        owner.money += rent_amount
                        print(f"{player.name} paid ${rent_amount} rent to {owner.name}")

                    else:
                        print(f'Cooperation between {owner.name} and {player.name} exists. No rent charged.')
                else:
                    # Show cooperation popup only if they haven't agreed yet
                    if owner and owner.is_human and not player.is_human:
                        cooperation = self.show_cooperation_popup(screen, owner, player, game)
                        if cooperation:
                            print(f"{owner.name} and {player.name} agreed to cooperate. No rent will be charged.")
                            game.cooperation_map[player.name].add(owner.name)
                            game.cooperation_map[owner.name].add(player.name)
                        else:
                            rent_amount = self.calculate_rent()
                            player.money -= rent_amount
                            owner.money += rent_amount
                            print(f"{player.name} paid ${rent_amount} rent to {owner.name}")

                    else:
                        rent_amount = self.calculate_rent()
                        player.money -= rent_amount
                        owner.money += rent_amount
                        print(f"{player.name} paid ${rent_amount} rent to {owner.name}")
            
            if player.money <= 0:
                game.remove_player(player)

            if self.owner == player.name and not self.just_bought:
                self.upgrade(player, screen, game)  # Allow player to upgrade if they own the property and it wasn't just bought
            else:
                self.just_bought = False

    def calculate_rent(self):
        """Returns rent based on property level"""
        rent_prices = {1: 1000, 2: 2000, 3: 3000}
        return rent_prices.get(self.level, 0)

    def show_buy_popup(self, screen, player, property_name, game):
        """Display a popup asking the player if they want to buy the property"""
        self.show_popup(screen, f"{player.name}, Buy this property ({property_name})?", "Y/N", lambda: self.buy(player), game)

    def show_upgrade_popup(self, screen, player, game):
        """Display a popup asking the player if they want to upgrade"""
        self.show_popup(screen, f"{player.name}, Upgrade property to Level {self.level + 1}?", "Y/N", lambda: self.level_up(), game)

    def show_popup(self, screen, message, instructions, on_confirm, game):
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

        # Redraw the screen after the popup interaction
        screen.blit(game.background_image, (0, 0))  # Redraw background
        game.map.draw(screen)  # Redraw board
        for player in game.players:
            player.draw(screen)  # Redraw all players
        pygame.display.flip()

    def level_up(self):
        """Increase property level"""
        if self.level < 3:
            self.level += 1  # Upgrade up to Level 3
    
    def show_cooperation_popup(self, screen, owner, player, game):
        """Popup asking human player whether to cooperate with a bot"""
        pygame.font.init()
        font = pygame.font.Font(None, 28)
        popup_width, popup_height = 420, 140
        popup_surface = pygame.Surface((popup_width, popup_height))
        popup_surface.fill((255, 255, 255))
        pygame.draw.rect(popup_surface, (0, 0, 0), popup_surface.get_rect(), 3)

        # Render message
        message = f"Do you want to cooperate with {player.name}?"
        yes_text = font.render("Press Y to Cooperate", True, (0, 0, 0))
        no_text = font.render("Press N to Charge Rent", True, (0, 0, 0))

        text_surface = font.render(message, True, (0, 0, 0))
        popup_surface.blit(text_surface, (20, 40))
        popup_surface.blit(yes_text, (20, 80))
        popup_surface.blit(no_text, (20, 110))

        screen.blit(popup_surface, (SCREEN_WIDTH // 2 - popup_width // 2, SCREEN_HEIGHT // 2 - popup_height // 2))
        pygame.display.flip()

        waiting = True
        cooperation = False
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:  # Cooperate
                        cooperation = True
                        waiting = False
                    elif event.key == pygame.K_n:  # Charge rent
                        cooperation = False
                        waiting = False

        screen.blit(game.background_image, (0, 0))  
        game.map.draw(screen)
        for p in game.players:
            p.draw(screen)
        game.display_money()
        pygame.display.flip()
        return cooperation
    
    def cheat_popup(self, screen, player, owner, game):
        """Popup asking human player whether they want to cheat on a cooperating player"""
        if owner.is_human:
            pygame.font.init()
            font = pygame.font.Font(None, 28)
            popup_width, popup_height = 420, 140
            popup_surface = pygame.Surface((popup_width, popup_height))
            popup_surface.fill((255, 255, 255))
            pygame.draw.rect(popup_surface, (0, 0, 0), popup_surface.get_rect(), 3)

            # Render message
            message = f"You are cooperating with {owner.name}. Do you want to cheat and charge rent?"
            cheat_text = font.render("Press Y to Cheat (Charge Rent)", True, (255, 0, 0))  # Red text for cheating
            respect_text = font.render("Press N to Respect Cooperation", True, (0, 0, 0))

            text_surface = font.render(message, True, (0, 0, 0))
            popup_surface.blit(text_surface, (20, 40))
            popup_surface.blit(cheat_text, (20, 80))
            popup_surface.blit(respect_text, (20, 110))

            screen.blit(popup_surface, (SCREEN_WIDTH // 2 - popup_width // 2, SCREEN_HEIGHT // 2 - popup_height // 2))
            pygame.display.flip()

            waiting = True
            cheat = False
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_y:  # Cheat
                            cheat = True
                            waiting = False
                        elif event.key == pygame.K_n:  # Respect Cooperation
                            cheat = False
                            waiting = False

            screen.blit(game.background_image, (0, 0))  
            game.map.draw(screen)
            for p in game.players:
                p.draw(screen)
            game.display_money()
            pygame.display.flip()
        else:
            cheat = player.cheat(self) # bot cheating logic

        return cheat
