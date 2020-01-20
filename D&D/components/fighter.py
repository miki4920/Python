from math import floor
from random import randint


class Fighter(object):
    def __init__(self, hp, armor_class, strength):
        self.max_hp = hp
        self.hp = hp
        self.ac = armor_class
        if strength > 11:
            self.str = int(floor((strength-10)/2))
        else:
            self.str = -int(floor((11-strength)/2))
        self.str = strength
