from math import floor


def print_time_taken(delta, text='Experiment took: ', logger=None):
    minutes = floor(delta / 60)
    seconds = delta - minutes * 60
    message = text + f'{minutes:4d} min and {seconds:4.2f} sec'
    if logger is not None:
        logger.info(message)
    else:
        print(message)
