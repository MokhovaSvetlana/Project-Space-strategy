import pygame
from random import randint

from planet_system import PlanetSystemSprite
from statuses import Statuses, PlanetSystemStatus, SelectionPlanetSystemsStatus, InventoryStatus
from player import Player
from settings import w, h, menu_h


class Game:

    NUM_SYSTEMS = 5

    def __init__(self):

        pygame.init()
        pygame.display.set_caption("⁖⁘⁙ Space ⁙⁖⁘")

        self.screen = pygame.display.set_mode((w, h))
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.status_data = self.screen, self.clock, self.fps

        self.systems = pygame.sprite.Group()
        self.player = Player(generate_new_system(self.systems).planet_system)
        for i in range(self.NUM_SYSTEMS - 1):
            generate_new_system(self.systems)

        self.running = True
        self.status = PlanetSystemStatus(*self.status_data, self.player)
        self.run()

    def run(self):
        while self.running:
            new_status = self.status.run()
            if new_status is None:
                self.running = False
            elif new_status == Statuses.SelectionPlanetSystems:
                self.status = SelectionPlanetSystemsStatus(*self.status_data, self.systems, self.player.system, self.player)
            elif new_status == Statuses.INVENTORY:
                self.status = InventoryStatus(*self.status_data, self.player)
            elif new_status[0] == Statuses.PlanetSystem:
                self.player.system = new_status[1]
                self.status = PlanetSystemStatus(*self.status_data, self.player)


def generate_new_system(systems):
    system = None
    while system is None:
        radius = randint(15, 30)
        x, y = randint(0, w - 2 * radius), randint(menu_h, h - 2 * radius)
        system = PlanetSystemSprite(x, y, radius)
        if pygame.sprite.spritecollideany(system, systems) or \
                system.rect.bottom > h or system.rect.right > w:
            system = None

    systems.add(system)
    return system


if __name__ == "__main__":
    g = Game()
