import hashlib
import string as dictionary

def floor_checker(floor_string):
    count = 0
    for i in range(0, len(floor_string)):
        if floor_string[i] == "(":
            count+=1
        else:
            count-=1
        if count == -1:
            return i+1

        
def wrapping_paper(dimensions):
    dimensions = list(map(int, dimensions.split("x")))
    values = []
    for i in range(0, len(dimensions)):
        for j in range(0, len(dimensions)):
            if i != j:
                values.append(dimensions[i]*dimensions[j])
    output = min(values) + sum(values)
    return output

def wrapping_bow(dimensions):
    dimensions = list(map(int, dimensions.split("x")))
    volume = dimensions[0]*dimensions[1]*dimensions[2]
    perimeter = 2*min(dimensions)
    dimensions.remove(min(dimensions))
    perimeter += 2*min(dimensions)
    return volume + perimeter
             
def present_delivery(directions):
    visited_houses = []
    visits = 1
    north = 0
    east = 0
    north_robot = 0
    east_robot = 0
    santa = True
    visited_houses.append(str(north) + "," + str(east))
    for direction in directions:
        if direction == ">":
            east+= santa*1
            east_robot+= (not santa)*1
        elif direction == "<":
            east-= santa*1
            east_robot-= (not santa)*1
        elif direction == "^":
            north+=1*santa
            north_robot+=(not santa)*1
        elif direction == "v":
            north-=1*santa
            north_robot-=(not santa)*1
        santa = not santa
        if not (str(north) + "," + str(east) in visited_houses):
            visits += 1
            visited_houses.append(str(north) + "," + str(east))
        if not (str(north_robot) + "," + str(east_robot) in visited_houses):
            visits += 1
            visited_houses.append(str(north_robot) + "," + str(east_robot))
    return visits

def hash_finder(string):
    current = 1
    while True:
        if hashlib.md5(str.encode(string+str(current))).hexdigest()[:6] == "000000":
            return current
        else:
            current+=1

def string_goodness(string):
    double = ['aa', 'bb', 'cc', 'dd', 'ee', 'ff', 'gg', 'hh', 'ii', 'jj', 'kk', 'll', 'mm', 'nn', 'oo', 'pp', 'qq', 'rr', 'ss', 'tt', 'uu', 'vv', 'ww', 'xx', 'yy', 'zz']
    vowels = ["a", "e", "i", "o", "u"]
    naughty_string = ["ab","cd","pq","xy"]
    count = 0
    for i in naughty_string:
        if i in string:
            return False
    for i in string:
        if i in vowels:
            count += 1
    for i in double:
        if i in string and count > 2:
            return True
    return False
            
def string_goodness_second(string):
    pairs = []
    pair_in = False
    triplet = False
    for i in range(0, len(string)-1):
        pairs.append(string[i]+string[i+1])
    for pair in pairs:
        if pair in string.replace(pair,",", 1):
            pair_in = True
            break
    for i in range(0, len(string)-2):
        if string[i] == string[i+2]:
            triplet = True
            break
    if triplet and pair_in:
        return True
    return False

def grid_changer(change, lights):
    change = change.split(" ")
    if change[1] == "on":
        for i in range(int(change[2].split(",")[0]), int(change[4].split(",")[0])+1):
            for j in range(int(change[2].split(",")[1]), int(change[4].split(",")[1])+1):
                lights[i][j]+= 1
    elif change[1] == "off":
        for i in range(int(change[2].split(",")[0]), int(change[4].split(",")[0])+1):
            for j in range(int(change[2].split(",")[1]), int(change[4].split(",")[1])+1):
                if lights[i][j] > 0:
                    lights[i][j]-= 1
    else:
        for i in range(int(change[1].split(",")[0]), int(change[3].split(",")[0])+1):
            for j in range(int(change[1].split(",")[1]), int(change[3].split(",")[1])+1):
                lights[i][j]+=2
    return lights

        
count = 0
lights = [[0]*1000 for i in range(0, 1000)]
with open("input.txt","r") as f:
    x = f.read().split("\n")
    for i in x:
        lights = grid_changer(i, lights)
    for i in lights:
        for j in i:
            count+=j
    print(count)
