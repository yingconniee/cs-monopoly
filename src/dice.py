import pygame
import random
import time
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Dice():
    def __init__(self):
        self.images = [
            pygame.image.load("src/assets/dice1.png"),
            pygame.image.load("src/assets/dice2.png"),
            pygame.image.load("src/assets/dice3.png"),
            pygame.image.load("src/assets/dice4.png"),
        ]

        self.dice_images = [pygame.transform.scale(img, (80, 80)) for img in self.images]

    def roll(self, screen):
        roll_duration = 1.5  # Rolling time
        start_time = time.time()

        # Dice Rolling Animation
        while time.time() - start_time < roll_duration:
            dice_image = random.choice(self.dice_images)
            screen.blit(dice_image, (SCREEN_WIDTH // 2 - 40, SCREEN_HEIGHT // 2 - 40))
            pygame.display.flip()
            pygame.time.delay(150)

        # Get the final dice result
        final_roll = random.randint(1, 4)
        final_image = self.dice_images[final_roll - 1]

        # Show final roll for 2 seconds
        screen.blit(final_image, (SCREEN_WIDTH // 2 - 40, SCREEN_HEIGHT // 2 - 40))
        pygame.display.flip()
        time.sleep(1)  # Pause for 2 seconds

        return final_roll  # Return the rolled number
