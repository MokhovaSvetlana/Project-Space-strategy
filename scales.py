import pygame
from settings import w

from settings import FONT


class SatietyScale(pygame.sprite.Sprite):

    def __init__(self, occupancy):
        super().__init__()
        self.occupancy = occupancy
        self.image = pygame.Surface((100, 5))
        self.rect = pygame.Rect(45, 5, 100, 5)
        pygame.draw.rect(self.image, 'white', (0, 0, self.occupancy, 5))
        self.text_coord = 5
        self.im_coord = 5

    def draw(self, screen):
        surface = pygame.Surface((200, 15))
        font = pygame.font.Font(None, FONT)
        surface.fill('black')
        text = font.render('Satiety', True, 'white')
        intro_rect = text.get_rect()
        intro_rect.top = 3
        intro_rect.x = 5
        self.rect.width = self.occupancy
        self.image.fill('black')
        pygame.draw.rect(self.image, 'white', (0, 0, self.occupancy, 5))
        surface.blit(self.image, (45, 5))
        text_num = font.render(str(self.occupancy), True, 'white')
        intro_rect2 = text_num.get_rect()
        intro_rect2.top = 3
        intro_rect2.x = 152
        surface.blit(text, intro_rect)
        surface.blit(text_num, intro_rect2)
        screen.blit(surface, (w // 2 - surface.get_width() // 2, 0))

    def add(self, n):
        self.occupancy = min(self.occupancy + n, 100)

    def subtract(self, n):
        self.occupancy = max(self.occupancy - n, 0)


class FuelScale(pygame.sprite.Sprite):

    def __init__(self, occupancy):
        super().__init__()
        self.occupancy = occupancy
        self.image = pygame.Surface((100, 5))
        self.rect = pygame.Rect(45, 33, 100, 5)
        pygame.draw.rect(self.image, 'white', (0, 0, self.occupancy, 5))
        self.text_coord = 25
        self.im_coord = 25

    def draw(self, screen):
        surface = pygame.Surface((200, 25))
        font = pygame.font.Font(None, FONT)
        text = font.render('Fuel', True, 'white')
        intro_rect = text.get_rect()
        intro_rect.top = 15
        intro_rect.x = 3
        self.rect.width = self.occupancy
        self.image.fill('black')
        pygame.draw.rect(self.image, 'white', (0, 0, self.occupancy, 5))
        surface.blit(self.image, (45, 15))
        text_num = font.render(str(self.occupancy), True, 'white')
        intro_rect2 = text_num.get_rect()
        intro_rect2.top = 15
        intro_rect2.x = 150
        surface.blit(text, intro_rect)
        surface.blit(text_num, intro_rect2)
        screen.blit(surface, (2 + w // 2 - surface.get_width() // 2, 15))

    def add(self, n):
        self.occupancy = min(self.occupancy + n, 100)

    def subtract(self, n):
        self.occupancy = max(self.occupancy - n, 0)
