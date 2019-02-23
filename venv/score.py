import pygame

class Score:
    def __init__(self, settings, screen, msg, y_pos = 0.65):
        self.settings = settings
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.alt_color = (0, 255, 0)

        self.font = pygame.font.SysFont("monospace", 32)
        self.y_pos = y_pos

        self.msg = msg
        self.msg_image, self.msg_image_rect = None, None
        self.prep_msg(self.text_color)

    def check_button(self, mouse_x, mouse_y):
        if self.msg_image_rect.collidepoint(mouse_x, mouse_y):
            return True
        else:
            return False


    def prep_msg(self, color):
        self.msg_image = self.font.render(self.msg, True, color, self.settings.bg_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.centerx = (self.settings.screen_width // 2)
        self.msg_image_rect.centery = int(self.settings.screen_height * self.y_pos)

    def draw_button(self):
        self.screen.blit(self.msg_image, self.msg_image_rect)
