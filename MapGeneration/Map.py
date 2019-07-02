from PIL import Image
import random
from itertools import product


class PerlinNoise(object):
    def __init__(self, side_size):
        self.length = side_size**2
        self.gradients = {}
        self.values = self.values = list(product([i/side_size for i in range(0, side_size)], repeat=2))
        self.noise = [0] * self.length
        for i in list(product([0, 1], repeat=2)):
            vectors = [random.gauss(0, 1) for _ in range(2)]
            modulus = (vectors[0] ** 2 + vectors[1] ** 2) ** (-0.5)
            self.gradients[i] = [vectors[0] * modulus, vectors[1] * modulus]
        self.generate_noise()

    def generate_noise(self):
        for i in range(0, self.length):
            dots = []
            for coordinates in self.gradients:
                dot = self.dot_product(self.gradients[coordinates],
                [self.values[i][0]-coordinates[0], self.values[i][1]-coordinates[1]])
                dots.append(dot)
            self.noise[i] = self.find_average(self.values[i], dots)

    def find_average(self, point, dots):
        x = point[0]
        y = point[1]
        average_x = self.fade(x)
        linear_one = dots[0]+average_x*(dots[1]-dots[0])
        linear_two = dots[2]+average_x*(dots[3]-dots[2])
        average_y = self.fade(y)
        linear_final = linear_one+average_y*(linear_two-linear_one)
        return linear_final

    def dot_product(self, a, b):
        influence = (a[0]*b[0])+(a[1]*b[1])
        return influence

    def fade(self, value):
        return (6*value**2-15*value+10)*value**3

    def return_noise(self):
        return self.noise


size = 400
x = PerlinNoise(size)
data = x.return_noise()
image = Image.new("L", (size,size))
image.putdata(data, 128, 128)
image.save("Magic.png")
