import re


def importer(filepath):
    with open(filepath, mode="r") as f:
        lines = f.readlines()
    prefix = extract_prefix(filepath)
    _all_ = get_fn_or_class_names(lines)
    out = create_import_str(prefix, _all_)
    all_str = create_all_str(_all_)
    return sum_lines(out, all_str, sep="")


def extract_prefix(filepath):
    prefix = filepath.replace("./", "")
    prefix = prefix.replace(".py", "")
    prefix = prefix.replace("/", ".")
    return prefix


def create_all_str(_all_):
    start = "\n__all__ = ["
    end = "]\n"
    out = ""
    for el in _all_:
        out += f'    "{el}",\n'
    final = sum_lines(sum_lines(start, out), end, sep="")
    return final


def sum_lines(line1, line2, sep="\n"):
    return line1 + sep + line2


def create_import_str(prefix, _all_):
    out = ""
    for fn in _all_:
        out += f"from {prefix} import {fn}\n"
    return out


def get_fn_or_class_names(lines):
    pattern_fn = r"^def (\w+)\(*\)"
    pattern_cls = r"^class (\w+)\(\w+\):"
    fns = []
    for line in lines:
        line = line.replace("\n", "")
        name = re.search(pattern_fn, line)
        if name is not None:
            fns.append(name.group(1))
        name = re.search(pattern_cls, line)
        if name is not None:
            fns.append(name.group(1))
    return fns
