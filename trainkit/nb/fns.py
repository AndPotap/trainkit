import os
import nbformat


def extract_code_from_notebook(notebook_path, output_script_path):
    with open(notebook_path, 'r') as nb_file:
        notebook_content = nb_file.read()

    nb = nbformat.reads(notebook_content, as_version=4)
    code_cells = [cell for cell in nb.cells if cell.cell_type == "code"]

    script = ""
    for cell in code_cells:
        cell_script = cell["source"]
        script += cell_script + "\n\n"

    with open(output_script_path, 'w') as script_file:
        script_file.write(script)


if __name__ == "__main__":
    notebook_path = '/home/ubu/cola/docs/notebooks/Quick_Start.ipynb'
    output_script_path = 'output_script.py'

    extract_code_from_notebook(notebook_path, output_script_path)
    # Weirdly I need to run yapf before autopep8
    os.system(f"python3 -m yapf -i {output_script_path}")
    os.system(f"python3 -m autopep8 -i {output_script_path}")
    os.system(f"python3 -m yapf -i {output_script_path}")
