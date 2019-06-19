import turtle
from random import randint
from time import sleep

grid = []
grid.append([3, 0, 6, 5, 0, 8, 4, 0, 0])
grid.append([5, 2, 0, 0, 0, 0, 0, 0, 0])
grid.append([0, 8, 7, 0, 0, 0, 0, 3, 1])
grid.append([0, 0, 3, 0, 1, 0, 0, 8, 0])
grid.append([9, 0, 0, 8, 6, 3, 0, 0, 5])
grid.append([0, 5, 0, 0, 9, 0, 6, 0, 0])
grid.append([1, 3, 0, 0, 0, 0, 2, 5, 0])
grid.append([0, 0, 0, 0, 0, 0, 0, 7, 4])
grid.append([0, 0, 5, 2, 0, 6, 3, 0, 0])

myPen = turtle.Turtle()
myPen.speed(0)
myPen.color("#000000")
myPen.hideturtle()
topLeft_x=-150
topLeft_y=150


def text(message,x,y,size):
    FONT = ('Arial', size, 'normal')
    myPen.penup()
    myPen.goto(x,y)
    myPen.write(message,align="left",font=FONT)


def drawGrid(grid):
  intDim=35
  for row in range(0,10):
    if (row%3)==0:
      myPen.pensize(3)
    else:
      myPen.pensize(1)
    myPen.penup()
    myPen.goto(topLeft_x,topLeft_y-row*intDim)
    myPen.pendown()
    myPen.goto(topLeft_x+9*intDim,topLeft_y-row*intDim)
  for col in range(0,10):
    if (col%3)==0:
      myPen.pensize(3)
    else:
      myPen.pensize(1)
    myPen.penup()
    myPen.goto(topLeft_x+col*intDim,topLeft_y)
    myPen.pendown()
    myPen.goto(topLeft_x+col*intDim,topLeft_y-9*intDim)

  for row in range (0,9):
      for col in range (0,9):
        if grid[row][col]!=0:
          text(grid[row][col],topLeft_x+col*intDim+9,topLeft_y-row*intDim-intDim+8,18)
drawGrid(grid)