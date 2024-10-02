from pathlib import Path

from fns import extract_graph_filepaths, get_all_files, move_files

root = Path("/home/ubu/Downloads/Papers/neurips2024/einsum")
main_tex = "main.tex"
figs_name = "figs/"
backup_path = Path().home() / "Downloads/backup_latex"

for case in [main_tex, figs_name]:
    assert (root / case).exists(), f"{root / case} does not exist"

lines = (root / main_tex).read_text().split("\n")
used_figs = set(extract_graph_filepaths(lines))
all_figs = get_all_files(root / figs_name)
all_figs = set([figs_name + file for file in all_figs])

diff = used_figs.difference(all_figs)
assert len(diff) == 0, f"some figures are not in the correct folder, {diff}"

unused_figs = all_figs.difference(used_figs)
backup_path.mkdir(parents=True, exist_ok=True)
move_files(unused_figs, root=root, target_dir=backup_path)
