import pygame
from pygame.sprite import Sprite

# This class represents a single alien
class Alien(Sprite):
    def __init__(self, ai_settings, screen):
        # Initialize the alien and set a starting position
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the image of the alien and set rect attribute
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # Start each alien at the top left
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store alien's exact position
        self.x = float(self.rect.x)


    def blitme(self):
        # Draw alien at current location
        self.screen.blit(self.image,self.rect)


    def update(self):
        # Move alien right or left
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x


    def check_edges(self):
        # Checking to see whether an alien hit the edge of the screen
        screen_rect = self.screen.get_rect()
        # If the right rect position of the alien is greater than or equal to the right of the screen,
        # it must been it has reached the end, thus returning true
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= screen_rect.left:
            return True
