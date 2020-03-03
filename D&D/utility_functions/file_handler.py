import json
import os, os.path
import errno
from pathlib import Path


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def safe_open_w(path):
    mkdir_p(os.path.dirname(path))
    return open(path, 'w')


def write_json(path, content):
    with safe_open_w(path) as file:
        json.dump(content, file, indent=4, sort_keys=True)


def read_json(path):
    try:
        with open(path, "r") as file:
            content = json.load(file)
        return content
    except FileNotFoundError:
        print(f"File at the path {path} was not found")
        quit()


def get_main_path():
    path = Path(__file__).parent
    while os.path.basename(os.path.normpath(path)) != "D&D":
        path = path.parent
    return str(path)


if __name__ == "__main__":
    file_path = f"{get_main_path()}\\data\\monster_cr.json"
    print(file_path)
    file_content = {
        "Monster_CR": [0.125, 0.25, 0.5, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22,
                       23, 24, 25, 26, 27, 28, 29, 30]}
    write_json(file_path, file_content)
