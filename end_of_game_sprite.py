import pygame
from settings import w, h
from buttons import OutplayButton, ReturnToMenuButton


class ResultScreen(pygame.sprite.Sprite):

    def __init__(self, res, strings, screen):
        super().__init__()
        res = 'ВЫИГРАЛИ' if res else 'ПРОИГРАЛИ'
        self.text = [f'Вы {res}!', *strings, 'Попробовать снова?']
        self.width, self.height = self.calculating_size()
        self.height = len(self.text) * 30
        self.y_coord = max(5, h // 2 - self.height // 2 - 40)
        self.image = pygame.Surface((self.width, self.height))
        self.rect = pygame.Rect(w // 2 - self.width // 2, self.y_coord, self.width, self.height)
        font = pygame.font.Font(None, 25)
        text_coord = 2
        for line in self.text:
            text = font.render(line, True, 'white')
            intro_rect = text.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = self.width // 2 - text.get_width() // 2
            text_coord += intro_rect.height
            self.image.blit(text, intro_rect)
        text_coord = self.rect.y + self.height - 20
        self.button_outplay = OutplayButton((w // 2 - 50, text_coord + 50), (100, 40))
        text_coord += 90
        self.button_return = ReturnToMenuButton((w // 2 - 75, text_coord + 20), (150, 40))
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def calculating_size(self):
        height = len(self.text) * 30
        width = len(max(self.text, key=len)) * 10
        return width, height
