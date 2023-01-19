import pygame
from abc import ABC
from math import sin, cos, radians
from settings import FONT
from resource import TypesResources


class Button(pygame.sprite.Sprite, ABC):

    def __init__(self, pos, size):
        super().__init__()
        self.rect = pygame.rect.Rect(*pos, *size)
        self.image = pygame.Surface(size)

    def cursor_on_button(self, x, y):
        return self.rect.x <= x <= self.rect.right and \
            self.rect.y <= y <= self.rect.bottom


class PlayButton(Button):
    def draw(self, screen):
        self.image.fill('black')
        font = pygame.font.Font(None, 30)
        text = font.render('START', True, 'white')
        intro_rect = text.get_rect()
        intro_rect.top = 12
        intro_rect.x = 17
        self.image.blit(text, intro_rect)
        pygame.draw.rect(self.image, 'white', (1, 1, self.image.get_width() - 2, self.image.get_height() - 2), 1)
        screen.blit(self.image, (self.rect.x, self.rect.y))


class RulesButton(Button):
    def draw(self, screen):
        self.image.fill('black')
        font = pygame.font.Font(None, 30)
        text = font.render('RULES', True, 'white')
        intro_rect = text.get_rect()
        intro_rect.top = 12
        intro_rect.x = 17
        self.image.blit(text, intro_rect)
        pygame.draw.rect(self.image, 'white', (1, 1, self.image.get_width() - 2, self.image.get_height() - 2), 1)
        screen.blit(self.image, (self.rect.x, self.rect.y))


class BackButton(Button):
    def draw(self, screen):
        color = "white"
        start_pos = (self.rect.w * 0.25, self.rect.h * 0.5)
        pygame.draw.rect(self.image, color, (0, 0, *self.rect.size), width=1)
        pygame.draw.line(self.image, color, start_pos, (self.rect.w * 0.5, self.rect.h * 0.25))
        pygame.draw.line(self.image, color, start_pos, (self.rect.w * 0.5, self.rect.h * 0.75 + 1))
        pygame.draw.line(self.image, color, start_pos, (self.rect.w * 0.75, self.rect.h * 0.5))
        screen.blit(self.image, self.rect.topleft)


class SurchButton(Button):
    def draw(self, screen):
        color = "white"
        r = min(self.rect.w, self.rect.h) * 0.25
        center = (self.rect.w * 0.4, self.rect.h * 0.4)
        pygame.draw.rect(self.image, color, (0, 0, *self.rect.size), width=1)
        pygame.draw.circle(self.image, color, center, r, width=1)
        start_pos_line = (center[0] - r * sin(radians(315)), center[1] + r * cos(radians(315)))
        pygame.draw.line(self.image, color, start_pos_line,
                         (start_pos_line[0] + self.rect.w * 0.25, start_pos_line[1] + self.rect.h * 0.25))
        screen.blit(self.image, self.rect.topleft)


class SpaceshipButton(Button):
    def draw(self, screen):
        color = "white"
        self.image.fill("black")
        pygame.draw.rect(self.image, color, (0, 0, *self.rect.size), width=1)
        pygame.draw.rect(self.image, color, (self.rect.w * 0.2, self.rect.h * 0.2,
                                             int(self.rect.w * 0.6), int(self.rect.h * 0.4)), width=1)
        pygame.draw.line(self.image, color, (self.rect.w * 0.5, self.rect.h * 0.6),
                         (self.rect.w * 0.5, self.rect.h * 0.8))
        pygame.draw.line(self.image, color, (self.rect.w * 0.25, self.rect.h * 0.8),
                         (self.rect.w * 0.75, self.rect.h * 0.8))
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

    def break_contour(self, screen):
        pygame.draw.rect(screen, "black", (self.rect.left + 1, self.rect.bottom - 1, self.rect.w - 2, 2))


class RepairingButton(Button):

    def draw(self, screen):
        color = "white"
        self.image.fill("black")
        pygame.draw.rect(self.image, color, (0, 0, *self.rect.size), width=1)
        pygame.draw.line(self.image, color, (self.rect.w * 0.25, self.rect.h * 0.75 - 1),
                         (self.rect.w * 0.5 - 1, self.rect.h * 0.5 - 1), width=2)
        pygame.draw.arc(self.image, color, (self.rect.w // 2 - 3, 3, self.rect.w // 2, self.rect.h // 2),
                        2.3, 5.6, width=2)
        screen.blit(self.image, self.rect.topleft)

    def break_contour(self, screen):
        pygame.draw.rect(screen, "black", (self.rect.left + 1, self.rect.bottom - 1, self.rect.w - 2, 2))


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


class RepairSpaceshipButton(Button):
    def draw(self, screen):
        color = "white"
        self.image.fill("black")
        pygame.draw.rect(self.image, color, (0, 0, *self.rect.size), width=1)
        font = pygame.font.Font(None, FONT + 10)
        text = font.render("Repair Your Spaceship", True, color)
        self.image.blit(text, (self.rect.w // 2 - text.get_width() // 2, self.rect.h // 2 - text.get_height() // 2))
        screen.blit(self.image, self.rect.topleft)


class OutplayButton(Button):

    def draw(self, screen):
        self.image.fill('black')
        font = pygame.font.Font(None, 25)
        text = font.render('OUTPLAY', True, 'white')
        intro_rect = text.get_rect()
        intro_rect.top = 10
        intro_rect.x = 10
        self.image.blit(text, intro_rect)
        pygame.draw.rect(self.image, 'white', (1, 1, self.image.get_width() - 2, self.image.get_height() - 2), 1)
        screen.blit(self.image, (self.rect.x, self.rect.y))


class ReturnToMenuButton(Button):

    def draw(self, screen):
        self.image.fill('black')
        font = pygame.font.Font(None, 25)
        text = font.render('Return to menu', True, (180, 180, 180))
        intro_rect = text.get_rect()
        intro_rect.top = 10
        intro_rect.x = 13
        self.image.blit(text, intro_rect)
        pygame.draw.rect(self.image, (100, 100, 100), (1, 1, self.image.get_width() - 2, self.image.get_height() - 2), 1)
        screen.blit(self.image, (self.rect.x, self.rect.y))


class TradeResourceButton(Button):
    def __init__(self, pos, size, resource, is_selling=True):
        super().__init__(pos, size)
        self.resource = resource
        self.is_selling = is_selling
        if is_selling:
            self.money = self.resource.money // 2
        else:
            self.money = self.resource.money * 2

    def draw(self, screen, player_res):
        if not self.is_selling:
            color = "white"
        else:
            color = "green" if player_res is not None else "red"
        self.image.fill("black")
        strings = [self.resource.title, f"Quantity: {player_res.quantity if player_res is not None else 0}",
                   f"Money: {self.money}"]
        font = pygame.font.Font(None, FONT + 5)
        text_coord = 2
        for line in strings:
            text = font.render(line, True, color)
            intro_rect = text.get_rect()
            text_coord += 3
            intro_rect.top = text_coord
            intro_rect.x = 3
            text_coord += intro_rect.height
            self.image.blit(text, intro_rect)

        pygame.draw.rect(self.image, color, (0, 0, *self.rect.size), width=1)
        screen.blit(self.image, self.rect.topleft)


class TradeStatusButton(Button):
    def __init__(self, pos, size, is_selling=True):
        super().__init__(pos, size)
        font = pygame.font.Font(None, FONT + 5)
        self.text = font.render("sell" if is_selling else "buy", True, "white")

    def draw(self, screen):
        self.image.fill("black")
        color = "white"
        self.image.blit(self.text, (5, self.rect.h // 2 - self.text.get_height() // 2))
        pygame.draw.rect(self.image, color, (0, 0, *self.rect.size), width=1)
        screen.blit(self.image, self.rect.topleft)
