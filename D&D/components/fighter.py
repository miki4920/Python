from math import floor
from random import choice

import tcod
from monster_functions import get_monster_by_name, get_monster_hit_chance, get_monster_xp
from components.dice import DiceRoll
from game_messages import Message


def check_property(item, attribute):
    if item.get(attribute) == "YES":
        return True
    return False


def stat_conversion(statistics):
    for stat in statistics:
        statistics[stat] = floor(int(statistics[stat]) / 2) - 5
    return statistics


def get_hit_chance(name, strength, dexterity):
    bonus = max(strength, dexterity)
    return get_monster_hit_chance(name) + bonus, bonus


class Fighter(object):
    def __init__(self, name):
        monster = get_monster_by_name(name)
        description = monster.get("Description")
        self.name = description.get("Name")
        self.statistics = stat_conversion(monster.get("Statistics"))
        attributes = monster.get("Attributes")

        hp = attributes.get("HP")
        self.max_hp = DiceRoll(hp).roll_dice() + int(self.statistics["CON"])*int(hp.lower().split("d")[0])
        self.hp = self.max_hp
        self.ac = int(attributes.get("AC"))
        self.cr = attributes.get("CR")
        self.xp = get_monster_xp(self.cr)
        self.speed = attributes.get("Speed")
        self.actions = monster.get("Actions")
        self.hit, self.damage_bonus = get_hit_chance(name, self.statistics["STR"], self.statistics["DEX"])

    def take_damage(self, amount):
        results = []
        self.hp -= amount
        if self.hp <= 0:
            results.append({'dead': self.owner, 'xp': self.xp})
        return results

    def attack(self, target, attack_weapon, attack_message, no_damage_message, miss_message):
        attack_roll = DiceRoll("1d20").roll_dice() + self.hit
        results = []
        if attack_roll >= target.fighter.ac:
            damage = DiceRoll(attack_weapon.get("Damage")).roll_dice() + self.damage_bonus
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
                         int(self.actions[weapon].get("Range")) <= 5]
        if len(melee_weapons) == 0:
            return self.no_weapon("melee")
        attack_weapon = choice(melee_weapons)
        attack_message = '{0} attacks {1} for {2} hit points.'
        no_damage_message = '{0} attacks {1} but does no damage.'
        miss_message = '{0} attacks {1} but misses.'
        return self.attack(target, attack_weapon, attack_message, no_damage_message, miss_message)

    def range_attack(self, target):
        range_weapons = [self.actions[weapon] for weapon in self.actions.keys() if
                         int(self.actions[weapon].get("Range")) > 5]
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
