def print_breadcrumb(nav: list, sep: str = ">", show_prefix: bool = True) -> None:
    """
    向屏幕打印面包屑导航
    :param nav: 导航列表
    :param sep: 分隔符（无需空格）
    :param show_prefix: 是否作为前缀显示
    :return:
    """
    result = ""
    if show_prefix:
        result += f"{sep} "
    result += f" {sep} ".join(nav)
    print(result)
    print()
