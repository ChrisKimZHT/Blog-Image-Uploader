import os
import shutil

import pyperclip

from config.config_control import config
from utils.convert import image_convert
from utils.oss import upload_file


def process(source_dir: str, dest_name_without_ext: str) -> bool:
    """
    完整的一次操作
    :param source_dir: 源文件位置
    :param dest_name_without_ext: 目的文件名
    :return: 操作是否成功
    """
    # 目录操作
    source_dir = source_dir.strip()  # 去除首尾多余空格
    source_dir = source_dir.replace("\\", "/")  # 替换\为/
    source_dir = source_dir.strip("\'").strip("\"")  # 删除多余引号
    if not os.path.exists(source_dir):
        print("文件路径异常")
        return False

    # 复制并重命名
    original_ext = os.path.splitext(source_dir)[-1]  # 图片后缀名
    renamed_dir = os.path.join(config["upload"]["local_original_dir"], dest_name_without_ext + original_ext)  # 新图片路径
    try:
        if config["upload"]["use_move"]:
            shutil.move(source_dir, renamed_dir)  # 移动文件
            print(f"文件移动成功: {source_dir} -> {renamed_dir}")
        else:
            shutil.copy(source_dir, renamed_dir)  # 复制文件
            print(f"文件复制成功: {source_dir} -> {renamed_dir}")
    except Exception as e:
        print(f"文件复制失败:\n{e}")
        return False

    # 图片转码
    converted_dir = os.path.join(
        config["upload"]["local_trans_dir"],
        dest_name_without_ext + "." + config["upload"]["trans_format"]
    )  # 转码后图片路径
    try:
        image_convert(renamed_dir, converted_dir)
        print(f"图片转码成功: {renamed_dir} -> {converted_dir}")
    except Exception as e:
        print(f"图片转码失败:\n{e}")
        return False

    # 图片上传
    try:
        link = upload_file(converted_dir)
        print(f"文件上传成功: {converted_dir} -> {link}")
        pyperclip.copy(link)
        print("链接已复制到剪贴板")
    except Exception as e:
        print(f"文件上传失败:\n{e}")
        return False

    return True
