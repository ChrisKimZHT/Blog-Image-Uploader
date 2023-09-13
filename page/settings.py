from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator

from config.config_control import config, update_config
from utils.breadcrumb import print_breadcrumb
from utils.clear_screen import clear_screen


def settings() -> None:
    while True:
        clear_screen()
        print_breadcrumb()
        edited_config = config
        try:
            action = inquirer.select(
                message="选择设置项目:",
                choices=[
                    Choice(value=0, name="账号设置"),
                    Choice(value=1, name="储存桶设置"),
                    Choice(value=2, name="上传设置"),
                    Choice(value=3, name="命名设置"),
                    Separator(),
                    Choice(value=-2, name="返回"),
                    Choice(value=-1, name="保存并返回"),
                ],
                default=None,
            ).execute()
        except KeyboardInterrupt:
            return
        if action == -2:
            return
        elif action == -1:
            update_config(edited_config)
            return
