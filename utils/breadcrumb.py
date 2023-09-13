breadcrumb_list = []


def print_breadcrumb(sep: str = ">", show_prefix: bool = True) -> None:
    """
    向屏幕打印面包屑导航
    :param sep: 分隔符（无需空格）
    :param show_prefix: 是否作为前缀显示
    :return:
    """
    result = ""
    if show_prefix:
        result += f"{sep} "
    result += f" {sep} ".join(breadcrumb_list)
    print(result)


def push_breadcrumb(breadcrumb: str) -> None:
    breadcrumb_list.append(breadcrumb)


def pop_breadcrumb() -> None:
    breadcrumb_list.pop()
