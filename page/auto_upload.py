from InquirerPy import inquirer
from InquirerPy.validator import PathValidator

from config.config_control import config, increase_id
from utils.breadcrumb import print_breadcrumb
from utils.clear_screen import clear_screen
from utils.process import process


def auto_upload() -> None:
    while True:
        clear_screen()
        print_breadcrumb()

        dest_bucket_dir = config["upload"]["bucket_dir"]
        dest_name_without_ext = config["rename"]["post_id"] + "-" + config["rename"]["img_id"]
        dest_name = dest_name_without_ext + "." + config["upload"]["trans_format"]
        print(f"目的位置: {dest_bucket_dir + dest_name}")

        # 获取本地原图路径
        try:
            src_path = inquirer.filepath(
                message="请输入文件路径:",
                validate=PathValidator(is_file=True, message="文件路径错误"),
            ).execute()
        except KeyboardInterrupt:
            return

        if process(src_path, dest_name_without_ext):
            increase_id()
