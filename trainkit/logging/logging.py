import os
from datetime import datetime
import string
import logging
import random
from trainkit.saving import save_object


class TrainLogger:
    def __init__(self, defaults, output_dir):
        self.defaults = defaults
        self.output_dir = output_dir
        self.logger = self.initialize_logging()
        log_args(defaults, logger=self.logger)
        self.metrics = []

    def initialize_logging(self):
        self.output_dir = add_timestamp_with_random(self.output_dir, ending='')
        os.makedirs(self.output_dir, exist_ok=True)
        logger = prepare_logger(self.output_dir)
        return logger

    def finalize_logging(self):
        save_object(self.metrics, os.path.join(self.output_dir, 'metrics.pkl'))


def prepare_logger(log_dir):
    logger = logging.getLogger(log_dir)
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler(os.path.join(log_dir, "info.log"))
    fh.setLevel(logging.INFO)
    logger.addHandler(fh)
    # ch = logging.StreamHandler()
    # ch.setLevel(logging.INFO)
    # logger.addHandler(ch)
    return logger


def log_args(defaults, logger):
    output_path = os.path.join(logger.name, "defaults.pkl")
    save_object(defaults, output_path)

    for key, value in defaults.items():
        logger.info(f"{key}: {value}")


def add_timestamp(beginning='./params_'):
    time_stamp = datetime.now().strftime("%Y%m%d_%H%M")
    output_file = beginning + time_stamp
    return output_file


def add_timestamp_with_random(beginning='./params_', ending='.pkl'):
    time_stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    time_stamp += '_' + add_random_characters("", size_to_add=4)
    output_file = os.path.join(time_stamp, ending)
    output_file = os.path.join(beginning, output_file)
    return output_file


def add_random_characters(beginning, size_to_add):
    letters = list(string.ascii_letters)
    selected = random.sample(letters, size_to_add)
    stamp = ''.join(selected)
    return beginning + stamp
