import pygame
from random import randint

from settings import w, h
from buttons import PlayButton, RulesButton, ReturnToMenuButton


class Star(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y, n):
        super().__init__()
        self.image = pygame.Surface((1, 1))
        self.x_pos = pos_x
        self.y_pos = pos_y
        self.width = 2    # Четная!
        self.rect = pygame.Rect(self.x_pos, self.y_pos, self.width, self.width)
        pygame.draw.line(self.image, 'white', (0, 0), (self.width, self.width), 1)
        pygame.draw.line(self.image, 'white', (self.width, 0), (0, self.width), 1)
        pygame.draw.line(self.image, 'white', (self.width // 2, 0), (self.width // 2, self.width), 1)
        pygame.draw.line(self.image, 'white', (0, self.width // 2), (self.width, self.width // 2), 1)
        self.step_for_width = 2   # Четный!
        self.k = 0
        self.k1 = 0
        self.event = pygame.USEREVENT + n
        self.shine = False
        pygame.time.set_timer(self.event, randint(2000, 6000))

    def update(self):
        if not self.shine:
            self.image.fill('black')
            return

        if self.k1 < 4:
            self.k1 += 1
            return
        self.k1 = 0
        self.k += 1
        if self.k % 10 == 0:
            self.step_for_width *= -1
        if self.k == 20:
            self.k = 0
            self.shine = False

        self.width += self.step_for_width
        self.x_pos -= self.step_for_width // 2
        self.y_pos -= self.step_for_width // 2
        self.image = pygame.Surface((self.width, self.width))
        self.rect = pygame.Rect(self.x_pos, self.y_pos, self.width, self.width)
        self.image.fill('black')
        pygame.draw.line(self.image, 'white', (0, 0), (self.width, self.width))
        pygame.draw.line(self.image, 'white', (self.width, 0), (0, self.width))
        pygame.draw.line(self.image, 'white', (self.width // 2, 0), (self.width // 2, self.width), 1)
        pygame.draw.line(self.image, 'white', (0, self.width // 2), (self.width, self.width // 2), 1)

    def draw(self, screen):
        screen.blit(self.image, (self.x_pos, self.y_pos))


class Title(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((250, 60))
        self.rect = pygame.Rect(w // 2 - 125, h // 2 - 30, 250, 60)
        self.image.fill('black')
        self.y_coord = -60
        self.v = 1
        self.loading = True
        self.k = 0
        self.color = 'white'
        self.play_button = None
        self.rules = None
        self.all_sprites = pygame.sprite.Group()

    def draw(self, screen):
        if not self.loading:
            if self.k < 80:
                self.k += 1
            else:
                self.k = 0
                self.color = (randint(100, 255), randint(100, 255), randint(100, 255))
            self.v = 0
        elif self.y_coord == h // 2 - 120:
            self.loading = False
            self.play_button = PlayButton((w // 2 - 50, h // 2 - 30), (100, 40))
            self.rules = RulesButton((w // 2 - 50, h // 2 + 30), (100, 40))
            self.all_sprites.add(self.play_button)
            self.all_sprites.add(self.rules)
            return
        self.y_coord += self.v
        self.rect = pygame.Rect(w // 2 - 125, self.y_coord, 250, 60)
        surface = pygame.Surface((250, 60))
        surface.fill('black')
        font = pygame.font.Font(None, 30)
        text = font.render('SPACE RESEARCHER', True, self.color)
        intro_rect = text.get_rect()
        intro_rect.top = 20
        intro_rect.x = 20
        surface.blit(text, intro_rect)
        self.image.blit(surface, (0, 0))
        pygame.draw.rect(self.image, (100, 100, 100), (1, 1, self.image.get_width() - 2, self.image.get_height() - 2), 1)
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Rules(pygame.sprite.Sprite):

    def __init__(self, screen):
        super().__init__()
        self.image = pygame.Surface((500, 500))
        self.rect = pygame.Rect(0, 50, 500, 500)
        self.image.fill('black')
        self.all_sprites = pygame.sprite.Group()
        self.text = ['Ваш исследовательский корабль попал под метеоритный дождь',
                     'и теперь не может вернуться на родную планету!',
                     'Вам предстоит собрать необходимые ресурсы, чтобы починить',
                     'корабль и вернуться домой.',
                     '',
                     'При наведении курсора на планету отображается информация о ней,',
                     'при нажатии начинается миссия по сбору ресурсов.',
                     'Кнопка "поиска" позволяет рассмотреть ближайшие системы,',
                     'при нажатии на систему, если у вас достаточно ресурсов,',
                     'вы попадаете в нее.',
                     'Кнопка с "бортовым компьютером" отправляет вас в инвентарь,',
                     'через него вы можете попасть в окно "починки", где перечислены',
                     'необходимвые для восстановления корабля ресурсы.',
                     'Некоторые ресурсы вы можете использовать, чтобы пополнять',
                     'шкалы сытости (SATIETY) и топлива (FUEL) (не забывайте, что)',
                     'без топлива и пищи вы погибнете). Нажимая "use", вы',
                     'используете ресурсы (ресурс типа "PLANT" добавляет указанное)',
                     'количество очков сытости, ресурс типа "FOSSIL", соответственно,',
                     'пополняет топливный бак.']
        font = pygame.font.Font(None, 20)
        text_coord = 2
        for line in self.text:
            text = font.render(line, True, 'white')
            intro_rect = text.get_rect()
            text_coord += 5
            intro_rect.top = text_coord
            intro_rect.x = 250 - text.get_width() // 2
            text_coord += intro_rect.height
            self.image.blit(text, intro_rect)
        self.button_return = ReturnToMenuButton((w - 170, h - 60), (150, 40))
        screen.blit(self.image, (self.rect.x, self.rect.y))
