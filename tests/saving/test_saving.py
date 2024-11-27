from trainkit.saving.saving import find_latest


def test_find_latest(tmp_path):
    filenames = [
        "backup_2024-11-26_143055.log",
        "backup_2024-11-25_120102.log",
        "backup_2024-11-27_090900.log",
        "run.txt",
        "run_2024-11-28_130012.txt",
    ]
    for filename in filenames:
        (tmp_path / filename).touch()

    last_file = find_latest(tmp_path, prefix="backup")
    ans = str(tmp_path / "backup_2024-11-27_090900.log")
    assert last_file == ans

    last_file = find_latest(tmp_path, prefix="")
    ans = str(tmp_path / "run_2024-11-28_130012.txt")
    assert last_file == ans
