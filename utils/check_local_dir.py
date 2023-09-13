import os

from config.config_control import config


def check_local_dir():
    original_dir = config["upload"]["local_original_dir"]
    trans_dir = config["upload"]["local_trans_dir"]
    os.makedirs(original_dir, exist_ok=True)
    os.makedirs(trans_dir, exist_ok=True)
