from InquirerPy import inquirer
from InquirerPy.base.control import Choice

from utils.config import change_config
from page.auto_upload import auto_upload
from page.maunal_upload import manual_upload
from utils.clear_screen import clear_screen
from utils.breadcrumb import print_breadcrumb

if __name__ == "__main__":
    while True:
        clear_screen()
        print_breadcrumb(["首页"])
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
            auto_upload()
        elif action == 1:
            manual_upload()
        elif action == 2:
            change_config()
        else:
            exit(0)
