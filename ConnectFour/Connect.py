def who_is_winner(pieces_position_list):
    grid = []
    for i in range(0, 7):
        grid.append([])
    for i in pieces_position_list:
        if i[2] == "Y":
            grid[ord(i[0]) - 65].append(0)
        else:
            grid[ord(i[0]) - 65].append(1)
        x = check_winner(grid)
        if x == 0:
            return "Yellow"
        elif x == 1:
            return "Red"
    return "Draw"


def check_winner(grid):
    current = 0
    for i in grid:
        counter = 0
        for color in i:
            if color == current:
                counter += 1
                if counter == 4:
                    return current
            else:
                counter = 1
                if current == 0:
                    current = 1
                else:
                    current = 0
    for i in range(0, 4):
        for j in range(0, 3):
            counter = 0
            for k in range(0, 4):
                if len(grid[i + k]) <= j + k:
                    counter = 0
                    break
                else:
                    if grid[i + k][j + k] == current:
                        counter += 1
                        if counter == 4:
                            return current
                    else:
                        counter = 1
                        if current == 0:
                            current = 1
                        else:
                            current = 0
    for index in range(0, 6):
        counter = 0
        for column in grid:
            if len(column) - 1 < index:
                counter = 0
            else:
                if column[index] == current:
                    counter += 1
                    if counter == 4:
                        return current
                else:
                    counter = 1
                    if current == 0:
                        current = 1
                    else:
                        current = 0
    for i in range(3, 7):
        for j in range(0, 3):
            counter = 0
            for k in range(0, 4):
                if len(grid[i - k]) <= j + k:
                    counter = 0
                    break
                else:
                    if grid[i - k][j + k] == current:
                        counter += 1
                        if counter == 4:
                            return current
                    else:
                        counter = 1
                        if current == 0:
                            current = 1
                        else:
                            current = 0
