from random import randint


class DiceRoll(object):
    def __init__(self, roll):
        self.dice = []
        self.dice_modifier = 0
        self.handle_roll(roll)

    def handle_roll(self, roll):
        roll = roll.replace(" ", "")
        roll = roll.split("+")
        for _ in roll:
            if "d" in _:
                self.dice.append(_.split("d"))
            else:
                self.dice_modifier += int(_)

    def roll_dice(self):
        result = 0
        for die in self.dice:
            for rolls in range(0, int(die[0])):
                result += randint(1, int(die[1]))
        return result + self.dice_modifier
