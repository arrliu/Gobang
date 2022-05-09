import pygame
import pygame.font
class Word:
    def __init__(self, ai_game,rectx,recty):
        """Initialize button attributes."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions and properties of the button.
        self.width, self.height = 100, 30
        self.button_color = (255, 255,255)
        self.text_color = (0, 0,255)
        self.font = pygame.font.SysFont('SimHei', 26)

        # Build the button's rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.x = self.screen_rect.left+rectx
        self.rect.y = self.screen_rect.top+recty


        # The button message needs to be prepped only once.

    def draw_text(self,msg):
        self.msg_image = self.font.render(msg, True, self.text_color,
                                          self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
        # Draw blank button and then draw message.
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

