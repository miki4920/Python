import turtle
import math
import time
screen = turtle.Screen()
screen.bgcolor("white")
Jonathan = turtle.Turtle()
Jonathan.color("black")
Jonathan.speed(0)

def x_coordinate(a, delta):
    coordinate_list = []
    for i in range(0, 1000000):
        coordinate = 200*math.sin(a*i*0.01 + delta*0.01)
        coordinate_list.append(coordinate)
    return coordinate_list

def y_coordinate(b):
    coordinate_list = []
    for i in range(0, 1000000):
        coordinate = 200*math.sin(i*b*0.01)
        coordinate_list.append(coordinate)
    return coordinate_list

a = 56
b = 55
delta = math.pi/4
x = x_coordinate(a, delta)
y = y_coordinate(b)
for i in range(0, 1000000):
    Jonathan.goto(x[i], y[i])
time.sleep(100)
