from player import Player

class Bot(Player):
    def __init__(self, name, image, pos, offset):
        """Initialize bot (inherits from Player)"""
        super().__init__(name, image, pos, offset, is_human=False)
