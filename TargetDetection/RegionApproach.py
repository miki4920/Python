import turtle
from random import randint


class TargetDetection(object):
    def __init__(self):
        self.xa = randint(10, 30) * 5 - 200
        self.ya = randint(10, 30) * 5 - 150
        self.xb = self.xa - randint(5, 30) * 7
        self.yb = self.ya + randint(5, 30) * 7
        self.xc = self.xa + randint(5, 30) * 7
        self.yc = self.ya + randint(5, 30) * 7
        self.gradient_ab = 0
        self.gradient_bc = 0
        self.gradient_ac = 0

        self.intercept_ab = 0
        self.intercept_bc = 0
        self.intercept_ac = 0
        self.Ryan = turtle.Turtle()
        self.screen = turtle.Screen()
        canvas = self.screen.getcanvas()
        canvas.bind('<Motion>', self.check_position)
        self.calculate_lines()
        self.draw_triangle()

    def draw_triangle(self):
        self.Ryan.penup()
        self.Ryan.goto(self.xa, self.ya)
        self.Ryan.pendown()
        self.Ryan.goto(self.xb, self.yb)
        self.Ryan.goto(self.xc, self.yc)
        self.Ryan.goto(self.xa, self.ya)
        self.screen.exitonclick()

    def calculate_lines(self):
        self.gradient_ab = (self.yb-self.ya)/(self.xb-self.xa)
        self.gradient_bc = (self.yc-self.yb)/(self.xc-self.xb)
        self.gradient_ac = (self.yc-self.ya)/(self.xc-self.xa)
        self.intercept_ab = self.yb-self.gradient_ab*self.xb
        self.intercept_bc = self.yc-self.gradient_bc*self.xc
        self.intercept_ac = self.yc-self.gradient_ac*self.xc

    def check_position(self, event):
        x, y = event.x-345, 290-event.y
        if self.xb <= x <= self.xa:
            if (round(self.gradient_ab*x+self.intercept_ab)) <= y <= round(self.gradient_bc*x+self.intercept_bc):
                print("In range")
            else:
                print("Not in range")
        elif self.xa <= x <= self.xc:
            if self.gradient_ac * x + self.intercept_ac <= y <= self.gradient_bc * x + self.intercept_bc:
                print("In range")
            else:
                print("Not in range")

    def do_nothing(self):
        pass


app = TargetDetection()
