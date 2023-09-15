import os

from config.config_control import config


def init_dirs() -> bool:
    try:
        original_dir = config["upload"]["local_original_dir"]
        trans_dir = config["upload"]["local_trans_dir"]
        os.makedirs(original_dir, exist_ok=True)
        os.makedirs(trans_dir, exist_ok=True)
        return True
    except:
        return False
