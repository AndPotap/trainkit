from pathlib import Path
import re


def move_files(file_list, root, target_dir):
    for file in file_list:
        file = root / Path(file)
        target_path = target_dir / file.name
        file.rename(target_path)
        print(f"Moved: {file} -> \n       {target_path}")


def get_all_files(dir):
    dir = Path(dir)
    all_files = [str(file.relative_to(dir)) for file in dir.rglob("*") if file.is_file()]
    return all_files


def extract_graph_filepaths(lines):
    filepaths = []
    for line in lines:
        if line.find("includegraphics") >= 0:
            out = get_filepath(line)
            filepaths.append(out)
    return filepaths


def get_filepath(latex_command):
    pattern = r"\\includegraphics\[[^\]]*\]\{([^\}]*)\}"
    match = re.search(pattern, latex_command)
    assert match is not None, f"could not find match on {latex_command}"
    return match.group(1)
