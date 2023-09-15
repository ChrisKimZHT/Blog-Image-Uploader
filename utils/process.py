import os
import shutil

from config.config_control import config
from utils.convert import image_convert
from utils.oss import upload_file


def check_source_dir(source_dir: str) -> str:
    """
    预处理并检查目录
    :param source_dir: 目录
    :return: 目录，若空则异常
    """
    source_dir = source_dir.strip()  # 去除首尾多余空格
    source_dir = source_dir.replace("\\", "/")  # 替换\为/
    source_dir = source_dir.strip("\'").strip("\"")  # 删除多余引号
    if not os.path.exists(source_dir):
        return ""
    return source_dir


def move_and_rename(source_dir: str, dest_name_without_ext: str) -> str:
    """
    将原图储存并重命名
    :param source_dir: 源文件位置
    :param dest_name_without_ext: 目的文件名（不含后缀）
    :return: 目的文件，若空则异常
    """
    original_ext = os.path.splitext(source_dir)[-1]  # 图片后缀名
    renamed_dir = os.path.join(config["upload"]["local_original_dir"], dest_name_without_ext + original_ext)  # 新图片路径
    try:
        if config["upload"]["use_move"]:
            shutil.move(source_dir, renamed_dir)  # 移动文件
        else:
            shutil.copy(source_dir, renamed_dir)  # 复制文件
        return renamed_dir
    except:
        return ""


def format_convert(dest_name_without_ext: str, renamed_dir: str) -> str:
    """
    图片转码
    :param dest_name_without_ext: 目的文件名（不含后缀）
    :param renamed_dir: 目的文件路径
    :return: 转码文件，若空则异常
    """
    converted_dir = os.path.join(
        config["upload"]["local_trans_dir"],
        dest_name_without_ext + "." + config["upload"]["trans_format"]
    )  # 转码后图片路径
    try:
        image_convert(renamed_dir, converted_dir)
        return converted_dir
    except:
        return ""


def upload_oss(converted_dir: str) -> str:
    """
    将转码文件上传OSS
    :param converted_dir: 转码文件
    :return: 文件外链，若空则异常
    """
    try:
        link = upload_file(converted_dir)
        return link
    except:
        return ""


def process(source_dir: str, dest_name_without_ext: str) -> str:
    """
    完整的一次操作
    :param source_dir: 源文件位置
    :param dest_name_without_ext: 目的文件名（不含后缀）
    :return: 文件外链，若空则异常
    """
    # 预处理并检查目录
    print("检查本地文件目录...", end=" ")
    source_dir = check_source_dir(source_dir)
    if len(source_dir) == 0:
        print("错误")
        return ""
    print("完成")

    # 储存并重命名
    print("储存并重命名原图...", end=" ")
    renamed_dir = move_and_rename(source_dir, dest_name_without_ext)
    if len(renamed_dir) == 0:
        print("错误")
        return ""
    print("完成")

    # 图片转码
    print("图片转码...", end=" ")
    converted_dir = format_convert(dest_name_without_ext, renamed_dir)
    if len(converted_dir) == 0:
        print("错误")
        return ""
    print("完成")

    # 图片上传
    print("上传OSS...", end=" ")
    public_link = upload_oss(converted_dir)
    if len(public_link) == 0:
        print("错误")
        return ""
    print("完成")

    return public_link
