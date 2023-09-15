from InquirerPy import inquirer
from InquirerPy.base.control import Choice

from config.config_control import init_config
from page.auto_upload import auto_upload
from page.maunal_upload import manual_upload
from page.settings import settings
from utils.breadcrumb import print_breadcrumb, push_breadcrumb, pop_breadcrumb
from utils.clear_screen import clear_screen
from utils.init_dirs import init_dirs
from utils.oss import test_bucket, init_oss


def init():
    try:
        flag = True
        print("读取配置文件...", end=" ")
        flag &= init_config()
        print("完成" if flag else "错误")
        if not flag:
            raise
        print("初始化图片目录...", end=" ")
        flag &= init_dirs()
        print("完成" if flag else "错误")
        if not flag:
            raise
        print("初始化OSS...", end=" ")
        flag &= init_oss()
        print("完成" if flag else "错误")
        if not flag:
            raise
        print("测试OSS...", end=" ")
        flag &= test_bucket()
        print("完成" if flag else "错误")
        if not flag:
            raise
    except:
        print("[!] 程序初始化出现错误，请检查配置")
        input("按任意键继续...")


def main():
    push_breadcrumb("首页")
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
