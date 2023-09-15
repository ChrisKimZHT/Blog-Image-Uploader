from InquirerPy.utils import color_print

breadcrumb_list = []


def print_breadcrumb(sep: str = ">", show_prefix: bool = True) -> None:
    """
    向屏幕打印面包屑导航
    :param sep: 分隔符（无需空格）
    :param show_prefix: 是否作为前缀显示
    :return:
    """
    color_print([("#61AFEF", "Enter: "), ("", "确定, "),
                 ("#61AFEF", "↑ ↓: "), ("", "选择, "),
                 ("#61AFEF", "Ctrl+C: "), ("", "取消, "), ])
    prt_list = []
    first = True
    for bc in breadcrumb_list:
        if first:
            first = False
            if show_prefix:
                prt_list.append(("#98C379", f"{sep} "))
            prt_list.append(("#E5C07B", bc))
            continue
        prt_list.append(("#98C379", f" {sep} "))
        prt_list.append(("#E5C07B", bc))
    color_print(prt_list)
    print()


def push_breadcrumb(breadcrumb: str) -> None:
    breadcrumb_list.append(breadcrumb)


def pop_breadcrumb() -> None:
    breadcrumb_list.pop()
