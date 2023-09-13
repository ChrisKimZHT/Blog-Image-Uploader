from InquirerPy import inquirer
from InquirerPy.validator import PathValidator

from utils.breadcrumb import print_breadcrumb
from utils.clear_screen import clear_screen
from utils.config import post_config, program_config, get_destination, increase_id
from utils.process import process


def auto_upload() -> None:
    while True:
        clear_screen()
        print_breadcrumb()

        dest_name_without_ext = post_config["Post_ID"] + "-" + post_config["Img_ID"]
        dest_name = dest_name_without_ext + "." + program_config["Image_Format"]
        print(f"目的位置: {get_destination()}{dest_name}")

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
