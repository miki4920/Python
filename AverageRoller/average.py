from random import randint


def roll_five_drop_extremes():
    number_of_rolls = 0
    total = 0
    while True:
        rolls = []
        for i in range(0, 5):
            rolls.append(randint(1, 6))
        rolls.remove(min(rolls))
        rolls.remove(max(rolls))
        total += sum(rolls)
        number_of_rolls += 1
        if number_of_rolls % 100000:
            print(total/number_of_rolls)


def roll_three_reroll_extremes():
    number_of_rolls = 0
    total = 0
    while True:
        rolls = []
        for i in range(0, 3):
            x = randint(1, 6)
            while x == 1 or x == 6:
                x = randint(1, 6)
            rolls.append(x)
        total += sum(rolls)
        number_of_rolls += 1
        if number_of_rolls % 100000:
            print(total / number_of_rolls)


def roll_four_fours():
    number_of_rolls = 0
    total = 0
    while True:
        rolls = []
        for i in range(0, 4):
            x = randint(1, 4)
            rolls.append(x)
        total += sum(rolls)
        number_of_rolls += 1
        if number_of_rolls % 100000:
            print(total / number_of_rolls)


def roll_four_fours_reroll_ones():
    number_of_rolls = 0
    total = 0
    while True:
        rolls = []
        for i in range(0, 4):
            x = randint(1, 4)
            while x == 1:
                x = randint(1, 4)
            rolls.append(x)
        total += sum(rolls)
        number_of_rolls += 1
        if number_of_rolls % 100000:
            print(total / number_of_rolls)


roll_four_fours_reroll_ones()
