import json
from pathlib import Path

INDEX_FILE = Path("data/indexed_files.json")


def load_index():

    if not INDEX_FILE.exists():
        return {}

    with open(INDEX_FILE, "r") as f:
        return json.load(f)


def save_index(index):

    INDEX_FILE.parent.mkdir(exist_ok=True)

    with open(INDEX_FILE, "w") as f:
        json.dump(index, f, indent=4)


def is_indexed(filename):

    index = load_index()

    return filename in index


def mark_indexed(filename, pages):

    index = load_index()

    index[filename] = {
        "pages": pages
    }

    save_index(index)