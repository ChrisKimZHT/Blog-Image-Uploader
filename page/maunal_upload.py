from InquirerPy import inquirer
from InquirerPy.validator import PathValidator

from utils.breadcrumb import print_breadcrumb
from utils.clear_screen import clear_screen
from utils.process import process


def manual_upload() -> None:
    while True:
        clear_screen()
        print_breadcrumb()

        # 获取上传后的文件名
        try:
            dest_name_without_ext = inquirer.text(
                message="输入目的文件名(不包含后缀):",
                validate=lambda result: len(result) > 0,
                invalid_message="文件名不可为空",
            ).execute()
        except KeyboardInterrupt:
            return

        # 获取本地原图路径
        try:
            src_path = inquirer.filepath(
                message="请输入文件路径:",
                validate=PathValidator(is_file=True, message="文件路径错误"),
            ).execute()
        except KeyboardInterrupt:
            return

        process(src_path, dest_name_without_ext)

        inquirer.text(message="按回车继续").execute()
