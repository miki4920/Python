import math
from functools import reduce


def first_task(mass):
    fuel = math.floor(int(mass)/3)-2
    count = fuel
    while count > 0:
        count = math.floor(int(count)/3)-2
        if count > 0:
            fuel += count
    if fuel < 0:
        return 0
    else:
        return fuel


def second_task(instruction, noun, verb):
    index = 0
    instruction[1] = noun
    instruction[2] = verb
    while True:
        i = instruction[index]
        if i == 1:
            instruction[instruction[index + 3]] = instruction[instruction[index+1]] + instruction[
                instruction[index + 2]]
        elif i == 2:
            instruction[instruction[index + 3]] = instruction[instruction[index + 1]] * instruction[
                instruction[index + 2]]
        elif i == 99:
            break
        index += 4
    return instruction


def third_task(wires):
    dictionary = {}
    intersections = []
    for wire in range(0, len(wires)):
        x = 0
        y = 0
        wires[wire] = wires[wire].split(",")
        for segment in wires[wire]:
            for i in range(0, int(segment[1:])):
                if segment[0] == "R":
                    x += 1
                elif segment[0] == "L":
                    x -= 1
                elif segment[0] == "U":
                    y += 1
                elif segment[0] == "D":
                    y -= 1
                if (x, y) in dictionary:
                    if dictionary[(x, y)] != wire:
                        intersections.append([x, y])
                else:
                    dictionary[(x, y)] = wire
    return intersections


def third_task_expanded(wires, intersections):
    dictionary = {}
    steps_list = [[1, 1] for i in range(0, len(intersections))]
    for wire in range(0, len(wires)):
        x = 0
        y = 0
        steps = 0
        wires[wire] = wires[wire].split(",")
        for segment in wires[wire]:
            for i in range(0, int(segment[1:])):
                if segment[0] == "R":
                    x += 1
                elif segment[0] == "L":
                    x -= 1
                elif segment[0] == "U":
                    y += 1
                elif segment[0] == "D":
                    y -= 1
                steps += 1
                if [x, y] in intersections:
                    steps_list[intersections.index([x,y])][wire] = steps
                else:
                    dictionary[(x, y)] = wire
    return min(reduce(lambda a, b:a+b, sequence) for sequence in steps_list)


def fourth_task(task_range):
    integers = [str(i) for i in range(task_range[0], task_range[1])]
    final = []
    for integer in integers:
        correct = True
        check = False
        if (integer[0] == integer[1] and integer[1] != integer[2]) or (integer[len(integer)-1] == integer[len(integer)-2] and integer[len(integer)-2] != integer[len(integer)-3]):
            check = True
        for index in range(0, len(integer)-1):
            if int(integer[index]) > int(integer[index+1]):
                correct = False
                break
        for index in range(1, len(integer)-2):
            if integer[index] == integer[index+1] and integer[index+1] != integer[index+2] and integer[index] != integer[index-1]:
                check = True
        if correct and check:
            final.append(integer)
    return len(final)


class FifthTask(object):
    def __init__(self, instruction):
        self.instruction = instruction
        self.current_index = 0
        self.current_instruction = instruction[self.current_index][::-1]
        self.register = []
        self.run_computer()

    def run_computer(self):
        while True:
            if "99" == self.current_instruction[0:2]:
                break
            self.register = []
            [self.register.append(i) for i in self.current_instruction]
            if len(self.register) > 1:
                del self.register[1]
            if len(self.register) < 4:
                self.register += ["0" for i in range(0, 4-len(self.register))]
            if self.register[0] == "1":
                self.add()
                index_jump = 4
            elif self.register[0] == "2":
                self.multiply()
                index_jump = 4
            elif self.register[0] == "3":
                self.instruction[int(self.instruction[self.current_index+1])] = input("Please insert a value: ")
                index_jump = 2
            elif self.register[0] == "4":
                index_jump = 2
                print(self.current_index)
                print(self.instruction[int(self.instruction[self.current_index+1])])
            self.current_index += index_jump
            self.current_instruction = self.instruction[self.current_index][::-1]

    def add(self):
        values = self.get_values()
        self.instruction[int(self.instruction[self.current_index+3])] = str(sum(values))

    def multiply(self):
        output = 1
        values = self.get_values()
        for i in values:
            output *= i
        self.instruction[int(self.instruction[self.current_index + 3])] = str(output)

    def get_values(self):
        values = []
        for i in range(1, 3):
            if self.register[i] == "0":
                values.append(int(self.instruction[int(self.instruction[self.current_index + i])]))
            else:
                values.append(int(self.instruction[self.current_index + i]))
        return values


with open("input.txt", "r") as f:
    data = f.read().split(",")
    task = FifthTask(data.copy())


