import turtle
import random
import math


class ConfettiDrawer(object):
    def __init__(self):
        self.Mark = turtle.Turtle()
        self.Mark.speed(0)
        self.screen = turtle.Screen()
        self.circle_list = []
        self.circle_number = 10000
        self.radius = 25
        self.counter = 0
        self.generate_circles()
        self.screen.exitonclick()

    def check_intersection(self, coordinates):
        intersection = True
        for circle in self.circle_list:
            if math.sqrt((coordinates[0]-circle[0])**2 + (coordinates[1]-circle[1])**2) >= 2*self.radius:
                pass
            else:
                intersection = False
                self.counter += 1
        return intersection

    def generate_circles(self):
        counter = 0
        while counter < self.circle_number:
            if self.counter > self.circle_number*100:
                break
            x = random.randint(self.radius-650, 650-self.radius)
            y = random.randint(self.radius-335, 335-self.radius)
            coordinates = [x, y]
            if self.check_intersection(coordinates):
                counter += 1
                self.circle_list.append(coordinates)
                self.Mark.penup()
                self.Mark.goto(x, y)
                self.Mark.pendown()
                self.Mark.dot(self.radius*2, "#" + "%06x" % random.randint(0, 0xFFFFFF))



app = ConfettiDrawer()
