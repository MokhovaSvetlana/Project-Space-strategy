import pygame
from abc import ABC
from math import sin, cos, radians
from settings import FONT


class Button(pygame.sprite.Sprite, ABC):

    def __init__(self, pos, size):
        super().__init__()
        self.rect = pygame.rect.Rect(*pos, *size)
        self.image = pygame.Surface(size)

    def cursor_on_button(self, x, y):
        return self.rect.x <= x <= self.rect.right and \
            self.rect.y <= y <= self.rect.bottom


class BackButton(Button):
    def draw(self, screen):
        color = "white"
        start_pos = (self.rect.w * 0.25, self.rect.h * 0.5)
        pygame.draw.rect(self.image, "white", (0, 0, *self.rect.size), width=1)
        pygame.draw.line(self.image, color, start_pos, (self.rect.w * 0.5, self.rect.h * 0.25))
        pygame.draw.line(self.image, color, start_pos, (self.rect.w * 0.5, self.rect.h * 0.75 + 1))
        pygame.draw.line(self.image, color, start_pos, (self.rect.w * 0.75, self.rect.h * 0.5))
        screen.blit(self.image, self.rect.topleft)


class SurchButton(Button):
    def draw(self, screen):
        color = "white"
        r = min(self.rect.w, self.rect.h) * 0.25
        center = (self.rect.w * 0.4, self.rect.h * 0.4)
        pygame.draw.rect(self.image, "white", (0, 0, *self.rect.size), width=1)
        pygame.draw.circle(self.image, color, center, r, width=1)
        start_pos_line = (center[0] - r * sin(radians(315)), center[1] + r * cos(radians(315)))
        pygame.draw.line(self.image, color, start_pos_line,
                         (start_pos_line[0] + self.rect.w * 0.25, start_pos_line[1] + self.rect.h * 0.25))
        screen.blit(self.image, self.rect.topleft)


class InventoryButton(Button):
    def draw(self, screen):
        k = 0.2
        color = "white"
        pygame.draw.rect(self.image, color, (0, 0, *self.rect.size), width=1)
        pygame.draw.rect(self.image, color, (self.rect.w * k, self.rect.h * k,
                                               int(self.rect.w * (1 - 2 * k)),
                                               int(self.rect.h * (1 - 2 * k))), width=1)
        pygame.draw.line(self.image, color, (self.rect.w * k, self.rect.h * 0.4),
                         (self.rect.w * (1 - k) - 1, self.rect.h * 0.4))
        screen.blit(self.image, self.rect.topleft)


class ResourceButton(Button):
    def __init__(self, pos, size, title, ix):
        super().__init__(pos, size)
        self.resource_title = title
        self.ix = ix

    def draw(self, screen):
        color = "white"
        self.image.fill("black")
        pygame.draw.rect(self.image, color, (0, 0, *self.rect.size), width=1)
        font = pygame.font.Font(None, FONT + 5)
        text = font.render(self.resource_title, True, color)
        self.image.blit(text, (5, self.rect.h // 2 - text.get_height() // 2))
        screen.blit(self.image, self.rect.topleft)


class UseButton(Button):
    def __init__(self, pos, size, resource):
        super().__init__(pos, size)
        self.resource = resource

    def draw(self, screen):
        color = "white"
        self.image.fill("black")
        pygame.draw.rect(self.image, color, (0, 0, *self.rect.size), width=1)
        font = pygame.font.Font(None, FONT + 5)
        text = font.render("Use", True, color)
        self.image.blit(text, (self.rect.w // 2 - text.get_width() // 2, self.rect.h // 2 - text.get_height() // 2))
        screen.blit(self.image, self.rect.topleft)
