import fire

from trainkit.formatting import format_directory


def main(dir):
    format_directory(dir)


def entrypoint(**kwargs):
    main(**kwargs)


if __name__ == '__main__':
    fire.Fire(entrypoint)
