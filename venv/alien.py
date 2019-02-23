import pygame
from pygame.sprite import Sprite


def load_image(name):
    image = pygame.image.load(name)
    return image


class Alien(Sprite):
    # This class represents a single alien

    def __init__(self, ai_settings, screen, img, img2):
        # Initialize Alien and set starting values.
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Animations interator.
        self.index = 0

        # Load the alien image, make a holder to get the rect attribute.
        self.image = pygame.image.load(img)


        # Holds all of the images for animations, keep appending if you want more frames.
        self.images = []
        self.images.append(load_image(img))
        self.images.append(load_image(img2))

        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact position.
        self.x = float(self.rect.x)

    def check_edges(self):
        # Check if the alien has reached the edge of the screen.
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True


    def update(self):
        # Move alien continuously.
        # A HA I FOUND YOU
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        # check out this cool thing if you uncomment this and comment the above
        #self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.ufo_direction)
        self.rect.x = self.x
        self.animate()

    def animate(self):
        # Animations, goes through the index of images for the alien.
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]


    def blitme(self):
        # Draw aliens current location
        self.screen.blit(self.image, self.rect)