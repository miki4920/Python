import math
import random
import turtle

def binary_denary(number):
    number = number[::-1]
    counter = 0
    final = 0
    for i in number:
        if i == "1":
            final += 2**counter
        counter += 1
    return final
    
def denary_binary(number):
	length = math.floor(math.log(number,2))
	output = ""
	while number>0:
		if number-(2**length)>=0:
			number-=2**length
			output+="1"
		else:
			output+="0"
		length-=1
	if length!=0:
		return output+("0"*length)
	return output
        
def calculate_superset_length(set_length):
    superset_length = 0
    for i in range(0, set_length+1):
        superset_length += math.factorial(set_length)/((math.factorial(i)*math.factorial(set_length-i)))
    return int(superset_length)

def denary_hexary(number):
    value_list = ["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F"]
    output = ""
    length = math.floor(math.log(number, 16))
    while number>0:
        for i in range(15, -1, -1):
            if number-i*16**length>=0:
                output+=value_list[i]
                number-=i*16**length
                break
            if i == 0:
                output+="0"
        length-=1
    if length!=0:
        return output+("0"*length)
    return output
        
def hexary_denary(number):
    number = number[::-1]
    value_list = ["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F"]
    output=0
    for i in range(0, len(number)):
        output+=16**i*value_list.index(number[i])
    return output

def adding_table_denary(first_number, second_number):
    output = str(first_number+second_number)
    first_number = str(first_number)[::-1]
    second_number = str(second_number)[::-1]
    carry = 0
    carried = False
    first_number = first_number+"0"*(len(output)-len(first_number))
    second_number = second_number+"0"*(len(output)-len(second_number))
    for i in range(0, len(first_number)):
        digit_one = int(first_number[i])
        digit_two = int(second_number[i])
        digit_one+= 1*carried
        carried = False
        if (digit_one+digit_two)//10==1:
            carry+=10**(i+1)
            carried = True
    carry = "0"*(len(output)-len(str(carry))) + str(carry)
    print(first_number[::-1])
    print(second_number[::-1])
    print(carry)
    print(output)

def negate_number(number):
    output = 0
    length = len(number)
    for i in range(0, length):
        if i == 0 and number[i] != "1":
            output-=2**(length-1)
        elif number[i] != "1":
            output+=2**(length-(i+1))
    output+= 1
    output = bin(output & 0xffffffff)[::-1][0:length][::-1]
    return output

def russian_roulette():
        value = 0
        count = 0
        while True:
                user = input("Do you want to give it a try? ")
                if user.lower() == "no":
                    break
                else:
                    value = random.randint(1,6)
                    count += 1
                    if value == 6:
                        break
                    else:
                        print("Well done, you survived")
        print("Dead")
        return f"Your result was {count}, well done"

def check_magical_square(table):
    diagonal_1 = []
    diagonal_2 = []
    check = sum(table[0])
    for i in range(0, len(table)):
        temp_table = []
        for j in range(0,  len(table)):
            temp_table.append(table[j][i])
        if sum(table[i]) != check or sum(temp_table) != check:
            return False
        diagonal_1.append(table[i][i])
        diagonal_2.append(table[-i-1][-i-1])
    if sum(diagonal_1) != check or sum(diagonal_2) != check:
        return False
    return True

def generate_anagrams(word):
    word_list = []
    word = word.lower()
    temp_list = []
    output = []
    for letter in word:
        word_list.append(letter)
    for i in range(0, len(word)-1):
        for letter in word:
            for anagram in word_list:
                temp_list.append(anagram+letter)
                if sorted(anagram+letter) == sorted(word):
                    output.append((anagram+letter).capitalize())
        word_list = temp_list
        temp_list = []
    return output
            
def draw_turtle_house(size):
    screen = turtle.Screen()
    reza = turtle.Turtle()
    reza.speed(0)
    for i in range(0, 3):       
        reza.forward(size)
        reza.right(90)
    reza.forward(size)
    reza.right(45)
    reza.forward(math.sqrt(2*(size/2)**2))
    reza.right(90)
    reza.forward(math.sqrt(2*(size/2)**2))
    reza.right(45)
    reza.forward(size)
    reza.right(90)
    reza.forward((1.2*size)/2)
    for i in range(0, 3):
        reza.right(90)
        reza.forward(size*0.2)
    

draw_turtle_house(100)
    
