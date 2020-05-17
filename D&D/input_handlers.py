import tcod
import tcod.event

from game_states import GameStates, MenuState


def handle_player_turn_keys(key):
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
    elif key.sym == 1073741913:  # 1 on NUM q
        # Moves one tile down and one left
        return {'move': (-1, 1)}
    elif key.sym == 1073741915:  # 3 on NUM
        # Moves one tile down and one right
        return {'move': (1, 1)}
    elif key.sym == 1073741909:
        # Sets a enemy checkup
        return {'look_enemy': True}
    elif key.sym == 1073741912:  # Enter on Numpad
        return {'pickup': True}
    elif key.sym == 1073741923:  # . on Numpad
        return {'show_inventory': True}
    elif key.sym == 1073741922:  # 0 on Numpad
        return {'drop_inventory': True}
    elif key.sym == 1073741910:
        return {'take_stairs': True}
    elif key.sym == 1073741892:  # F11 Key
        # Sets full screen
        return {'fullscreen': True}
    elif key.sym == 27:  # Escape Key
        # Exit the game
        return {'leave': True}
    elif key.sym == 1073741908:  # / on Numpad
        return {'show_character_screen': True}
    return {}


def handle_player_dead_keys(key):
    if key.sym == 1073741923:
        return {'show_inventory': True}
    elif key.sym == 1073741909:
        # Sets a enemy checkup
        return {'look_enemy': True}
    elif key.sym == 1073741892:  # F11 Key
        # Sets full screen
        return {'fullscreen': True}
    elif key.sym == 27:  # Escape Key
        # Exit the game
        return {'leave': True}
    return {}


def handle_inventory_keys(key):
    index = MenuState.menu_state
    if key.sym == 1073741920:  # 8 on NUM
        # Increments index
        index -= 1
    elif key.sym == 1073741914:  # 2 on NUM
        # Decrements index
        index += 1
    elif key.sym == 1073741912:
        return {'inventory_index': MenuState.menu_state}
    elif key.sym == 1073741892:  # F11 Key
        # Sets full screen
        return {'fullscreen': True}
    elif key.sym == 1073741923:  # Escape Key
        # Exit the game
        return {'leave': True}
    elif key.sym == 1073741923:  # . on Numpad
        return {'leave': True}
    MenuState.menu_state = index
    return {}


def handle_looking_keys(key):
    if key.sym == 27:
        return {'leave': True}
    elif key.sym == 1073741909:
        return {'look_enemy': True}
    return {}


def handle_targeting_keys(key):
    if key.sym == 27:
        return {'leave': True}
    return {}


def handle_character_screen(key):
    if key.sym == 1073741908:  # / on Numpad
        return {'leave': True}
    return {}


def handle_main_menu(key):
    if key.sym == 1073741912:
        return {'new_game': True}
    elif key.sym == 1073741922:
        return {'load_game': True}
    elif key.sym == 27:
        return {'exit': True}

    return {}


def handle_keys(key, game_state):
    if game_state == GameStates.PLAYER_TURN:
        return handle_player_turn_keys(key)
    elif game_state == GameStates.PLAYER_DEAD:
        return handle_player_dead_keys(key)
    elif game_state == GameStates.LOOK_ENEMY:
        return handle_looking_keys(key)
    elif game_state == GameStates.TARGETING:
        return handle_targeting_keys(key)
    elif game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        return handle_inventory_keys(key)
    elif game_state == GameStates.CHARACTER_SCREEN:
        return handle_character_screen(key)
    return {}


def handle_mouse(mouse):
    x, y = mouse.tile
    if mouse.button == tcod.event.BUTTON_LEFT:
        return {'left_click': (x, y)}
    elif mouse.button == tcod.event.BUTTON_RIGHT:
        return {'right_click': (x, y)}
    return {}
