from utility_functions.random_generator import NumberGenerator


class DiceRoll(object):
    def __init__(self, roll):
        self.dice = []
        self.dice_modifier = 0
        self.handle_roll(roll)

    def handle_roll(self, roll):
        roll = roll.replace(" ", "").lower()
        roll = roll.split("+")
        for die in roll:
            if "d" in die:
                self.dice.append(list(map(int, die.split("d"))))
            else:
                self.dice_modifier += int(die)

    def roll_dice(self):
        result = 0
        for die in self.dice:
            for rolls in range(0, int(die[0])):
                result += NumberGenerator().random_integer(1, int(die[1]))
        return result + self.dice_modifier
