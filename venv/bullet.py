import pygame
from pygame.sprite import Sprite

class Bullet (Sprite):
    # This class manages bullets fired from Ship

    # Create a bullet object at the ship's current position
    def __init__(self, ai_settings, screen, ship):
        super(Bullet, self).__init__()
        self.screen = screen

        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top


        # Store bullet's position as a decimal
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor


    def update(self):
        # Move the bullet up the screen
        # Update decimal position of the bullet
        self.y -= self.speed_factor
        # Update the rect position
        self.rect.y = self.y


    # Draw the bullet to the screen
    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)