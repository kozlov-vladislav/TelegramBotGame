import units
import random


class Team:
    def __init__(self):
        self.team_members = [types() for types in units.all_unit_types.values()]
        self.units_count = len(self.team_members)

    def add_unit(self, unit):
        if unit is None:
            return
        self.team_members.append(unit)
        self.units_count += 1

    def get_info(self):
        res = '/-------\n'
        for index, unit in enumerate(self.team_members):
            res += f'Unit index {index}:\n'
            res += unit.print_info()
            res += '\n/-------\n'
        return res

    def size(self):
        return self.units_count

    def check_alive(self):
        to_remove = [x for x in self.team_members if not x.is_alive]
        for x in to_remove:
            self.team_members.remove(x)
        self.units_count -= len(to_remove)

    def attack(self, another_team):
        who_attacks = False
        while self.size() > 0 and another_team.size() > 0:
            another_member = another_team.team_members[random.randint(0, another_team.size() - 1)]
            self_member = self.team_members[random.randint(0, self.size() - 1)]
            if who_attacks:
                another_member.attack(self_member)
            else:
                self_member.attack(another_member)
            who_attacks ^= 1
            self.check_alive()
            another_team.check_alive()
        return self.size() > 0


def generate_team(level):
    enemy_team = Team()
    add_members_count = max((level - 10) // 5, 0)
    what_to_add = random.choices(list(units.all_unit_types.values()), k=add_members_count)
    for x in what_to_add:
        enemy_team.add_unit(x())
    return enemy_team
