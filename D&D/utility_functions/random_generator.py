import random
from sys import maxsize
import os


def get_seed():
    if not os.path.exists("data"):
        os.mkdir("data")
    if not os.path.exists("data/seed.txt"):
        with open("data/seed.txt", "w") as f:
            seed = random.randint(0, maxsize * 2 + 1)
            f.write(str(random.randint(0, maxsize * 2 + 1)))
    else:
        with open("data/seed.txt", "r") as f:
            seed = int(f.read())

    return seed


def set_seed():
    with open("data/seed.txt", "w") as f:
        f.write(str(random.randint(0, maxsize * 2 + 1)))


class NumberGenerator(object):
    @staticmethod
    def seed():
        seed = get_seed()
        random.seed(seed)
        set_seed()

    @staticmethod
    def random_integer(a, b):
        return random.randint(a, b)

    @staticmethod
    def random_element(choices):
        return random.choice(choices)
