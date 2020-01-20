
def handle_keys(key):
    if key.sym == 1073741920:    # 8 on NUM
        # Moves one tile up
        return {'move': (0, -1)}
    elif key.sym == 1073741914:  # 2 on NUM
        # Moves one tile down
        return {'move': (0, 1)}
    elif key.sym == 1073741916:  # 4 on NUM
        # Moves one tile to the left
        return {'move': (-1, 0)}
    elif key.sym == 1073741918:  # 6 on NUM
        # Moves one tile to the right
        return {'move': (1, 0)}
    elif key.sym == 1073741919:  # 7 on NUM
        # Moves one tile up and one left
        return {'move': (-1, -1)}
    elif key.sym == 1073741921:  # 9 on NUM
        # Moves one tile up and one right
        return {'move': (1, -1)}
    elif key.sym == 1073741913:  # 1 on NUM
        # Moves one tile down and one left
        return {'move': (-1, 1)}
    elif key.sym == 1073741915:  # 3 on NUM
        # Moves one tile down and one right
        return {'move': (1, 1)}

    if key.sym == 1073741892:    # F11 Key
        # Sets full screen
        return {'fullscreen': True}
    elif key.sym == 27:          # Escape Key
        # Exit the game
        return {'leave': True}
    return {}
