from player import Player

class Bot(Player):
    def __init__(self, name, image, pos, offset):
        """Initialize bot (inherits from Player)"""
        super().__init__(name, image, pos, offset, is_human=False)
    
    def take_turn(self, screen, game):
        """Handles bot's turn automatically"""
        roll = game.dice.roll(screen)
        print(f"{self.name} rolled {roll}")
        self.move(roll, screen, game)
