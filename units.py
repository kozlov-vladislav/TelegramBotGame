from abc import abstractmethod


class Unit(object):
    def __init__(self):
        self.health = 0
        self.damage = 0
        self.is_alive = True
        self.type = ''

    def print_info(self):
        return f'type = {self.type},\nhealth = {self.health},\ndamage = {self.damage}'

    def change_health(self, new_health):
        pass

    def attack(self, another_unit):
        if another_unit.health <= self.damage:
            another_unit.is_alive = False
            return True
        another_unit.change_health(another_unit.health - self.damage)
        return False

    @classmethod
    def get_name(cls):
        pass

    @classmethod
    def get_price(cls):
        pass


class Warrior(Unit):
    def __init__(self):
        super().__init__()
        self.health = 15
        self.damage = 15
        self.type = 'Warrior'

    @staticmethod
    def get_price():
        return 9

    @staticmethod
    def get_name():
        return 'Warrior'

    def change_health(self, new_health):
        if new_health >= self.health:
            self.health = new_health
            return
        delta = 1.0 * new_health / self.health
        self.health, self.damage = new_health, self.damage * delta


class Defender(Unit):
    def __init__(self):
        super().__init__()
        self.health = 23
        self.damage = 10
        self.type = 'Defender'

    @staticmethod
    def get_price():
        return 10

    @staticmethod
    def get_name():
        return 'Defender'

    def change_health(self, new_health):
        if new_health >= self.health:
            self.health = new_health
            return
        delta = 1.0 * new_health / self.health
        self.health, self.damage = (self.health + new_health) / 2, self.damage * delta


class Berserk(Unit):
    def __init__(self):
        super().__init__()
        self.health = 7
        self.damage = 30
        self.type = 'Berserk'

    @staticmethod
    def get_price():
        return 15

    @staticmethod
    def get_name():
        return 'Berserk'

    def change_health(self, new_health):
        if new_health >= self.health:
            self.health = new_health
            return
        delta = 1.0 * new_health / self.health
        self.health, self.damage = new_health, self.damage * (2 - delta)


class Factory:
    @abstractmethod
    def get_unit(self):
        pass


class WarriorFactory(Factory):
    def get_unit(self):
        return Warrior()


class DefenderFactory(Factory):
    def get_unit(self):
        return Defender()


class BerserkFactory(Factory):
    def get_unit(self):
        return Berserk()





all_unit_types = {}


def get_unit(unit_name):
    return all_unit_types.get(unit_name)

