from enum import Enum, auto


class GameStates(Enum):
    PLAYER_TURN = auto()
    ENEMY_TURN = auto()
    PLAYER_DEAD = auto()
    LOOK_ENEMY = auto()
    SHOW_INVENTORY = auto()
    DROP_INVENTORY = auto()
    TARGETING = auto()


class MenuState:
    menu_state = 0
