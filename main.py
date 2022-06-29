from config import post_config, program_config, change_config, increase_id
from oss import upload_file
from convert import image_convert
import re
import os
import shutil


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
        shutil.copy(source_dir, renamed_dir)  # 复制文件
        print(f"文件复制成功: {source_dir} -> {renamed_dir}")
    except:
        print("文件复制失败")
        return False
    # 图片转码
    converted_dir = os.path.join(program_config["WebP_Path"], new_name_withoud_ext + ".webp")  # 转码后图片路径
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
    except:
        print("文件上传失败")
        return False
    return True


def common_upload() -> None:
    while True:
        new_name_without_ext = post_config['Post_ID'] + "-" + post_config['Img_ID']
        print("======普通上传======")
        print(f"上传已就绪，下一张图片: {new_name_without_ext}.webp")
        directory = input("输入图片路径: ")
        if directory == "q" or directory == "Q":
            break
        if process(directory, new_name_without_ext):
            increase_id()


def custom_upload() -> None:
    while True:
        print("======自定上传======")
        new_name_without_ext = input("输入图片名称(不包含后缀名): ")
        if new_name_without_ext == "q" or new_name_without_ext == "Q":
            break
        directory = input("输入图片路径: ")
        if directory == "q" or directory == "Q":
            break
        process(directory, new_name_without_ext)


if __name__ == "__main__":
    while True:
        print("===================\n"
              "Blog Image Uploader\n"
              "===================")
        print("1. 普通上传\n"
              "2. 自定上传\n"
              "3. 修改设置\n"
              "q. 退出\n"
              "选择上传模式：", end="")
        choose = input()
        if choose == "q" or choose == "Q":
            break
        elif choose == "1":
            common_upload()
        elif choose == "2":
            custom_upload()
        elif choose == "3":
            change_config()
        else:
            print("输入异常.请重新输入")
