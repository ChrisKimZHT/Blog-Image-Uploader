import os

from InquirerPy import inquirer
from InquirerPy.base.control import Choice

from config.config_control import config
from page.auto_upload import auto_upload
from page.maunal_upload import manual_upload
from page.settings import settings
from utils.breadcrumb import print_breadcrumb, push_breadcrumb, pop_breadcrumb
from utils.clear_screen import clear_screen
from utils.oss import test_bucket


def init():
    push_breadcrumb("首页")
    original_dir = config["upload"]["local_original_dir"]
    trans_dir = config["upload"]["local_trans_dir"]
    os.makedirs(original_dir, exist_ok=True)
    os.makedirs(trans_dir, exist_ok=True)
    if not test_bucket():
        print("Bucket测试未通过，请检查账号")


def main():
    while True:
        clear_screen()
        print_breadcrumb()
        try:
            action = inquirer.select(
                message="请选择操作:",
                choices=[
                    Choice(value=0, name="自动模式"),
                    Choice(value=1, name="手动模式"),
                    Choice(value=2, name="设置"),
                    Choice(value=-1, name="退出"),
                ],
                default=0,
            ).execute()
        except KeyboardInterrupt:
            exit(0)
        if action == 0:
            push_breadcrumb("自动模式")
            auto_upload()
            pop_breadcrumb()
        elif action == 1:
            push_breadcrumb("手动模式")
            manual_upload()
            pop_breadcrumb()
        elif action == 2:
            push_breadcrumb("设置")
            settings()
            pop_breadcrumb()
        else:
            exit(0)


if __name__ == "__main__":
    init()
    main()
