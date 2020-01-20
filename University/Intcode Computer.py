class Computer(object):
    def __init__(self):
        self.pc = 0
        self.ir = ""
        self.instructions = []

    def run(self):
        while True:
            self.ir = self.instructions[self.pc]
            self.ir = self.sign_extend(self.ir, 5)
            opcode = self.ir[3:]
            if opcode == "99":
                break
            elif opcode == "01":
                self.add()
                self.pc += 4
            elif opcode == "02":
                self.multiply()
                self.pc += 4
            elif opcode == "03":
                self.receive_input()
                self.pc += 2
            elif opcode == "04":
                self.output()
                self.pc += 2

    def add(self):
        values = self.fetch_values(self.ir[0:2])
        self.instructions[self.instructions[2]] = str(sum(list(map(int, values))))

    def multiply(self):
        values = self.fetch_values(self.ir[0:2])
        output = 1
        for i in values:
            output *= int(i)
        self.instructions[self.instructions[2]] = str(output)

    def receive_input(self):
        self.instructions[self.pc+1] = input("Instruction:")

    def output(self):
        values = self.fetch_values([3])
        print(self.instructions[values[0]])

    def fetch_values(self, mode):
        values = []
        for i in range(1, len(mode)+1):
            if mode[i-1] == "0":
                values.append(int(self.instructions[int(self.instructions[self.pc+i])]))
            elif mode[i-1] == "1":
                values.append(int(self.instructions[self.pc+i]))
        values = list(map(int, values))
        return values

    def read_instructions(self, filename):
        with open(filename, "r") as f:
            self.instructions = f.read().split(",")

    def sign_extend(self, instruction, length):
        if len(instruction) < length:
            return "0"*(5-len(instruction)) + instruction



computer = Computer()
computer.read_instructions("input.txt")
computer.run()