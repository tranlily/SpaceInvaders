import pygame.font

class Intro():
    def __init__(self, ai_settings, screen):

        self.screen = screen
        self.screen_rect = screen.get_rect()


        # Set properties
        self.width = screen_width
        self.height = screen_height
        self.introcolor = (123,174,157)

    def game_intro(self):
        gameDisplay = pygame.display.set_mode((display_width, display_height))

        intro = True

        while intro:
            for event in pygame.event.get():
                print(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            gameDisplay.fill(white)
            largeText = pygame.font.Font('freesansbold.ttf', 115)
            TextSurf, TextRect = text_objects("A bit Racey", largeText)
            TextRect.center = ((display_width / 2), (display_height / 2))
            gameDisplay.blit(TextSurf, TextRect)
            pygame.display.update()
            clock.tick(15)
