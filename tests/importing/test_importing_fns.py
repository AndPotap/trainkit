from trainkit.importing.importing_fns import importer


def test_importer():
    filepath = "./trainkit/importing/fns_for_test.py"
    approx = importer(filepath)
    with open("./tests/importing/init_test_file.py", mode="r") as f:
        soln = f.read()
    assert soln == approx
