import turtle


class Maze(object):
    def __init__(self):
        self.grid = []
        self.size = 40
        self.Lois = turtle.Turtle()
        self.Lois.speed(0)
        self.Lois.penup()
        self.screen = turtle.Screen()
        if self.size % 2 == 0:
            self.mean_size = int(self.size/2)
        else:
            self.mean_size = int((self.size+1)/2)
        if not self.size >= 10:
            quit()
        for i in range(0, self.size):
            self.grid.append([0 for x in range(0, self.size)])
        self.create_squares()
        self.draw_maze()

    def create_squares(self):

        for i in range(0, self.mean_size, 2):
            side = [0 for x in range(0, i)]
            middle = [1 for x in range(i, self.size - i)]
            self.grid[i] = side + middle + side
            self.grid[self.size - (i + 1)] = side + middle + side
        for i in range(0, self.mean_size, 2):
            for row in self.grid[i:self.size-i]:
                row[i] = 1
                row[len(row)-(i+1)] = 1

    def draw_maze(self):
        for row in range(0, self.size):
            for column in range(0, self.size):
                if self.grid[row][column] == 1:
                    self.Lois.goto((row-self.mean_size)*10, (column-self.mean_size)*10)
                    self.Lois.dot()
                else:
                    pass
        self.screen.exitonclick()

maze = Maze()