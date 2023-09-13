import os
import re
import shutil

import pyperclip

from convert import image_convert
from utils.config import program_config
from utils.oss import upload_file


def process(source_dir: str, new_name_withoud_ext: str) -> bool:
    # 目录操作
    source_dir = source_dir.strip()  # 去除首尾多余空格
    source_dir = re.compile(r"\\").sub("/", source_dir)  # 替换\为/
    source_dir = re.compile("\"").sub("", source_dir)  # 删除多余引号
    if not os.path.exists(source_dir):
        print("文件路径异常")
        return False
    # 复制并重命名
    original_ext = os.path.splitext(source_dir)[-1]  # 图片后缀名
    renamed_dir = os.path.join(program_config["Original_Path"], new_name_withoud_ext + original_ext)  # 新图片路径
    try:
        if program_config["Use_Move"]:
            shutil.move(source_dir, renamed_dir)  # 移动文件
            print(f"文件移动成功: {source_dir} -> {renamed_dir}")
        else:
            shutil.copy(source_dir, renamed_dir)  # 复制文件
            print(f"文件复制成功: {source_dir} -> {renamed_dir}")
    except:
        print("文件复制失败")
        return False
    # 图片转码
    converted_dir = os.path.join(program_config["WebP_Path"],
                                 new_name_withoud_ext + "." + program_config["Image_Format"])  # 转码后图片路径
    try:
        image_convert(renamed_dir, converted_dir)
        print(f"图片转码成功: {renamed_dir} -> {converted_dir}")
    except:
        print("图片转码失败")
        return False
    # 图片上传
    try:
        link = upload_file(converted_dir)
        print(f"文件上传成功: {converted_dir} -> {link}")
        pyperclip.copy(link)
        print("链接已复制到剪贴板")
    except:
        print("文件上传失败")
        return False
    return True
