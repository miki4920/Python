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
        coordinate = 200*math.sin(step_size*(a*step + delta))
        coordinate_list.append(coordinate)
    return coordinate_list


def y_coordinate(b, steps, step_size):
    coordinate_list = []
    for step in range(0, steps):
        coordinate = 200*math.sin(step*b*step_size)
        coordinate_list.append(coordinate)
    return coordinate_list


steps = 1000000
step_size = 0.001
a = 56
b = 55
delta = math.pi/4
x = x_coordinate(a, delta, steps, step_size)
y = y_coordinate(b, steps, step_size)
for i in range(0, 1000000):
    Jonathan.goto(x[i], y[i])

