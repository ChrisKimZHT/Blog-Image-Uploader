import pyperclip
from InquirerPy import inquirer
from InquirerPy.utils import color_print
from InquirerPy.validator import PathValidator

from config.config_control import config, increase_id
from utils.breadcrumb import print_breadcrumb, push_breadcrumb, pop_breadcrumb
from utils.clear_screen import clear_screen
from utils.process import process


def auto_upload() -> None:
    while True:
        clear_screen()
        print_breadcrumb()

        dest_bucket_name = config["bucket"]["name"]
        dest_bucket_dir = config["upload"]["bucket_dir"]
        dest_name_without_ext = config["rename"]["post_id"] + "-" + config["rename"]["img_id"]
        dest_name = dest_name_without_ext + "." + config["upload"]["trans_format"]
        print(f"目的位置: oss://{dest_bucket_name}/{dest_bucket_dir + dest_name}")

        # 获取本地原图路径
        try:
            src_path = inquirer.filepath(
                message="请输入文件路径:",
                validate=PathValidator(is_file=True, message="文件路径错误"),
            ).execute()
        except KeyboardInterrupt:
            return

        clear_screen()
        push_breadcrumb("开始上传")
        print_breadcrumb()
        pop_breadcrumb()

        print(f"本地路径: {src_path}")
        print(f"目的路径: oss://{dest_bucket_name}/{dest_bucket_dir + dest_name}")

        public_link = process(src_path, dest_name_without_ext)
        if len(public_link):
            increase_id()
            color_print([("green", "[上传成功] "), ("orange", "图片链接: "), ("blue", public_link)])
            pyperclip.copy(public_link)
            color_print([("orange", "(图片链接已复制)")])
        else:
            color_print([("red", "[上传失败] "), ("orange", "图片上传失败")])

        input("按回车继续")
