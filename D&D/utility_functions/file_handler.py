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


def write_json(path, content, sorting=False):
    path = get_main_path() + path
    with safe_open_w(path) as file:
        json.dump(content, file, indent=4, sort_keys=sorting)


def read_json(path):
    path = get_main_path() + path
    try:
        with open(path, "r") as file:
            content = json.load(file)
        return content
    except FileNotFoundError:
        print(f"File at the path {path} was not found")
        return False


def get_main_path():
    path = Path(__file__).parent
    while os.path.basename(os.path.normpath(path)) != "D&D":
        path = path.parent
    return str(path)
