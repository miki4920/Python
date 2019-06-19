import turtle
from random import randint


class TargetDetection(object):
    def __init__(self):
        self.line_list = []
        self.point_list = []
        self.counter = 0

        self.Tony = turtle.Turtle()
        self.Tony.speed(0)

        self.screen = turtle.Screen()
        self.screen.setworldcoordinates(0, 0, 400, 400)
        self.point = [randint(0, 400), randint(0, 400)]
        self.line = Line([0, 0], self.point)
        self.generate_lines()
        self.draw_lines()
        self.ray_counter()
        self.screen.exitonclick()

    def generate_lines(self):
        change = True
        number_of_lines = randint(3, 10)
        point_one = [randint(10, 390), randint(10, 390)]
        point_two = 0
        self.point_list.append(point_one)
        for i in range(0, number_of_lines):
            if change:
                point_two = [randint(10, 390), randint(10, 390)]
                self.point_list.append(point_two)
                self.line_list.append(Line(point_one, point_two))
                change = False
            else:
                point_one = [randint(10, 390), randint(10, 390)]
                self.point_list.append(point_one)
                self.line_list.append(Line(point_two, point_one))
                change = True
        if number_of_lines % 2 == 0:
            self.line_list.append(Line(point_two, self.point_list[0]))
            self.point_list.append(self.point_list[0])
        else:
            self.line_list.append(Line(point_one, self.point_list[0]))
            self.point_list.append(self.point_list[0])

    def draw_lines(self):
        self.Tony.color("blue")
        self.Tony.goto(self.point)
        self.Tony.dot(5)
        self.Tony.color("black")
        self.Tony.penup()
        self.Tony.goto(self.point_list[0])
        self.Tony.pendown()
        for point in self.point_list:
            self.Tony.goto(point[0], point[1])

    def ray_counter(self):
        for line in self.line_list:
            if self.line.find_intersection(line):
                self.paint_red(line)
                self.counter += 1
        print(self.counter)
        if self.counter % 2 != 0:
            print("Point inside")
        else:
            print("Point outside")

    def paint_red(self, line):
        self.Tony.color("red")
        self.Tony.penup()
        self.Tony.goto(line.return_points()[0])
        self.Tony.pendown()
        self.Tony.goto(line.return_points()[1])


class Line(object):
    def __init__(self, point_one, point_two):
        self.point_one = point_one
        self.point_two = point_two
        self.gradient = 0
        self.intersect = 0
        self._find_gradient()
        self._find_intersect()

    def _find_gradient(self):
        y_change = self.point_two[1] - self.point_one[1]
        x_change = self.point_two[0]-self.point_one[0]
        self.gradient = y_change/x_change

    def _find_intersect(self):
        self.intersect = (self.point_two[1]-(self.point_two[0]*self.gradient))

    def find_intersection(self, line):
        if line.return_gradient() - self.gradient != 0:
            intersection_point = (line.return_intersect())/(self.gradient - line.return_gradient())
            x_cords = line.return_range_x()
            if x_cords[0] <= intersection_point <= x_cords[1] and self.point_one[0] <= intersection_point <= self.point_two[0]:
                return True
        return False

    def return_gradient(self):
        return self.gradient

    def return_intersect(self):
        return self.intersect

    def return_range_x(self):
        if self.point_one[0] <= self.point_two[0]:
            return self.point_one[0], self.point_two[0]
        return self.point_two[0], self.point_one[0]
    
    def return_points(self):
        return self.point_one, self.point_two



app = TargetDetection()