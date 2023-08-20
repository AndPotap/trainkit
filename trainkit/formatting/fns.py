import os


def format_directory(dir):
    python_files = list_python_files(dir)
    for file in python_files:
        print(f"Going over {file}")
        pass_formatting(file)
        print("Sucessful")


def pass_formatting(file_path):
    os.system(f"python3 -m yapf -i {file_path}")
    os.system(f"python3 -m autopep8 -i {file_path}")
    os.system(f"python3 -m yapf -i {file_path}")


def list_python_files(dir):
    python_files = []
    for root, _, files in os.walk(dir):
        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))
    return python_files
