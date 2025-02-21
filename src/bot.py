from src.player import Player
import random

class Bot(Player):
    def __init__(self, name, image, pos, offset):
        """Initialize bot (inherits from Player)"""
        super().__init__(name, image, pos, offset, is_human=False)

    def take_turn(self, screen, game):
        """Handles bot's turn automatically"""
        roll = game.dice.roll(screen)
        print(f"{self.name} rolled {roll}")
        self.move(roll, screen, game)
        if tuple(self.pos) in game.map.minigame_positions:
            self.play_minigame(screen, game)
    
    def play_minigame(self, screen, game):
        money = random.choice([500, -500])
        print(money)
        self.money += money

        if money == 500:
            result_message = "You won the minigame! You earned $500."
        else:
            result_message = "You lost the minigame! You lost $500."

        self.show_popup(screen, result_message)

class Cheater(Bot):
    """Bot2 always buys and upgrades properties"""
    def interact_with_property(self, property, screen, game):
        if property.owner is None:
            property.buy(self)  # Buy instantly
        elif property.owner == self.name:
            property.upgrade(self, screen, game)  # Upgrade if owned
    
    def cheat(self, game, player): # to be fixed here, currently only player 1
        return True

class Grudger(Bot):
    """Bot3 will not buy property until Player1 buys at least one"""
    def __init__(self, name, image, pos, offset):
        super().__init__(name, image, pos, offset)
        self.waiting_for_player1 = True  # Track Player1's action
        self.player_1_cheated = False

    def interact_with_property(self, property, screen, game):
        # player1 = game.get_player_by_name("Player1") # to be fixed here, currently only player 1

        # if property.owner is None:
        #     if self.waiting_for_player1 and player1 and any(p.owner == "Player1" for p in game.map.properties.values()):
        #         self.waiting_for_player1 = False  # Stop waiting once Player1 has bought at least one property
        #         property.buy(self)  # Now buy property
        # elif property.owner == self.name:
        #     property.upgrade(self, screen, game)  # Upgrade if owned
        if property.owner is None:
            property.buy(self)  # Buy instantly
        elif property.owner == self.name:
            property.upgrade(self, screen, game)
    
    def cheat(self, game, player):
        if self.name in game.cheat_map[player.name]:
            print(f"{self.name} remembers {player.name} cheated! Now cheating back forever.")
            return True
        else:
            print(f"{self.name} cooperates unless Player1 cheats.")
            return False
        
class Detective(Bot):
    """Bot4 buys on second visit, skips third/fourth, then mirrors Player1"""
    def __init__(self, name, image, pos, offset):
        super().__init__(name, image, pos, offset)
        self.visit_count = {}  # Track visits per property
        self.mirroring_player1 = False  # Track when to mirror Player1
        self.cheat_sequence = [False, False, True, False]
        self.curr_cheat_index = 0

    def interact_with_property(self, property, screen, game):
        # if property.position not in self.visit_count:
        #     self.visit_count[property.position] = 0

        # self.visit_count[property.position] += 1
        # visit_num = self.visit_count[property.position]
        # player1 = game.get_player_by_name("Player1")

        # if property.owner is None:
        #     if visit_num == 2:
        #         property.buy(self)  # Buy on second visit
        #     elif visit_num > 4:
        #         if player1 and any(p.owner == "Player1" for p in game.map.properties.values()):
        #             self.mirroring_player1 = True  # Start mirroring Player1

        #     if self.mirroring_player1 and player1:
        #         if any(p.owner == "Player1" for p in game.map.properties.values()):
        #             property.buy(self)  # Mirror Player1's buying action
        # elif property.owner == self.name:
        #     property.upgrade(self, screen, game)  # Upgrade if owned
        if property.owner is None:
            property.buy(self)  # Buy instantly
        elif property.owner == self.name:
            property.upgrade(self, screen, game)
    
    def cheat(self, game, player): # to be fixed here, currently only player 1
        if self.name in game.cheat_map[player.name]:
            print(f"{self.name} saw {player.name} cheated! Now cheating back forever.")
            return True
        else:
            cheat = self.cheat_sequence[self.curr_cheat_index]
            self.curr_cheat_index = (self.curr_cheat_index + 1) % len(self.cheat_sequence)
            print(f"{self.name} following its strategy to cheat.")
        return cheat
