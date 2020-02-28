from math import floor
from random import choice

import tcod

from components.dice import DiceRoll
from create_monster import get_statistics
from game_messages import Message


def stat_conversion(stat):
    stat = int(stat)
    if stat > 11:
        stat = int(floor((stat - 10) / 2))
    else:
        stat = -int(floor((11 - stat) / 2))
    return stat


class Fighter(object):
    def __init__(self, name):
        self.name = name
        statistics = get_statistics(name)
        attributes = statistics.get("attributes")
        self.max_hp = int(DiceRoll(attributes.get("HP")).roll_dice())
        self.hp = int(self.max_hp)
        self.ac = int(attributes.get("AC"))
        self.xp = attributes.get("XP")
        if self.xp:
            self.xp = int(self.xp)
        self.speed = int(attributes.get("Speed"))
        stats = statistics.get("statistics")
        self.str = stat_conversion(stats["STR"])
        self.dex = stat_conversion(stats["DEX"])
        self.con = stat_conversion(stats["CON"])
        self.int = stat_conversion(stats["INT"])
        self.wis = stat_conversion(stats["WIS"])
        self.cha = stat_conversion(stats["CHA"])
        self.actions = statistics.get("actions")

    def take_damage(self, amount):
        results = []
        self.hp -= amount
        if self.hp <= 0:
            results.append({"dead": self.owner})
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
