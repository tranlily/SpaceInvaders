import pygame
from pygame.sprite import Sprite
from random import choice

def load_image(name):
    image = pygame.image.load(name)
    return image


class Ufo(Sprite):
    def __init__(self, ai_settings, screen):
        super(Ufo, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        self.possible_points = ai_settings.ufo_points

        self.images = []
        self.images.append(load_image('images/ufo.png'))
        self.images.append(load_image('images/ufo2.png'))
        self.images.append(load_image('images/ufo3.png'))
        self.images.append(load_image('images/ufo4.png'))

        self.index = 0
        self.image = self.images[self.index]

        self.rect = self.image.get_rect()

        # Start each ufo near the top left of the screen.
        # Check out the neat bug if you comment this out
        self.rect.x = self.rect.width

        self.speed = ai_settings.ufo_speed_factor * (choice([-1, 1]))
        self.rect.y = ai_settings.screen_height * 0.1

        self.x = float(self.rect.x)

    def check_edges(self):
        # Check if the ufo has reached the edge of the screen.
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        # Move ufo continuously
        self.x += (self.ai_settings.ufo_speed_factor * self.ai_settings.ufo_direction)
        self.rect.x = self.x

        # Animations, goes through the index of images for the ufo
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def get_score(self):
        self.score = choice(self.possible_points)
        return self.score