def probability_finder(number_range, modifier, target_number):
    counter = 0
    for die in range(1, number_range[0]+1):
        for second_die in range(1, number_range[1]+1):
            if die+second_die+modifier == target_number:
                counter += 1
            
    return (counter/(number_range[0]*number_range[1]))

number_range = [100, 20]
modifier = 0
target_number = range(1, sum(number_range)+1)

dice_probability = [probability_finder([100, 20],0, target_number) for target_number in range(1, 121+modifier)]
dice_probability = list(filter(lambda x: x != 0, dice_probability))
print(dice_probability)
