import pygame
import csv
from enum import Enum


class TypesResources(Enum):
    PLANT = 1
    FOSSIL = 2
    JEWEL = 3


class Resource:
    def __init__(self, title, type, utility, image_path, money, k=0):
        self.title = title
        self.quantity = k
        self.type = type
        self.utility = utility
        self.image = image_path
        self.money = money

    def __repr__(self):
        return "<R>" + self.title + f" <{self.quantity}>"

    def show_information(self, rect, screen):
        indent = 25
        image = pygame.image.load(self.image)
        image = pygame.transform.scale(image, (rect.w - 2 * indent, rect.w - 2 * indent))
        screen.blit(image, (rect.x + indent, rect.y + indent))
        color = "white"
        info_h = rect.y + image.get_height() + 2 * indent
        pygame.draw.line(screen, color, (rect.x, info_h), (rect.right, info_h))
        info = self.create_info()
        font = pygame.font.Font(None, 20)
        text_coord = info_h
        for line in info:
            text = font.render(f'{line[0]}: {line[1]}', True, 'white')
            intro_rect = text.get_rect()
            text_coord += 3
            intro_rect.top = text_coord
            intro_rect.x = rect.left + 3
            text_coord += intro_rect.height
            screen.blit(text, intro_rect)

        return text_coord if self.utility != 0 else None

    def create_info(self):
        info = [("Title", self.title), ("Quantity", self.quantity)]
        if self.type == TypesResources.PLANT:
            info.append(("Type", "plant"))
        elif self.type == TypesResources.FOSSIL:
            info.append(("Type", "fossil"))
        elif self.type == TypesResources.JEWEL:
            info.append(("Type", "jewel"))
        if self.utility != 0:
            info.append(("Utility", self.utility))
        return info


def _read_all_resources():
    resources_for_safe_planets = []
    resources_for_middle_planets = []
    resources_for_dangerous_planets = []
    type_of_resource = {'plant': TypesResources.PLANT,
                        'fossil': TypesResources.FOSSIL,
                        'jewel': TypesResources.JEWEL}

    with open('data/resources.csv', encoding="utf8") as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        next(reader)
        for row in reader:

            res = (row[1], type_of_resource[row[2]], int(row[3]), row[4], int(row[5]))
            if row[0] == 'save':
                resources_for_safe_planets.append(res)
            elif row[0] == 'middle':
                resources_for_middle_planets.append(res)
            elif row[0] == 'dangerous':
                resources_for_dangerous_planets.append(res)

    return resources_for_safe_planets, resources_for_middle_planets, \
        resources_for_dangerous_planets
