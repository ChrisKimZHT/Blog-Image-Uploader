import pyperclip
from InquirerPy import inquirer
from InquirerPy.utils import color_print
from InquirerPy.validator import PathValidator

from config.config_control import config
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

        dest_bucket_name = config["bucket"]["name"]
        dest_bucket_dir = config["upload"]["bucket_dir"]
        dest_name = dest_name_without_ext + "." + config["upload"]["trans_format"]

        # 获取本地原图路径
        try:
            src_path = inquirer.filepath(
                message="请输入文件路径:",
                validate=PathValidator(is_file=True, message="文件路径错误"),
            ).execute()
        except KeyboardInterrupt:
            return

        print(f"本地路径: {src_path}")
        print(f"目的路径: oss://{dest_bucket_name}/{dest_bucket_dir + dest_name}")

        public_link = process(src_path, dest_name_without_ext)
        if len(public_link):
            color_print([("green", "[上传成功] "), ("orange", "图片链接: "), ("blue", public_link)])
            pyperclip.copy(public_link)
            color_print([("orange", "(图片链接已复制)")])
        else:
            color_print([("red", "[上传失败] "), ("orange", "图片上传失败")])

        input("按回车继续")
