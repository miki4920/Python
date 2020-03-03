from math import floor
from random import choice

import tcod

from components.dice import DiceRoll
from create_monster import get_data
from game_messages import Message


def check_property(item, attribute):
    if item.get(attribute) == "YES":
        return True
    return False


def handle_xp(attributes):
    xp = attributes.get("XP")
    if xp:
        xp = int(xp)
    return xp


def stat_conversion(statistics):
    for stat in statistics:
        stat_value = int(statistics[stat])
        if stat_value > 11:
            stat_value = int(floor((stat_value - 10) / 2))
        else:
            stat_value = -int(floor((11 - stat_value) / 2))
        statistics[stat] = stat_value
    return statistics


class Fighter(object):
    def __init__(self, name):
        self.name = name
        data = get_data(name)
        attributes = data.get("attributes")
        self.max_hp = int(DiceRoll(attributes.get("HP")).roll_dice())
        self.hp = int(self.max_hp)
        self.ac = int(attributes.get("AC"))
        self.xp = handle_xp(attributes)
        self.speed = int(attributes.get("Speed"))
        self.statistics = stat_conversion(data.get("statistics"))
        self.actions = data.get("actions")
        self.finesse = check_property(data.get("properties"), "FINESSE")

    def take_damage(self, amount):
        results = []
        self.hp -= amount
        if self.hp <= 0:
            results.append({'dead': self.owner, 'xp': self.xp})
        return results

    def attack(self, target, attack_weapon, attack_message, no_damage_message, miss_message):
        attack_roll = DiceRoll("1d20+" + attack_weapon.get("HIT")).roll_dice()
        results = []
        if attack_roll >= target.fighter.ac:
            damage = DiceRoll(attack_weapon.get("DAMAGE")).roll_dice()
            if damage > 0:
                results.append({'message': Message(attack_message.format(
                    self.owner.name.capitalize(), target.name, str(damage)), tcod.yellow)})
                results.extend(target.fighter.take_damage(damage))
            else:
                results.append({'message': Message(no_damage_message.format(
                    self.owner.name.capitalize(), target.name), tcod.white)})
        else:
            results.append({'message': Message(miss_message.format(
                self.owner.name.capitalize(), target.name), tcod.white)})
        return results

    def no_weapon(self, message):
        results = [{'message': Message('The {0} does not have a valid {1} weapon'.format(
            self.owner.name.capitalize(), message), tcod.red)}]
        return results

    def melee_attack(self, target):
        melee_weapons = [self.actions[weapon] for weapon in self.actions.keys() if
                         self.actions[weapon].get("RANGE") != "YES"]
        if len(melee_weapons) == 0:
            return self.no_weapon("melee")
        attack_weapon = choice(melee_weapons)
        attack_message = '{0} attacks {1} for {2} hit points.'
        no_damage_message = '{0} attacks {1} but does no damage.'
        miss_message = '{0} attacks {1} but misses.'
        return self.attack(target, attack_weapon, attack_message, no_damage_message, miss_message)

    def range_attack(self, target):
        range_weapons = [self.actions[weapon] for weapon in self.actions.keys() if
                         self.actions[weapon].get("RANGE") == "YES"]
        if len(range_weapons) == 0:
            return self.no_weapon("range")
        attack_weapon = choice(range_weapons)
        attack_message = '{0} shoots {1} and hits for {2} hit points.'
        no_damage_message = '{0} shoots {1} but does no damage.'
        miss_message = '{0} shoots {1} but misses.'
        return self.attack(target, attack_weapon, attack_message, no_damage_message, miss_message)

    def heal(self, amount):
        if type(amount) == int:
            self.hp += amount
        elif type(amount) == str:
            self.hp += DiceRoll(amount).roll_dice()
        if self.hp > self.max_hp:
            self.hp = self.max_hp
