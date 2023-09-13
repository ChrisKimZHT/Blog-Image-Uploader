import os

import pydantic.error_wrappers
import yaml

from config.config_model import ConfigModel
from page.init_config import init_config


def load_config() -> dict:
    if not os.path.exists("config.yaml"):
        save_config(init_config())
    try:
        with open("config.yaml", "r") as config_file:
            _config = yaml.safe_load(config_file)
    except:
        print("配置文件读取失败")
        return ConfigModel().dict()
    try:
        validated_config = ConfigModel(**_config).dict()
        return validated_config
    except pydantic.error_wrappers.ValidationError as e:
        print(f"配置文件格式非法:\n{e}")
        return ConfigModel().dict()


def save_config(_config: dict) -> None:
    try:
        with open("config.yaml", "w") as config_file:
            yaml.safe_dump(_config, config_file, sort_keys=False)
    except:
        print("配置文件保存失败")


def update_config(edited_config: dict) -> None:
    global config
    save_config(edited_config)
    config = load_config()


def increase_id() -> None:
    global config
    img_id = int(config["rename"]["img_id"]) + 1
    config["rename"]["img_id"] = "{:02d}".format(img_id)
    save_config(config)


def config_startup_init() -> None:
    global config
    config = load_config()


config: dict = {}
