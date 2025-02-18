class Camera:
    def __init__(self, screen_width, screen_height, map_width, map_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.map_width = map_width
        self.map_height = map_height
        self.offset_x = 0
        self.offset_y = 0

    def update(self, player):
        self.offset_x = player.rect.centerx - self.screen_width // 2
        self.offset_y = player.rect.centery - self.screen_height // 2

        self.offset_x = max(0, min(self.offset_x, self.map_width - self.screen_width))
        self.offset_y = max(0, min(self.offset_y, self.map_height - self.screen_height))

        # print(f"Camera offsets: x={self.offset_x}, y={self.offset_y}")
        # print(f"Player position: x={player.rect.centerx}, y={player.rect.centery}")
