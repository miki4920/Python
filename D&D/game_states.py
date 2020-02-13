from enum import Enum


class GameStates(Enum):
    PLAYER_TURN = 1
    ENEMY_TURN = 2
    PLAYER_DEAD = 3
    LOOK_ENEMY = 4
    SHOW_INVENTORY = 5
    DROP_INVENTORY = 6
    TARGETING = 7


class MenuState:
    menu_state = 0
