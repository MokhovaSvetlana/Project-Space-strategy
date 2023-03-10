from random import sample, randint

from scales import SatietyScale, FuelScale
from resource import Resource
from settings import RESOURCES_FOR_SAFE_PLANETS, RESOURCES_FOR_MIDDLE_PLANETS, RESOURCES_FOR_DANGEROUS_PLANETS



class Player:
    def __init__(self, system):
        self.system = system

        satiety = 50
        fuel = 50
        self.scale_satiety = SatietyScale(satiety)
        self.scale_fuel = FuelScale(fuel)
        self.resources_for_repair = list()
        self._generate_resources_for_repair()
        self.inventory = list()
        self.add_all_res()
        self.money = 0

    def add_resources(self, resources):
        for res in resources:
            for resi in self.inventory:
                if res.title == resi.title:
                    resi.quantity += res.quantity
                    break
            else:
                self.inventory.append(Resource(res.title, res.type, res.utility, res.image, res.money))
                self.inventory[-1].quantity = res.quantity
                self.inventory.sort(key=lambda res: res.title)

    def subtract_resources(self, resources):
        is_resource_out = False
        for resource in resources:
            for ix, res in enumerate(self.inventory):
                if res.title == resource.title:
                    res.quantity -= 1
                if res.quantity <= 0:
                    is_resource_out = True
                    self.inventory.pop(ix)

        return is_resource_out

    def is_in_inventory(self, resource):
        for res_i in self.inventory:
            if res_i.title == resource.title:
                return res_i.quantity >= resource.quantity
        return False

    def get_resource(self, resource):
        for res_i in self.inventory:
            if res_i.title == resource.title:
                return res_i
        return None

    def add_all_res(self):
        ress = []
        for res in RESOURCES_FOR_SAFE_PLANETS + RESOURCES_FOR_MIDDLE_PLANETS + RESOURCES_FOR_DANGEROUS_PLANETS:
            ress.append(Resource(*res))
            ress[-1].quantity = 25
        self.add_resources(ress)

    def _generate_resources_for_repair(self):
        for res in sample(RESOURCES_FOR_DANGEROUS_PLANETS, k=4):
            resource = Resource(*res)
            resource.quantity = randint(2, 6)
            self.resources_for_repair.append(resource)
        for res in sample(RESOURCES_FOR_MIDDLE_PLANETS, k=5):
            resource = Resource(*res)
            resource.quantity = randint(5, 10)
            self.resources_for_repair.append(resource)
        for res in sample(RESOURCES_FOR_SAFE_PLANETS, k=3):
            resource = Resource(*res)
            resource.quantity = randint(20, 25)
            self.resources_for_repair.append(resource)
