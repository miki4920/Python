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
    while True:
        try:
            number = int(input(f"Please Insert Monster's {attribute_name}: "))
            print(f"The {attribute_name} you inserted: {number}. Is it correct?")
            answer = input().lower()
            if "y" in answer:
                break
            else:
                cls()
        except ValueError:
            cls()
            print("Your number wasn't correct")
    return number


def get_attributes():
    attributes = {"HP": get_attribute("HP"), "AC": get_attribute("AC"), "Speed": get_attribute("Speed")}
    return attributes


def create_monster():
    name = get_monster_name()
    attributes = get_attributes()
    statistics = {}
    actions = {}
    monster = {"name": name, "attributes": attributes, "statistics": statistics, "actions": actions}
    for key in attributes:
        print(f"{key}:{attributes[key]}")


if __name__ == "__main__":
    create_monster()
