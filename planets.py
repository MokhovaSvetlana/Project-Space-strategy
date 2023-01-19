import pygame
import random
from enum import Enum

from resource import Resource
from settings import w, h, menu_h
from settings import FONT
from settings import n_planet
h -= menu_h


class PlanetType(Enum):

    SAFE = 1
    MIDDLE = 2
    DANGEROUS = 3
    HABITABLE = 4


class Circles(pygame.sprite.Sprite):

    def __init__(self, max_radius, k_circles, step):
        super().__init__()
        self.width = 1
        self.image = pygame.Surface((2 * max_radius, 2 * max_radius))
        for i in range(k_circles):
            pygame.draw.circle(self.image, 'white', (max_radius, max_radius), max_radius - i * step, self.width)
        self.rect = pygame.Rect(w // 2 - max_radius, h // 2 - max_radius, 2 * max_radius, 2 * max_radius)


class Planet(pygame.sprite.Sprite):

    LARGEST_INSCRIPTION = 155

    def __init__(self, line_from_periphery, radius_of_planet, step_for_circle):
        super().__init__()
        self.radius = radius_of_planet
        radius = line_from_periphery * step_for_circle
        min_x, max_x = w // 2 - line_from_periphery * step_for_circle, w // 2 + line_from_periphery * step_for_circle
        x = random.randrange(min_x, max_x)
        x_pos = abs(w // 2 - x)
        y_pos = int((radius ** 2 - x_pos ** 2) ** 0.5)
        y = random.choice((h // 2 + y_pos, h // 2 - y_pos))
        self.image = pygame.Surface((2 * radius_of_planet, 2 * radius_of_planet))
        pygame.draw.circle(self.image, 'grey', (radius_of_planet, radius_of_planet), radius_of_planet)
        self.rect = pygame.Rect(x - radius_of_planet, y - radius_of_planet, 2 * radius_of_planet, 2 * radius_of_planet)
        self.resources_updating = False
        self.time_for_update = 0
        n_planet[0] += 1
        self.n = n_planet[0]
        self.event = pygame.USEREVENT + self.n

        self.width_of_line_success = 0
        self.gr = 0

    def cursor_on_planet(self, x, y):
        x_center = self.rect.x + self.radius // 2
        if (self.rect.x <= x <= self.rect.x + 2 * self.radius) and (self.rect.y <= y <= self.rect.y + 2 * self.radius):
            return True, x_center, self.rect.y
        return False, None, None

    def generating_information_about_planet(self, resources: dict, type, chance, fuel_level):
        self.resources = dict()
        for resource in resources:
            res = Resource(*resource)
            self.resources[res.title] = res
            self.resources[res.title].quantity = 1

        self.type = type
        if type == PlanetType.HABITABLE:
            self.info = ['HABITABLE PLANET', 'Сome to planet to trading']
        else:
            self.info = {'Level of danger': self.type.name}
            self.chance = chance
            self.info['Chance of success'] = f"{self.chance}%"
            self.fuel_level = fuel_level
            self.info['Need fuel'] = f"{self.fuel_level}"
            for position in self.resources:
                self.info[position] = self.resources[position].quantity

    def show_info_about_planet(self, x, y, fuel_occupancy, screen):
        if self.resources_updating:
            strings = ['Resources are updating', f"Please, wait {self.time_for_update}s"]
            surface = pygame.Surface((self.LARGEST_INSCRIPTION, len(strings) * FONT))
            surface.fill('black')
            font = pygame.font.Font(None, FONT)
            text_coord = 2
            for line in strings:
                text = font.render(line, True, 'white')
                intro_rect = text.get_rect()
                text_coord += 3
                intro_rect.top = text_coord
                intro_rect.x = 3
                text_coord += intro_rect.height
                surface.blit(text, intro_rect)
            pygame.draw.rect(surface, 'white', (1, 1, surface.get_width() - 1, surface.get_height() - 1), 1)

            x = min(x, w - self.LARGEST_INSCRIPTION)
            y = min(y, h - len(strings) * FONT)
            screen.blit(surface, (x, y))
            return

        surface = pygame.Surface((self.LARGEST_INSCRIPTION, len(self.info) * FONT))
        surface.fill('black')
        font = pygame.font.Font(None, FONT)
        text_coord = 2
        for line in self.info:
            if line == 'Need fuel' and fuel_occupancy >= int(self.info[line]):
                color = 'green'
            elif line == 'Need fuel' and fuel_occupancy < int(self.info[line]):
                color = 'red'
            else:
                color = 'white'
            text = font.render(f'{line}: {self.info[line]}' if self.type is not PlanetType.HABITABLE else line,
                               True, color)
            intro_rect = text.get_rect()
            text_coord += 3
            intro_rect.top = text_coord
            intro_rect.x = 3
            text_coord += intro_rect.height
            surface.blit(text, intro_rect)

        pygame.draw.rect(surface, 'white', (1, 1, surface.get_width() - 1, surface.get_height() - 1), 1)
        if x is not None:
            x = min(x, w - self.LARGEST_INSCRIPTION)
            y = min(y, h - len(self.info) * FONT)
            screen.blit(surface, (x, y))

    def mission_calculation(self):
        variants = [1] * self.chance + [0] * (100 - self.chance)
        random.shuffle(variants)
        result_of_mission = random.choice(variants)
        return result_of_mission

    def treatment_of_mission(self, fps, screen):
        self.v = 100 // fps

        surface = pygame.Surface((120, 40))
        surface.fill((80, 80, 80))
        font = pygame.font.Font(None, FONT)
        text_coord = 2
        text = font.render('Mission in progress...', True, 'white')
        intro_rect = text.get_rect()
        text_coord += 4
        intro_rect.top = text_coord
        intro_rect.x = 3
        text_coord += intro_rect.height
        surface.blit(text, intro_rect)
        pygame.draw.rect(surface, 'white', (3, text_coord + FONT // 2, surface.get_width() - 6, surface.get_height() - 25), 1)
        self.width_of_line_success += self.v
        self.width_of_line_success = min(surface.get_width() - 1, self.width_of_line_success)
        pygame.draw.rect(surface, 'white', (3, text_coord + FONT // 2, self.width_of_line_success - 6, surface.get_height() - 25))
        x = self.rect.x + self.radius // 2 - text.get_width() // 2
        y = self.rect.y - surface.get_height()

        y = max(y, 1)

        if self.width_of_line_success != surface.get_width() - 6:
            screen.blit(surface, (x, y))
            return True, None, None, None
        else:
            result = self.mission_calculation()
            self.show_result(result, x, y, screen)
            self.width_of_line_success = 0
            return False, result, x, y

    def show_result(self, result, x, y, screen):
        color = 'green' if result else 'red'
        result = 'SUCCESSFUL' if result else 'FAILED'
        surface = pygame.Surface((125, 40))
        surface.fill('black')
        font = pygame.font.Font(None, FONT)
        text1 = font.render('mission', True, 'white')
        text2 = font.render(result, True, color)
        intro_rect = text1.get_rect()
        intro_rect.top = 3
        intro_rect.x = 3
        surface.blit(text1, intro_rect)
        intro_rect = text2.get_rect()
        intro_rect.top = 3
        intro_rect.x = text1.get_width() + 6
        surface.blit(text2, intro_rect)
        text3 = font.render('Press <space> to close', True, 'white')
        intro_rect = text3.get_rect()
        intro_rect.bottom = surface.get_height() - 4
        intro_rect.right = surface.get_width() - 4
        pygame.draw.rect(surface, 'white', (1, 1, surface.get_width() - 2, surface.get_height() - 2), 1)
        pygame.draw.rect(surface, 'white', (intro_rect.x - 3, intro_rect.y - 3, text3.get_width() + 6, text3.get_height() + 6), 1)
        surface.blit(text3, intro_rect)

        y = max(y, 1)

        screen.blit(surface, (x, y))
        self.resources_updating = True
        self.time_for_update = 10
        pygame.time.set_timer(self.event, 1000)
