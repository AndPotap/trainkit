from trainkit.saving.saving import sort_files


def test_sort_files(tmp_path):
    filenames = [
        "backup_2024-11-26_143055.log",
        "backup_2024-11-25_120102.log",
        "backup_2024-11-27_090900",
        "run.txt",
        "run_2024-11-28_130012.txt",
    ]
    for filename in filenames:
        (tmp_path / filename).touch()

    last_file = str(sort_files(tmp_path, prefix="backup")[0])
    ans = str(tmp_path / "backup_2024-11-27_090900")
    assert last_file == ans

    last_file = str(sort_files(tmp_path, prefix="")[0])
    ans = str(tmp_path / "run_2024-11-28_130012.txt")
    assert last_file == ans

    last_file = sort_files(tmp_path, prefix="backup")[0].name
    ans = "backup_2024-11-27_090900"
    assert last_file == ans
