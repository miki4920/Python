from PIL import Image
import random
from itertools import product


class PerlinNoise(object):
    def __init__(self, side_size):
        self.length = side_size**2
        self.gradients = {}
        self.values = self.values = list(product([i/side_size for i in range(0, side_size)], repeat=2))
        self.noise = [0] * self.length
        # Generate gradient within the noise
        self.generate_gradient()
        self.generate_noise()

    def generate_gradient(self):
        for i in list(product([0, 1], repeat=2)):
            vectors = [random.gauss(0, 1) for _ in range(2)]
            modulus = (vectors[0] ** 2 + vectors[1] ** 2) ** (-0.5)
            self.gradients[i] = [vectors[0] * modulus, vectors[1] * modulus]

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

    @staticmethod
    def dot_product(a, b):
        influence = (a[0]*b[0])+(a[1]*b[1])
        return influence

    @staticmethod
    def fade(value):
        return (6*value**2-15*value+10)*value**3

    def return_noise(self):
        return self.noise



def color_map(data):
    a = min(data)
    b = max(data)
    x = b-a
    for i in range(0, len(data)):
        if data[i] > b-(x*0.1):
            data[i] = (134, 126, 112)
        elif data[i] > b-(x*0.2):
            data[i] = (151,124,83)
        elif data[i] < b-(x*0.8):
            data[i] = (0, 0, 89)
        elif data[i] < b-(x*0.7):
            data[i] = (144,152,204)
        elif data[i] < b-(x*0.65):
            data[i] = (253,223,119)
        elif data[i] < b-(x*0.3):
            data[i] = (124,252,0)
        else:
            data[i] = (222,165,33)
    return data


size = 4096
a = []
x = PerlinNoise(size)
data = x.return_noise()
data = color_map(data)
image = Image.new("RGB", (size,size))
image.putdata(data, 128, 128)
image.save("Magic.png")
