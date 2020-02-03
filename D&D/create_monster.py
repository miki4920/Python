import json
import random


def get_attribute(attribute_name):
    number = input(f"Please Insert Monster's {attribute_name}: ")
    return number


def get_attributes(required_stats):
    attributes = {}
    for stat in required_stats:
        attributes[stat] = get_attribute(stat)
    return attributes


def action_maker():
    action = {}
    action_attributes = ["HIT", "DAMAGE"]
    for attribute in action_attributes:
        action[attribute] = get_attribute(attribute)
    return action


def store_monster(monster, name, cr):
    with open(f"monsters/{name}.json", "w") as creature_file:
        json.dump(monster, creature_file, indent=4)
    try:
        with open(f"monsters/monster_dict.json", "r") as monster_dict_file:
            monster_dict = json.load(monster_dict_file)
            if cr in monster_dict:
                monster_dict[cr].append(name)
            else:
                monster_dict[cr] = [name]
        with open("monsters/monster_dict.json", "w") as monster_dict_file:
            json.dump(monster_dict, monster_dict_file, indent=4, sort_keys=True)
    except (FileNotFoundError, json.JSONDecodeError):
        monster_dict = {cr: [name]}
        json.dump(monster_dict, open("monsters/monster_dict.json", "w"), indent=4)
    print("Writing successful")


def create_monster():
    name = get_attribute("name")
    attributes = get_attributes(["HP", "AC", "Speed"])
    statistics = get_attributes(["STR", "DEX", "CON", "INT", "WIS", "CHA"])
    cr = get_attribute("CR")
    actions = {}
    for i in range(0, int(input("How many actions does the monster have? "))):
        actions[str(i)] = action_maker()
    monster = {"attributes": attributes, "statistics": statistics, "actions": actions}
    store_monster(monster, name, cr)


def generate_creatures(cr):
    current_monsters = []
    monster_group_max = 4
    try:
        with open("monsters/monster_dict.json", "r") as file:
            monster_dictionary = json.load(file)
            choice = random.randint(1, 2)
            # Powerful Monster
            if choice == 1:
                current_monsters.append(random.choice(monster_dictionary.get(str(cr))))
            elif choice == 2:
                for i in range(0, monster_group_max):
                    current_monsters.append(
                        random.choice(monster_dictionary.get(round_to_nearest(cr / monster_group_max))))
        return current_monsters
    except (json.JSONDecodeError, FileNotFoundError):
        print("There has been an error with the monster file")
        return []
    except TypeError:
        print("There is no requested cr in the dictionary")
        return []


def get_statistics(monster_name):
    with open(f"monsters/{monster_name}.json", "r") as creature_file:
        monster = json.load(creature_file)
    return monster


def round_to_nearest(cr):
    monster_cr = [0.125, 0.25, 0.5, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22,
                  23, 24, 25, 26, 27, 28, 29, 30]
    for i in range(0, len(monster_cr) - 1):
        if monster_cr[i] <= cr < monster_cr[i + 1]:
            return str(monster_cr[i])
        elif monster_cr[i] == cr:
            return str(monster_cr[i])


if __name__ == "__main__":
    create_monster()
