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
        if not statistics:
            quit()
        attributes = statistics.get("attributes")
        self.max_hp = int(DiceRoll(attributes.get("HP")).roll_dice())
        self.hp = int(self.max_hp)
        self.ac = int(attributes.get("AC"))
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

    def attack(self, target):
        attack_weapon = self.actions[choice(list(self.actions.keys()))]
        attack_roll = DiceRoll("1d20+" + attack_weapon.get("HIT")).roll_dice()
        results = []
        if attack_roll >= target.fighter.ac:
            damage = DiceRoll(attack_weapon.get("DAMAGE")).roll_dice()
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

    def range_attack(self, target):
        attack_weapon = {}
        while attack_weapon.get("RANGE") != "YES":
            attack_weapon = self.actions[choice(list(self.actions.keys()))]
        attack_roll = DiceRoll("1d20+" + attack_weapon.get("HIT")).roll_dice()
        results = []
        if attack_roll >= target.fighter.ac:
            damage = DiceRoll(attack_weapon.get("DAMAGE")).roll_dice()
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

    def heal(self, amount):
        self.hp += DiceRoll(amount).roll_dice()
        if self.hp > self.max_hp:
            self.hp = self.max_hp
