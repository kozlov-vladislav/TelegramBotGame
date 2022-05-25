import units
import team
import errors


class Process:
    def __init__(self):
        self.active_status = True
        self.coins = 10
        self.team = team.Team()

    def send_print_units(self):
        return self.team.get_info()

    def attack(self, level):
        another_team = team.generate_team(level)
        result = self.team.attack(another_team)
        if result:
            self.coins += level
            return 'You have won!!!'
        else:
            return 'Sorry, you have been defeated'

    def show_coins(self):
        return f'You have {self.coins} coins'

    def buy(self, name):
        unit_type = units.get_unit(name)
        if unit_type is None:
            return errors.unit_create_error(name)
        if unit_type.get_price() > self.coins:
            return errors.money_error(self.coins, unit_type.get_price())
        self.coins -= unit_type.get_price()
        self.team.add_unit(unit_type())
        return 'Done'

    def upgrade_unit(self, index, type_of, x):
        if x > self.coins:
            return errors.money_error(self.coins, x)
        self.coins -= x
        if type_of == 'damage':
            self.team.team_members[index].damage += x
        else:
            self.team.team_members[index].health += x
        return 'Done'

