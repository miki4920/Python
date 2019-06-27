import math
class PerlinNoise(object):
    def __init__(self, seed, number_of_points):
        self.seed = seed.lower()
        self.seed_value = 0
        self.size = number_of_points
        self.x_table = []
        self.x_multiplier = 7
        self.x_modulus = 937
        self.y_table = []
        self.y_multiplier = 9
        self.y_modulus = 773
        self.calculate_seed()
        self.generate_x_values()
        self.generate_y_values()
        self.normalize_values()

    def calculate_seed(self):
        for letter in self.seed:
            self.seed_value += ord(letter)

    def generate_x_values(self):
        number = (self.seed_value*self.x_multiplier + self.x_modulus) % self.seed_value
        if number == 0:
            self.x_table.append(77)
        else:
            if number % 2 == 0:
                self.x_table.append(-number)
            else:
                self.x_table.append(number)
        for i in range(0, self.size-1):
            number = (self.x_table[i] * self.x_multiplier + self.x_modulus) % self.x_modulus
            if number == 0:
                self.x_table.append(77)
            else:
                if number % 2 == 0:
                    self.x_table.append(-number)
                else:
                    self.x_table.append(number)

    def generate_y_values(self):
        number = (self.seed_value * self.y_multiplier + self.y_modulus) % self.seed_value
        if number == 0:
            self.y_table.append(7)
        else:
            if number % 2 == 0:
                self.y_table.append(number)
            else:
                self.y_table.append(-number)
        for i in range(0, self.size - 1):
            number = (self.y_table[i] * self.y_multiplier + self.y_modulus) % self.y_modulus
            if number == 0:
                self.y_table.append(7)
            else:
                if number % 2 == 0:
                    self.y_table.append(number)
                else:
                    self.y_table.append(-number)

    def normalize_values(self):
        for i in range(0, self.size):
            modulus = math.sqrt(self.x_table[i]**2 + self.y_table[i]**2)
            self.x_table[i] = self.x_table[i]/modulus
            self.y_table[i] = self.y_table[i]/modulus



PerlinNoise("banana", 256)