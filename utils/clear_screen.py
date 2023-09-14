import os


def clear_screen() -> None:
    """
    根据系统类型，执行对应终端清屏指令。
    :return:
    """
    os.system("cls" if os.name == "nt" else "clear")
