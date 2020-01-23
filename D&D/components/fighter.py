from math import floor
from random import randint

import tcod

from game_messages import Message


class Fighter(object):
    def __init__(self, hp, armor_class, strength, damage_die):
        self.max_hp = hp
        self.hp = hp
        self.ac = armor_class
        if strength > 11:
            self.str = int(floor((strength-10)/2))
        else:
            self.str = -int(floor((11-strength)/2))
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
