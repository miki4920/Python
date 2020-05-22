import turtle
import math
screen = turtle.Screen()
screen.bgcolor("white")
Jonathan = turtle.Turtle()
Jonathan.color("black")
Jonathan.speed(0)


def x_coordinate(a, delta, steps, step_size):
    coordinate_list = []
    for step in range(0, steps):
        coordinate = 250*math.sin(step_size*(a*step + delta))
        coordinate_list.append(coordinate)
    return coordinate_list


def y_coordinate(b, steps, step_size):
    coordinate_list = []
    for step in range(0, steps):
        coordinate = 250*math.sin(step*b*step_size)
        coordinate_list.append(coordinate)
    return coordinate_list


steps = 10000
step_size = 0.01
a = 18
b = 17
delta = math.pi/6
x = x_coordinate(a, delta, steps, step_size)
y = y_coordinate(b, steps, step_size)
for i in range(0, steps):
    Jonathan.goto(x[i], y[i])

