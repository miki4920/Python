from utility_functions.file_handler import write_json, read_json
from components.ai import *
from utility_functions.random_generator import NumberGenerator

monster_path = "\data\monsters\\"


def __get_description(description_names):
    description = {}
    for word in description_names:
        description[word] = input(word + ": ")
    return description["Name"], description


def __get_attributes(attribute_names):
    attributes = {}
    for word in attribute_names:
        attributes[word] = input(word + ": ")
    return attributes["CR"], attributes


def __get_statistics(statistic_names):
    statistics = {}
    for word in statistic_names:
        statistics[word] = input(word + ": ")
    return statistics


def __get_properties(property_names):
    properties = {}
    for word in property_names:
        properties[word] = input(word + ": ")
    return properties


def __get_actions(action_names):
    number = int(input("Actions: "))
    actions = {}
    for i in range(0, number):
        action = {}
        for word in action_names:
            action[word] = input(word + ": ")
        actions[i] = action
    return actions


def __add_monster_to_dictionary(name, cr):
    path = "\data\monsters\monster_dict.json"
    if not read_json(path):
        write_json(path, {})
    monster_dictionary = read_json(path)
    same_cr_monsters = monster_dictionary.get(cr)
    if same_cr_monsters:
        if name not in same_cr_monsters:
            same_cr_monsters.append(name)
            monster_dictionary[cr] = same_cr_monsters
            write_json(path, monster_dictionary)
    else:
        monster_dictionary[cr] = [name]
        write_json(path, monster_dictionary)


def create_monster():
    name, description = __get_description(["Name", "Size", "Type", "Alignment"])
    cr, attributes = __get_attributes(["HP", "AC", "CR", "Speed"])
    statistics = __get_statistics(["STR", "DEX", "CON", "INT", "WIS", "CHA"])
    properties = __get_properties(["AI"])
    actions = __get_actions(["Name", "Damage", "Range"])
    monster = {"Description": description, "Attributes": attributes, "Statistics": statistics, "Properties": properties,
               "Actions": actions}
    write_json(monster_path + name + ".json", monster)
    __add_monster_to_dictionary(name, cr)


def round_to_nearest(cr):
    monster_cr = read_json("\data\monster_cr.json").get("Monster_CR")
    for i in range(0, len(monster_cr) - 1):
        if monster_cr[i] <= cr < monster_cr[i + 1]:
            return str(monster_cr[i])
    else:
        return str(monster_cr[0])


def get_monster_by_name(name):
    monster = read_json(monster_path + name + ".json")
    return monster


def get_monster_by_cr(cr):
    difficulty = round_to_nearest(cr)
    monster_dictionary = read_json("\data\monsters\monster_dict.json")
    monster = monster_dictionary.get(str(difficulty))
    monster = NumberGenerator.random_element(monster)
    return monster


def get_monster_ai(name):
    monster = get_monster_by_name(name)
    ai = monster.get("Properties").get("AI")
    if ai == "Basic":
        return BasicMonster()
    elif ai == "Skirmish":
        return SkirmishMonster()
    elif ai == "None":
        return None
    elif ai == "Charger":
        return ChargerMonster()
    else:
        print(f"The monster {name} does not have an AI defined, going back to basic")
        return BasicMonster


def get_monster_arrangement(difficulty):
    choice = NumberGenerator.random_integer(1, 2)
    monsters = []
    if choice == 1:
        monsters = [get_monster_by_cr(difficulty)]
    elif choice == 2:
        nearest_cr = float(round_to_nearest(difficulty / 4))
        number_of_monsters = difficulty / nearest_cr
        if number_of_monsters > 8:
            number_of_monsters = 8
        for i in range(0, NumberGenerator().random_integer(1, number_of_monsters)):
            monster = get_monster_by_cr(nearest_cr)
            monsters.append(monster)
    return monsters


def get_monster_hit_chance(name):
    monster = get_monster_by_name(name)
    cr = monster.get("Attributes").get("CR")
    hit_chances = read_json("\data\monster_hit_chance.json").get("Proficiency")
    return int(hit_chances[cr])


def get_monster_xp(difficulty):
    xp_table = read_json("\data\monster_xp.json").get("XP")
    xp = xp_table.get(difficulty)
    return int(xp)


if __name__ == "__main__":
    create_monster()
