import random
from sys import maxsize


def get_seed():
    try:
        with open("data/seed.txt", "r") as f:
            seed = int(f.read())
    except FileNotFoundError:
        with open("data/seed.txt", "w") as f:
            seed = random.randint(0, maxsize * 2 + 1)
            f.write(str(random.randint(0, maxsize * 2 + 1)))
    finally:
        return seed


def set_seed():
    with open("data/seed.txt", "w") as f:
        f.write(str(random.randint(0, maxsize * 2 + 1)))


class NumberGenerator(object):
    def __init__(self):
        seed = get_seed()
        random.seed(seed)
        set_seed()

    @staticmethod
    def random_integer(a, b):
        return random.randint(a, b)

    @staticmethod
    def random_element(choices):
        return random.choice(choices)
