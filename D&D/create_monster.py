def cls():
    print("\n" * 100)
    print("Renewing the process")


def get_monster_name():
    while True:
        name = input("Please Insert Monster's name: ")
        print(f"The name you inserted: {name}. Is it correct?")
        answer = input().lower()
        if "y" in answer:
            break
        else:
            cls()
    return name


def get_attribute(attribute_name):
    number = input(f"Please Insert Monster's {attribute_name}: ")
    print(f"The {attribute_name} you inserted: {number}.")
    return number


def get_attributes(required_stats):
    attributes = {}
    for stat in required_stats:
        attributes[f"{stat}"] = get_attribute(f"{stat}")
    return attributes


def action_maker():
    action = {}
    action_attributes = ["HIT", "DAMAGE"]
    for attribute in action_attributes:
        action[f"{attribute}"] = get_attribute(f"{attribute}")
    return action


def create_monster():
    name = get_monster_name()
    attributes = get_attributes(["HP", "AC", "Speed"])
    statistics = get_attributes(["STR", "DEX", "CON", "INT", "WIS", "CHA"])
    actions = {}
    for i in range(0, int(input("How many actions does the monster have? "))):
        actions[str(i)] = action_maker()
    monster = {"name": name, "attributes": attributes, "statistics": statistics, "actions": actions}
    print(monster)


if __name__ == "__main__":
    create_monster()
