import datetime
from pathlib import Path
import pickle
import re
from random import randint


def append_timestamp(filepath, add_random_suffix=False):
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H%M%S")
    if add_random_suffix:
        timestamp += f"_r{randint(1, 1_000)}"
    filepath = Path(filepath)
    aux = f"{filepath.stem}_{timestamp}{filepath.suffix}"
    new_filepath = filepath.with_name(aux)
    return str(new_filepath)


def ask_save_output():
    out = input("SAVE OUTPUT (Y/N) ")
    save_output = bool(re.match(r"^[Yy]$", out.strip()))
    if save_output:
        print("Decided to save")
    else:
        print("Not saving")
    return save_output


def load_object(filepath):
    with open(file=filepath, mode='rb') as f:
        obj = pickle.load(file=f)
    return obj


def save_object(obj, filepath, use_highest=True):
    protocol = pickle.HIGHEST_PROTOCOL if use_highest else pickle.DEFAULT_PROTOCOL
    with open(file=filepath, mode='wb') as f:
        pickle.dump(obj=obj, file=f, protocol=protocol)
