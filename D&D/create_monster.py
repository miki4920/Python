import json
from utility_functions.file_handler import write_json, read_json
from random import choice, randint
def create_monster():
    pass

def round_to_nearest(cr):
    monster_cr = read_json("\data\monster_cr.json")
    for i in range(0, len(monster_cr) - 1):
        if monster_cr[i] <= cr < monster_cr[i + 1]:
            return str(monster_cr[i])
        elif monster_cr[i] == cr:
            return str(monster_cr[i])


if __name__ == "__main__":
    create_monster()
