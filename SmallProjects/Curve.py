import turtle
import math


class CurveDrawer(object):
    def __init__(self):
        self.Tortoise = turtle.Turtle()
        self.Tortoise.speed(0)
        self.Screen = turtle.Screen()
        self.R = 3.26
        self.r = 11.43
        self.d = 7.21
        self.steps = 35
        self.scalar = 10
        self.rotations = 10
        self.draw_curve()
        self.Screen.exitonclick()

    def draw_curve(self):
        self.Tortoise.penup()
        for i in range(0, self.steps):
            angle = math.radians(0 + self.rotations*360*i/self.steps)
            x = (self.R - self.r) * math.cos(angle) + self.d * math.cos(angle * (self.R - self.r) / self.r)
            y = (self.R - self.r) * math.sin(angle) - self.d * math.sin(angle * (self.R - self.r) / self.r)
            self.Tortoise.goto(x*self.scalar, y*self.scalar)
            self.Tortoise.pendown()


app = CurveDrawer()
