import json


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
        with open(f"monsters/monster_dict.json", "w") as monster_dict_file:
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


if __name__ == "__main__":
    create_monster()
