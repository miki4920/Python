from math import floor
from random import randint

import tcod

from game_messages import Message


def stat_conversion(stat):
    if stat > 11:
        stat = int(floor((stat - 10) / 2))
    else:
        stat = -int(floor((11 - stat) / 2))
    return stat


class Fighter(object):
    def __init__(self, hp, armor_class, strength, damage_die):
        self.max_hp = hp
        self.hp = hp
        self.ac = armor_class
        self.str = stat_conversion(strength)
        # self.str = stat_conversion(stats["strength"])
        # self.dex = stat_conversion(stats["dexterity"])
        # self.con = stat_conversion(stats["constitution"])
        # self.int = stat_conversion(stats["intelligence"])
        # self.wis = stat_conversion(stats["wisdom"])
        # self.cha = stat_conversion(stats["charisma"])
        self.damage_die = damage_die

    def take_damage(self, amount):
        results = []
        self.hp -= amount
        if self.hp <= 0:
            results.append({"dead": self.owner})
        return results

    def attack(self, target):
        attack_roll = randint(1, 20) + self.str
        results = []
        if attack_roll >= target.fighter.ac:
            damage = randint(self.damage_die[0], self.damage_die[1]) + self.str
            if damage > 0:
                results.append({'message': Message('{0} attacks {1} for {2} hit points.'.format(
                    self.owner.name.capitalize(), target.name, str(damage)), tcod.yellow)})
                results.extend(target.fighter.take_damage(damage))
            else:
                results.append({'message': Message('{0} attacks {1} but does no damage.'.format(
                    self.owner.name.capitalize(), target.name), tcod.white)})
        else:
            results.append({'message': Message('{0} attacks {1} but misses.'.format(
                self.owner.name.capitalize(), target.name))})
        return results
