import turtle
loadWindow = turtle.Screen()
Richard = turtle.Turtle()
Richard.speed(0)
Richard.penup()
Richard.color("black")
Richard.pensize(3)
black_tiles = []
current_x = 0
current_y = 0
rotation = 0
scale = 10
while True:
    point = [current_x, current_y]
    Richard.goto(point[0], point[1])
    Richard.dot()
    if point in black_tiles:
        Richard.color("white")
        black_tiles.remove(point)
        if rotation-90 >= 0:
            rotation = rotation-90
        else:
            rotation = 270
    else:
        Richard.color("black")
        black_tiles.append(point)
        if rotation+90 < 360:
            rotation = rotation+90
        else:
            rotation = 0
    if rotation == 0:
        current_x += scale
    elif rotation == 90:
        current_y += scale
    elif rotation == 180:
        current_x -= scale
    elif rotation == 270:
        current_y -= scale
