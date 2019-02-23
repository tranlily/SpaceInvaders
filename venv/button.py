import pygame.font

class Button():

    def __init__(self, ai_settings, screen, msg):
        """Initialize button attributes."""
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Set the dimensions and properties of the button.
        self.width, self.height = 200, 50
        self.button_color = (2, 4, 14)
        self.text_color = (76, 215, 255)

        # This is the background color beneath the button
        self.intro_color = (2, 4, 14)
        self.font = pygame.font.SysFont("monospace", 32)

        # Build the button's rect object, and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)

        self.rect.midbottom = self.screen_rect.midbottom

        # The button message only needs to be prepped once.
        self.prep_msg(msg)


    def prep_msg(self, msg):
        """Turn msg into a rendered image, and center text on the button."""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.midbottom = self.rect.midbottom


    def draw_button(self):
        self.screen.fill(self.intro_color)
        my_image = pygame.image.load('images/starry.jpg')
        self.screen.blit(my_image, (-150, 0))
        self.screen.blit(self.msg_image, self.msg_image_rect)

