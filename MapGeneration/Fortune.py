import random


class PerlinNoise(object):
    def __init__(self, seed=0, octaves=1, frequency=1):
        random.seed(seed)
        self.gradients = ((1, 1), (-1, 1), (1, -1), (-1, -1))

    def calculate_dot_product(self, coords):
        pass
    def generate_point(self, coords):
        x, y = coords
        distance_vectors = ((1-x, 1-y), (x, 1-y), (1-x, y), (x, y))



x = PerlinNoise()
x.generate_point((0.5, 0.3))
