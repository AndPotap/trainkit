import json
import pickle
import re
from datetime import datetime
from pathlib import Path
from random import randint

import yaml


def append_timestamp(filepath, add_random_suffix=False):
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H%M%S")
    if add_random_suffix:
        timestamp += f"_r{randint(1, 1_000)}"
    filepath = Path(filepath)
    aux = f"{filepath.stem}_{timestamp}{filepath.suffix}"
    new_filepath = filepath.with_name(aux)
    return str(new_filepath)


def find_latest(root, prefix=""):
    files = [str(f) for f in root.iterdir()]
    if len(prefix) > 0:
        files = [f for f in files if prefix in f]
    fmt = "%Y-%m-%d_%H%M%S"
    pattern = r"\d{4}-\d{2}-\d{2}_\d{6}"

    def extract_timestamp(file):
        match = re.search(pattern, file)
        if match:
            return datetime.strptime(match.group(), fmt)
        return None

    filtered_files = []
    for file in files:
        match = extract_timestamp(file)
        if match is not None:
            filtered_files.append(file)

    sorted_files = sorted(filtered_files, key=lambda x: extract_timestamp(x), reverse=True)
    return sorted_files[0]


def ask_save_output():
    out = input("SAVE OUTPUT (Y/N) ")
    save_output = bool(re.match(r"^[Yy]$", out.strip()))
    if save_output:
        print("Decided to save")
    else:
        print("Not saving")
    return save_output


def load_json(filepath):
    with open(file=filepath, mode="r") as file:
        obj = json.load(file)
    return obj


def save_json(obj, filepath):
    with open(file=filepath, mode="w") as file:
        obj = json.dump(obj, file)
    return obj


def load_yml(filepath):
    with open(file=filepath, mode="r") as file:
        obj = yaml.safe_load(file)
    return obj


def save_yml(obj, filepath):
    with open(file=filepath, mode="w") as file:
        yaml.dump(obj, file)


def load_object(filepath):
    with open(file=filepath, mode="rb") as f:
        obj = pickle.load(file=f)
    return obj


def save_object(obj, filepath, use_highest=True):
    protocol = pickle.HIGHEST_PROTOCOL if use_highest else pickle.DEFAULT_PROTOCOL
    with open(file=filepath, mode="wb") as f:
        pickle.dump(obj=obj, file=f, protocol=protocol)
