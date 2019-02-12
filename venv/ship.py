import pygame

class Ship():

    def __init__(self, ai_settings, screen):
        self.screen = screen
        self.ai_settings = ai_settings

        # load ship image and get rect
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # start each new ship at bottom center scrn
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # store decimal value for ship's center
        self.center = float(self.rect.centerx)


        # movement flags
        self.moving_right = False
        self.moving_left = False



    # update the ships' position based on movement flags
    def update(self):
        # if statements limit the ships range
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        # update rect obj
        self.rect.centerx = self.center

    def blitme(self):
        self.screen.blit(self.image, self.rect)

        # i figured out what was wrong and why it wasn't displaying the ship. it was probably because of python3
        # when i was testing to see why the ship wasn't coming in the screen i noticed that i could no longer change bg
        # it indeed was because it wasn't actually running the code
