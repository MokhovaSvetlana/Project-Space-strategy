import pygame
from random import randint, choice

from enum import Enum
from abc import ABC, abstractmethod

from main_menu_sprites import Star, Title, Rules
from end_of_game_sprite import ResultScreen
from buttons import BackButton, SurchButton, SpaceshipButton, \
    InventoryButton, RepairingButton, ResourceButton, UseButton, RepairSpaceshipButton, \
    TradeResourceButton, TradeStatusButton
from resource import TypesResources
from planets import PlanetType

from settings import w, h, menu_h, FONT
h -= menu_h


class Statuses(Enum):
    PlanetSystem = 1
    SelectionPlanetSystems = 2
    Inventory = 3
    Repair = 4
    MainMenu = 5
    EndOfGame = 6
    Rules = 7
    SellResources = 8
    BuyResources = 9


def switch_to_planet_system(system):
    return Statuses.PlanetSystem, system


def switch_to_selection_planet_systems():
    return Statuses.SelectionPlanetSystems


def switch_to_inventory(previous_status):
    return Statuses.Inventory, previous_status


def switch_to_repair(previous_status):
    return Statuses.Repair, previous_status


def switch_to_end(result, purpose):
    return Statuses.EndOfGame, result, purpose


def switch_to_main_menu(previous_status):
    return Statuses.MainMenu, previous_status


def switch_to_rules(previous_status):
    return Statuses.Rules, previous_status


def switch_to_sell_resources():
    return Statuses.SellResources


def switch_to_buy_resources():
    return Statuses.BuyResources


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


class MainMenu(Status):
    def __init__(self, screen, clock, fps):
        super().__init__(screen, clock, fps)
        self.stars = pygame.sprite.Group()
        n = 1
        for i in range(25):
            x, y = randint(0, w), randint(0, h)
            star = Star(x, y, n)
            while pygame.sprite.spritecollideany(star, self.stars):
                x, y = randint(0, w), randint(0, h)
                star = Star(x, y, n)
            self.stars.add(star)
            self.all_sprites.add(star)
            n += 1
        self.title = Title()
        self.all_sprites.add(self.title)

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.title.play_button and self.title.play_button.cursor_on_button(*event.pos):
                    self.next_status = switch_to_planet_system(None)
                    self.running = False
                if self.title.rules and self.title.rules.cursor_on_button(*event.pos):
                    self.next_status = switch_to_rules(None)
                    self.running = False
            for st in self.stars:
                if event.type == st.event:
                    st.shine = True

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill('black')
        self.all_sprites.draw(self.screen)
        if not self.title.loading:
            self.stars.draw(self.screen)

        self.title.draw(self.screen)
        if self.title.play_button is not None:
            self.title.play_button.draw(self.screen)
        if self.title.rules is not None:
            self.title.rules.draw(self.screen)
        pygame.display.flip()


class RulesScreen(Status):

    def __init__(self, screen, clock, fps):
        super().__init__(screen, clock, fps)
        self.text = Rules(screen)
        self.all_sprites.add(self.text)

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.text.button_return and self.text.button_return.cursor_on_button(*event.pos):
                    self.next_status = switch_to_main_menu(None)
                    self.running = False

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill('black')
        self.all_sprites.draw(self.screen)

        self.text.button_return.draw(self.screen)
        pygame.display.flip()


class PlanetSystemStatus(Status):
    def __init__(self, screen, clock, fps, player):
        super().__init__(screen, clock, fps)
        self.player = player
        self.surch_button = SurchButton((0, 0), (menu_h, menu_h))
        self.spaceship_button = SpaceshipButton((menu_h, 0), (menu_h, menu_h))
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
            elif event.type == self.SATIETYDROP:
                self.player.scale_satiety.subtract(1)
            elif event.type == self.player.system.TRADEUBDATE:
                self.player.system.generate_resources_for_trade()
            elif event.type == pygame.MOUSEMOTION:
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.showing_results or self.planet_is_chosen_for_mission:
                    continue
                for planet in self.player.system.planets:
                    self.on_planet, self.x, self.y = planet.cursor_on_planet(*event.pos)
                    if self.on_planet:
                        if planet.type == PlanetType.HABITABLE:
                            self.next_status = switch_to_sell_resources()
                            self.running = False
                        else:
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
                    elif self.spaceship_button.cursor_on_button(*event.pos):
                        self.next_status = switch_to_inventory(Statuses.PlanetSystem)
                        self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.showing_results:
                    self.showing_results = False
                elif event.key == pygame.K_i:
                    self.next_status = switch_to_inventory(Statuses.PlanetSystem)
                    self.running = False
            for planet in self.player.system.planets:
                if event.type == planet.event:
                    planet.time_for_update -= 1
                    if planet.time_for_update == 0:
                        planet.resources_updating = False

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill('black')

        self.surch_button.draw(self.screen)
        self.spaceship_button.draw(self.screen)
        self.player.scale_satiety.draw(self.screen)
        self.player.scale_fuel.draw(self.screen)
        self.player.system.show_title(self.screen)

        self.player.system.all_sprites.draw(self.screen)

        if self.player.scale_satiety.occupancy == 0:
            self.running = False
            self.next_status = switch_to_end(0, 'satiety')
            return

        elif self.player.scale_fuel.occupancy == 0:
            self.running = False
            self.next_status = switch_to_end(0, 'fuel')
            return

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


class SelectionPlanetSystemsStatus(Status):
    def __init__(self, screen, clock, fps, systems, player):
        super().__init__(screen, clock, fps)
        self.back_button = BackButton((0, 0), (menu_h, menu_h))
        self.spaceship_button = SpaceshipButton((menu_h, 0), (menu_h, menu_h))

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
                                                                system.title == self.player.system.title):
                        if system.planet_system is not self.player.system:
                            self.player.subtract_resources(system.necessary_resources)
                        self.next_status = switch_to_planet_system(system.planet_system)
                        if self.next_status[0] is not None:
                            self.running = False
                if self.back_button.cursor_on_button(*event.pos):
                    self.next_status = switch_to_planet_system(self.player.system)
                    self.running = False
                elif self.spaceship_button.cursor_on_button(*event.pos):
                    self.next_status = switch_to_inventory(Statuses.SelectionPlanetSystems)
                    self.running = False
            elif event.type == pygame.MOUSEMOTION:
                for system in self.systems:
                    if system.cursor_on_system(*event.pos) and \
                            system.planet_system is not self.player.system:
                        self.ch_system = system
                        self.cursor_on_system = True
                        break
                else:
                    self.cursor_on_system = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    self.next_status = switch_to_inventory(Statuses.SelectionPlanetSystems)
                    self.running = False

    def update(self):
        self.systems.update(self.player.system)

    def draw(self):
        self.screen.fill("black")
        self.back_button.draw(self.screen)
        self.spaceship_button.draw(self.screen)

        self.systems.draw(self.screen)
        if self.cursor_on_system:
            self.ch_system.show_necessary_resources(self.screen, self.player.inventory)

        pygame.display.flip()


class InventoryStatus(Status):

    W_OF_MAIN_PART = 0.6 * w
    SIZE_USE_BUTTON = 60, 30

    def __init__(self, screen, clock, fps, player, previous_status):
        super().__init__(screen, clock, fps)
        self.back_button = BackButton((0, 0), (menu_h, menu_h))
        self.inventory_button = InventoryButton((menu_h, 0), (menu_h, menu_h))
        self.repairing_button = RepairingButton((2 * menu_h, 0), (menu_h, menu_h))
        self.player = player
        self.previous_status = previous_status
        self.showed_resource = None
        self.use_button = None
        self.resource_buttons = list()
        self.create_resource_buttons()

    def create_resource_buttons(self):
        self.showed_resource = None
        self.use_button = None
        self.resource_buttons = list()
        start = 10
        for ix, resource in enumerate(self.player.inventory):
            self.resource_buttons.append(ResourceButton((10, menu_h + start + (FONT * ix)),
                                                        (self.W_OF_MAIN_PART - 20, FONT), resource.title, ix))

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.back_button.cursor_on_button(*event.pos):
                    if self.previous_status == Statuses.PlanetSystem:
                        self.next_status = switch_to_planet_system(self.player.system)
                    elif self.previous_status == Statuses.SelectionPlanetSystems:
                        self.next_status = switch_to_selection_planet_systems()
                    self.running = False
                elif self.repairing_button.cursor_on_button(*event.pos):
                    self.next_status = switch_to_repair(self.previous_status)
                    self.running = False
                elif self.use_button and self.use_button.cursor_on_button(*event.pos):
                    if self.showed_resource.type == TypesResources.PLANT:
                        self.player.scale_satiety.add(self.showed_resource.utility)
                    elif self.showed_resource.type == TypesResources.FOSSIL:
                        self.player.scale_fuel.add(self.showed_resource.utility)
                    is_resource_out = self.player.subtract_resources([self.showed_resource])
                    if is_resource_out:
                        self.create_resource_buttons()
                for button in self.resource_buttons:
                    if button.cursor_on_button(*event.pos):
                        self.showed_resource = self.player.inventory[button.ix]

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill('black')
        self.back_button.draw(self.screen)
        self.repairing_button.draw(self.screen)
        self.draw_selection_resources()
        self.draw_showed_resource()
        pygame.display.flip()

    def draw_selection_resources(self):
        pygame.draw.rect(self.screen, "white", (0, menu_h, self.W_OF_MAIN_PART, h), width=1)
        if not self.player.inventory:
            font = pygame.font.Font(None, FONT)
            text = font.render("Inventory is empty", True, "white")
            self.screen.blit(text, ((self.W_OF_MAIN_PART - text.get_width()) // 2, h // 2))
        else:
            for button in self.resource_buttons:
                button.draw(self.screen)

    def draw_showed_resource(self):
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

        self.inventory_button.draw(self.screen)
        self.inventory_button.break_contour(self.screen)


class RepairStatus(Status):

    def __init__(self, screen, clock, fps, player, previous_status):
        super().__init__(screen, clock, fps)
        self.player = player
        self.previous_status = previous_status

        self.back_button = BackButton((0, 0), (menu_h, menu_h))
        self.inventory_button = InventoryButton((menu_h, 0), (menu_h, menu_h))
        self.repair_spaceship_button = None

        self.repairing_button = RepairingButton((2 * menu_h, 0), (menu_h, menu_h))

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.back_button.cursor_on_button(*event.pos):
                    if self.previous_status == Statuses.PlanetSystem:
                        self.next_status = switch_to_planet_system(self.player.system)
                    elif self.previous_status == Statuses.SelectionPlanetSystems:
                        self.next_status = switch_to_selection_planet_systems()
                    self.running = False
                elif self.repair_spaceship_button is not None and \
                        self.repair_spaceship_button.cursor_on_button(*event.pos):
                    self.next_status = switch_to_end(1, 'win')
                    self.running = False
                elif self.inventory_button.cursor_on_button(*event.pos):
                    self.next_status = switch_to_inventory(self.previous_status)
                    self.running = False

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill("black")
        self.back_button.draw(self.screen)
        self.inventory_button.draw(self.screen)

        pygame.draw.rect(self.screen, "white", (0, menu_h, w, h), width=1)

        color = "white"
        text_h = menu_h + 20
        font = pygame.font.Font(None, FONT + 15)
        text = font.render("Repairing spaceship", True, color)
        self.screen.blit(text, (3, text_h))
        text_h += text.get_height()

        font = pygame.font.Font(None, FONT + 8)
        text = font.render("Necessary resources: ", True, color)
        self.screen.blit(text, (3, text_h + 10))
        text_h += text.get_height() + 20

        for resource in self.player.resources_for_repair:
            color = "green" if self.player.is_in_inventory(resource) else "red"
            text = font.render(f"{resource.title} : {resource.quantity}", True, color)
            self.screen.blit(text, (20, text_h + 10))
            text_h += text.get_height() + 10

        if all((self.player.is_in_inventory(res) for res in self.player.resources_for_repair)):
            self.repair_spaceship_button = RepairSpaceshipButton((w // 2, menu_h + 10), (w // 2 - 10, 50))
        else:
            self.repair_spaceship_button = None

        if self.repair_spaceship_button is not None:
            self.repair_spaceship_button.draw(self.screen)

        self.repairing_button.draw(self.screen)
        self.repairing_button.break_contour(self.screen)
        pygame.display.flip()


class EndOfGame(Status):
    def __init__(self, screen, clock, fps, result, purpose):
        super().__init__(screen, clock, fps)
        self.stars = pygame.sprite.Group()
        n = 1
        for i in range(25):
            x, y = randint(0, w), randint(0, h)
            star = Star(x, y, n)
            while pygame.sprite.spritecollideany(star, self.stars):
                x, y = randint(0, w), randint(0, h)
                star = Star(x, y, n)
            self.stars.add(star)
            self.all_sprites.add(star)
            n += 1
        if result == 0:
            if purpose == 'satiety':
                text_result = [choice(['Пища закончилась...', 'Голод стал нестерпим...',
                                       'Вас настигла голодная смерть...', 'А нужен был всего лишь один корешок!..'])]
            else:
                text_result = [choice(['Всё топливо израсходовано...', 'Двигатели отказали...',
                                       'Ваш корабль дрейфует в неизвестности...'])]
        else:
            text_result = ['Корабль успешно добрался до дома!', 'Спасибо за путешествие, капитан!']
        self.text = ResultScreen(result, text_result, self.screen)
        self.all_sprites.add(self.text)

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            for st in self.stars:
                if event.type == st.event:
                    st.shine = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.text.button_outplay and self.text.button_outplay.cursor_on_button(*event.pos):
                    self.next_status = switch_to_planet_system(None)
                    self.running = False
                if self.text.button_return and self.text.button_return.cursor_on_button(*event.pos):
                    self.next_status = switch_to_main_menu(None)
                    self.running = False

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill('black')
        self.stars.draw(self.screen)
        self.all_sprites.draw(self.screen)

        self.text.button_outplay.draw(self.screen)
        self.text.button_return.draw(self.screen)
        pygame.display.flip()


class SellResourcesStatus(Status):
    def __init__(self, screen, clock, fps, player):
        super().__init__(screen, clock, fps)
        self.player = player
        self.back_button = BackButton((0, 0), (menu_h, menu_h))
        self.sell_button = TradeStatusButton((menu_h, 0), (2 * menu_h, menu_h), is_selling=True)
        self.buy_button = TradeStatusButton((3 * menu_h, 0), (2 * menu_h, menu_h), is_selling=False)
        self.selling_resources_buttons = list()
        self.num_rows, self.num_cols = 3, 4
        cell_w, cell_h = w // self.num_cols, h // self.num_rows
        indent = 10
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                if row * self.num_cols + col < len(self.player.system.resources_for_sell):
                    self.selling_resources_buttons.append(
                        TradeResourceButton((col * cell_w + indent, row * cell_h + indent + menu_h),
                                            (cell_w - 2 * indent, cell_h - 2 * indent),
                                            self.player.system.resources_for_sell[row * self.num_cols + col]))
                else:
                    break

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.back_button.cursor_on_button(*event.pos):
                    self.next_status = switch_to_planet_system(self.player.system)
                    self.running = False
                elif self.buy_button.cursor_on_button(*event.pos):
                    self.next_status = switch_to_buy_resources()
                    self.running = False
                for button in self.selling_resources_buttons:
                    if button.cursor_on_button(*event.pos) and self.player.is_in_inventory(button.resource):
                        self.player.subtract_resources([button.resource])
                        self.player.money += button.money

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill("black")
        self.back_button.draw(self.screen)
        self.sell_button.draw(self.screen)
        self.buy_button.draw(self.screen)
        font = pygame.font.Font(None, menu_h)
        text = font.render(f"Moneys: {self.player.money}", True, "white")
        self.screen.blit(text, (w - text.get_width() - 10, menu_h - text.get_height()))
        for button in self.selling_resources_buttons:
            button.draw(self.screen, self.player.get_resource(button.resource))
        pygame.display.flip()


class BuyResourcesStatus(Status):
    def __init__(self, screen, clock, fps, player):
        super().__init__(screen, clock, fps)
        self.player = player
        self.back_button = BackButton((0, 0), (menu_h, menu_h))
        self.sell_button = TradeStatusButton((menu_h, 0), (2 * menu_h, menu_h), is_selling=True)
        self.buy_button = TradeStatusButton((3 * menu_h, 0), (2 * menu_h, menu_h), is_selling=False)
        self.selling_resources_buttons = list()
        self.num_rows, self.num_cols = 3, 4
        cell_w, cell_h = w // self.num_cols, h // self.num_rows
        indent = 10
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                if row * self.num_cols + col < len(self.player.system.resources_for_buy):
                    self.selling_resources_buttons.append(
                        TradeResourceButton((col * cell_w + indent, row * cell_h + indent + menu_h),
                                            (cell_w - 2 * indent, cell_h - 2 * indent),
                                            self.player.system.resources_for_buy[row * self.num_cols + col],
                                            is_selling=False))
                else:
                    break

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.back_button.cursor_on_button(*event.pos):
                    self.next_status = switch_to_planet_system(self.player.system)
                    self.running = False
                elif self.sell_button.cursor_on_button(*event.pos):
                    self.next_status = switch_to_sell_resources()
                    self.running = False
                for button in self.selling_resources_buttons:
                    if button.cursor_on_button(*event.pos) and self.player.money >= button.money:
                        self.player.add_resources([button.resource])
                        self.player.money -= button.money

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill("black")
        self.back_button.draw(self.screen)
        self.sell_button.draw(self.screen)
        self.buy_button.draw(self.screen)
        font = pygame.font.Font(None, menu_h)
        text = font.render(f"Moneys: {self.player.money}", True, "white")
        self.screen.blit(text, (w - text.get_width() - 10, menu_h - text.get_height()))
        for button in self.selling_resources_buttons:
            button.draw(self.screen, self.player.get_resource(button.resource))
        pygame.display.flip()
