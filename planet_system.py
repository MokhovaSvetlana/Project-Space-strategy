import pygame
import random
from enum import Enum

from planets import Circles, Planet
from resource import Resource
from settings import w, h, menu_h, \
    RESOURCES_FOR_SAFE_PLANETS, \
    RESOURCES_FOR_MIDDLE_PLANETS, \
    RESOURCES_FOR_DANGEROUS_PLANETS, FONT
h -= menu_h


class PlanetSystemSprite(pygame.sprite.Sprite):

    RESOURCES_FONT = 15
    LARGEST_INSCRIPTION = 155

    def __init__(self, x, y, radius):
        super().__init__()
        self.font = pygame.font.Font(None, FONT + 10)
        self.title = self.generate_title()
        self.text = self.font.render(self.title, True, "white")
        self.planet_system = PlanetSystem(self.title)
        self.radius = radius
        self.indent = 10
        self.rect = pygame.Rect(x, y, *self.get_size())
        self.image = pygame.Surface(self.rect.size)
        self.generate_necessary_resources()
        self.visit_allowed = True

    def update(self, current):
        self.image.fill("black")
        if current == self.planet_system:
            self.text = self.font.render(self.title, True, "blue")
        else:
            self.text = self.font.render(self.title, True, "white")

        pygame.draw.circle(self.image, pygame.Color("orange"),
                           (self.rect.w // 2, self.radius), self.radius)
        self.image.blit(self.text, (self.rect.w // 2 - self.text.get_width() // 2,
                                    2 * self.radius + self.indent))

    @staticmethod
    def generate_title():
        title = chr(random.randrange(ord("A"), ord("Z") + 1))
        title += "-"
        title += "".join(str(random.randint(0, 9)) for _ in range(3))
        return title

    def get_size(self):
        return max(self.text.get_width(), 2 * self.radius), \
            (2 * self.radius + self.indent + self.text.get_height())

    def cursor_on_system(self, x, y):
        return self.rect.x <= x <= self.rect.right and \
            self.rect.y <= y <= self.rect.bottom

    def generate_necessary_resources(self):
        self.necessary_resources = list()
        for res in random.sample(RESOURCES_FOR_DANGEROUS_PLANETS, 2) + \
                random.sample(RESOURCES_FOR_MIDDLE_PLANETS, 3):
            self.necessary_resources.append(Resource(*res))
            self.necessary_resources[-1].quantity = 1

    def check_permission(self, player):
        for position in self.necessary_resources:
            if not player.is_in_inventory(position):
                return False
        return True

    def check_necessary_resources(self, inventory, resource):
        for position in inventory:
            if resource in str(position):
                return True
        return False

    def show_necessary_resources(self, screen, inventory):
        x, y = self.rect.center
        surface = pygame.Surface((self.LARGEST_INSCRIPTION, len(self.necessary_resources) * self.RESOURCES_FONT))
        surface.fill('black')
        font = pygame.font.Font(None, self.RESOURCES_FONT)
        text_coord = 2
        for res in self.necessary_resources:
            if self.check_necessary_resources(inventory, res.title):
                color = 'green'
            else:
                color = 'red'
                self.visit_allowed = False
            text = font.render(f'{res.title}: {res.quantity}', True, color)
            intro_rect = text.get_rect()
            text_coord += 3
            intro_rect.top = text_coord
            intro_rect.x = 3
            text_coord += intro_rect.height
            surface.blit(text, intro_rect)

        pygame.draw.rect(surface, 'white', (1, 1, surface.get_width() - 1, surface.get_height() - 1), 1)
        x = min(x, w - self.LARGEST_INSCRIPTION - 10)
        y = min(y, h - len(self.necessary_resources) * self.RESOURCES_FONT - 10)
        screen.blit(surface, (x + 10, y + 10))


class LevelOfDanger(Enum):

    SAFE = 1
    MIDDLE = 2
    DANGEROUS = 3


class PlanetSystem:

    INTERNAL_RADIUS = 60

    def __init__(self, title):
        self.planets = list()
        self.planet_radius = 10
        self.step_for_circle = 30
        self.k_planets = random.randint(5, (min(w, h) - 100) // 2 // self.step_for_circle)
        self.max_circle_radius = self.INTERNAL_RADIUS + (self.k_planets - 1) * self.step_for_circle

        self.all_sprites = pygame.sprite.Group()
        self.planet_sprites = pygame.sprite.Group()
        self.all_sprites.add(Circles(self.max_circle_radius, self.k_planets, self.step_for_circle))
        self.generate_planets()
        for sprite in self.all_sprites:
            sprite.rect.y += menu_h

        self.title = title

    def __repr__(self):
        return self.title

    def generate_planets(self, *level):  # level - на первых этапах больше "safe planets"?
        dangerous_planets = self.k_planets // 4
        middle_planets = (self.k_planets - dangerous_planets) // 2
        safe_planets = self.k_planets - dangerous_planets - middle_planets
        self.levels_planets = list()
        self.levels_planets += [LevelOfDanger.DANGEROUS] * dangerous_planets
        self.levels_planets += [LevelOfDanger.MIDDLE] * middle_planets
        self.levels_planets += [LevelOfDanger.SAFE] * safe_planets
        random.shuffle(self.levels_planets)

        for ix, pl in enumerate(self.levels_planets):
            planet = Planet(ix + 2, self.planet_radius, self.step_for_circle)
            self.all_sprites.add(planet)
            resources, chance, fuel_level = self.choice_of_resources(pl.value)
            planet.generating_information_about_planet(resources, pl.name, chance, fuel_level)
            self.planets.append(planet)
        self.add_planets()

    def add_planets(self):
        for pl in self.planets:
            self.planet_sprites.add(pl)

    def choice_of_resources(self, level_of_danger, *level):   # генерация ресурсов и расчет шанса на успех (больше ресурсов - меньше шанс)
        if level_of_danger == LevelOfDanger.DANGEROUS.value:
            num_of_resources = random.randint(3, 5)
            #k_resource --- ?
            chance_of_success = 100 - num_of_resources * 15    # 25 - 55 %
            resources = random.sample(RESOURCES_FOR_DANGEROUS_PLANETS, num_of_resources)
            fuel_level = random.randint(18, 25)
            return resources, chance_of_success, fuel_level
        elif level_of_danger == LevelOfDanger.MIDDLE.value:
            num_of_resources = random.randint(4, 6)
            chance_of_success = 100 - num_of_resources * 6      # 64 - 76 %
            resources = random.sample(RESOURCES_FOR_MIDDLE_PLANETS, num_of_resources)
            fuel_level = random.randint(7, 11)
            return resources, chance_of_success, fuel_level
        else:
            num_of_resources = random.randint(4, 6)
            chance_of_success = 100 - num_of_resources * 4      # 76 - 84 %
            resources = random.sample(RESOURCES_FOR_SAFE_PLANETS, num_of_resources)
            fuel_level = random.randint(3, 6)
            return resources, chance_of_success, fuel_level

    def show_title(self, screen):
        font = pygame.font.Font(None, menu_h)
        text = font.render(self.title, True, "white")
        screen.blit(text, (w - text.get_width(), 0))
