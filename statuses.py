import pygame

from enum import Enum
from abc import ABC, abstractmethod
from buttons import BackButton, SurchButton, InventoryButton, ResourceButton, UseButton
from resource import TypesResources

from settings import w, h, menu_h, FONT
h -= menu_h


class Statuses(Enum):
    PlanetSystem = 1
    SelectionPlanetSystems = 2
    INVENTORY = 3


def switch_to_planet_system():
    return Statuses.PlanetSystem


def switch_to_selection_planet_systems():
    return Statuses.SelectionPlanetSystems


def switch_to_inventory():
    return Statuses.INVENTORY


class Status(ABC):
    def __init__(self, screen, clock, fps):
        self.screen = screen
        self.clock = clock
        self.fps = fps

        self.running = True
        self.next_status = None
        self.all_sprites = pygame.sprite.Group()

    def run(self):
        while self.running:
            self.process_events()
            self.update()
            self.draw()
            self.clock.tick(self.fps)
        return self.next_status

    @abstractmethod
    def process_events(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self):
        pass


class SelectionPlanetSystemsStatus(Status):
    def __init__(self, screen, clock, fps, systems, current_system, player):
        super().__init__(screen, clock, fps)
        self.current_system = current_system
        self.back_button = BackButton((0, 0), (menu_h, menu_h))
        self.systems = systems
        self.cursor_on_system = False
        self.player = player

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                for system in self.systems:
                    if system.cursor_on_system(*event.pos) and (system.check_permission(self.player) or
                                                                system.title == self.current_system.title):
                        if system.planet_system is not self.current_system:
                            self.player.subtract_resources(system.necessary_resources)
                        self.next_status = switch_to_planet_system(), system.planet_system
                        if self.next_status[0] is not None:
                            self.running = False
                if self.back_button.cursor_on_button(*event.pos):
                    self.next_status = switch_to_planet_system(), self.current_system
                    self.running = False

            elif event.type == pygame.MOUSEMOTION:
                for system in self.systems:
                    if system.cursor_on_system(*event.pos) and \
                            system.planet_system is not self.current_system:
                        self.ch_system = system
                        self.cursor_on_system = True
                        break
                else:
                    self.cursor_on_system = False

    def update(self):
        self.systems.update(self.current_system)

    def draw(self):
        self.screen.fill("black")
        self.back_button.draw(self.screen)

        self.systems.draw(self.screen)
        if self.cursor_on_system:
            self.ch_system.show_necessary_resources(self.screen, self.player.inventory)

        pygame.display.flip()


class PlanetSystemStatus(Status):
    def __init__(self, screen, clock, fps, player):
        super().__init__(screen, clock, fps)
        self.player = player
        self.surch_button = SurchButton((0, 0), (menu_h, menu_h))
        self.inventory_button = InventoryButton((menu_h, 0), (menu_h, menu_h))
        self.all_sprites.add(self.player.scale_satiety)
        self.all_sprites.add(self.player.scale_fuel)

        self.SATIETYDROP = pygame.USEREVENT + 1
        pygame.time.set_timer(self.SATIETYDROP, 10000)

        self.cursor_on_planet = False
        self.showing_results = False
        self.planet_is_chosen_for_mission = False

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            for planet in self.player.system.planets:
                if event.type == planet.event:
                    planet.time_for_update -= 1
                    if planet.time_for_update == 0:
                        planet.resources_updating = False
            if event.type == self.SATIETYDROP:
                self.player.scale_satiety.subtract(1)
            if event.type == pygame.MOUSEMOTION:
                if self.showing_results or self.planet_is_chosen_for_mission:
                    continue
                for planet in self.player.system.planets:
                    self.on_planet, self.x, self.y = planet.cursor_on_planet(*event.pos)
                    if self.on_planet:
                        self.cursor_on_planet = True
                        self.ch_planet = planet
                        break
                else:
                    self.cursor_on_planet = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.showing_results or self.planet_is_chosen_for_mission:
                    continue
                for planet in self.player.system.planets:
                    self.on_planet, self.x, self.y = planet.cursor_on_planet(*event.pos)
                    if self.on_planet:
                        if planet.resources_updating:
                            break
                        self.ch_planet = planet
                        self.loss_of_fuel = self.ch_planet.fuel_level
                        if self.loss_of_fuel <= self.player.scale_fuel.occupancy:
                            self.player.scale_fuel.occupancy -= self.loss_of_fuel
                            self.planet_is_chosen_for_mission = True
                        break

                    elif self.surch_button.cursor_on_button(*event.pos):
                        self.next_status = switch_to_selection_planet_systems()
                        self.running = False
                    elif self.inventory_button.cursor_on_button(*event.pos):
                        self.next_status = switch_to_inventory()
                        self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.showing_results:
                    self.showing_results = False

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill('black')

        self.surch_button.draw(self.screen)
        self.inventory_button.draw(self.screen)
        self.player.scale_satiety.draw(self.screen)
        self.player.scale_fuel.draw(self.screen)
        self.player.system.show_title(self.screen)

        self.player.system.all_sprites.draw(self.screen)

        if self.planet_is_chosen_for_mission:
            self.cursor_on_planet = False
            self.planet_is_chosen_for_mission, self.res, self.x1, self.y1 = \
                self.ch_planet.treatment_of_mission(self.fps, self.screen)
            if not self.planet_is_chosen_for_mission:
                self.showing_results = True
                if self.res:
                    self.player.add_resources(self.ch_planet.resources.values())
        if self.showing_results:
            self.cursor_on_planet = False
            self.ch_planet.show_result(self.res, self.x1, self.y1, self.screen)
        elif self.cursor_on_planet:
            self.ch_planet.show_info_about_planet(self.x, self.y, self.player.scale_fuel.occupancy, self.screen)

        pygame.display.flip()


class InventoryStatus(Status):

    W_OF_MAIN_PART = 0.6 * w
    SIZE_USE_BUTTON = 60, 30

    def __init__(self, screen, clock, fps, player):
        super().__init__(screen, clock, fps)
        self.back_button = BackButton((0, 0), (menu_h, menu_h))
        self.player = player
        self.resource_buttons = list()
        self.showed_resource = None
        self.use_button = None
        self.create_resource_buttons()

    def create_resource_buttons(self):
        self.showed_resource = None
        self.use_button = None
        self.resource_buttons = list()
        for ix, resource in enumerate(self.player.inventory):
            self.resource_buttons.append(ResourceButton((0, menu_h + (FONT * ix)),
                                                         (self.W_OF_MAIN_PART, FONT), resource.title, ix))

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.back_button.cursor_on_button(*event.pos):
                    self.next_status = switch_to_planet_system(), self.player.system
                    self.running = False
                for button in self.resource_buttons:
                    if button.cursor_on_button(*event.pos):
                        self.showed_resource = self.player.inventory[button.ix]
                if self.use_button and self.use_button.cursor_on_button(*event.pos):
                    if self.showed_resource.type == TypesResources.PLANT:
                        self.player.scale_satiety.add(self.showed_resource.utility)
                    elif self.showed_resource.type == TypesResources.FOSSIL:
                        self.player.scale_fuel.add(self.showed_resource.utility)
                    is_resource_out = self.player.subtract_resources([self.showed_resource])
                    if is_resource_out:
                        self.create_resource_buttons()

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill('black')
        self.back_button.draw(self.screen)
        # выбор ресурсов
        pygame.draw.rect(self.screen, "white", (0, menu_h, self.W_OF_MAIN_PART, h), width=1)
        if not self.player.inventory:
            font = pygame.font.Font(None, FONT)
            text = font.render("Inventory is empty", True, "white")
            self.screen.blit(text, ((self.W_OF_MAIN_PART - text.get_width()) // 2, h // 2))
        else:
            for button in self.resource_buttons:
                button.draw(self.screen)

        # информация о ресурсе
        pygame.draw.rect(self.screen, "white", (self.W_OF_MAIN_PART, menu_h,
                                                w - self.W_OF_MAIN_PART, h), width=1)
        if self.showed_resource:
            end_info = self.showed_resource.show_information(pygame.rect.Rect(
                (self.W_OF_MAIN_PART, menu_h, w - self.W_OF_MAIN_PART, h)), self.screen)
            if end_info:
                self.use_button = UseButton(
                    (self.W_OF_MAIN_PART + (w - self.W_OF_MAIN_PART - self.SIZE_USE_BUTTON[0]) // 2,
                     end_info + (h // 2 - self.SIZE_USE_BUTTON[1]) // 2), self.SIZE_USE_BUTTON, self.screen)
            else:
                self.use_button = None

            if self.use_button:
                self.use_button.draw(self.screen)

        pygame.display.flip()
