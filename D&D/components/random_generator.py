import random
import time


def get_seed():
    with open("data/seed.txt", "r") as f:
        seed = int(f.read())
    return seed


def set_seed(seed=time.time()):
    seed = int(seed)
    with open("data/seed.txt", "w") as f:
        f.write(str(random.randint(0, seed)))


class NumberGenerator(object):
    def __init__(self):
        seed = get_seed()
        random.seed(seed)
        if seed != 0:
            set_seed(seed)
        else:
            set_seed()

    @staticmethod
    def random_integer(a, b):
        return random.randint(a, b)

    @staticmethod
    def random_element(choices):
        return random.choice(choices)
