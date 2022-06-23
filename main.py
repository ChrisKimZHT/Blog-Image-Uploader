from config import post_config, increase_id
from oss import upload_file
from convert import to_webp
import re
import os
import shutil

orig_path = "Images/Original/"
webp_path = "Images/WebP/"


def check(input_dir: str) -> str:
    """接受用户输入图片路径且检查合法性，并且进行转换

    :param input_dir: 输入的路径
    :return: 图片路径
    """
    # 替换\为/
    input_dir = re.compile(r"\\").sub("/", input_dir)
    # 删除多余引号
    input_dir = re.compile("\"").sub("", input_dir)
    if os.path.exists(input_dir):
        return input_dir
    return ""


def copy(post_id: str, img_id: str, img_dir: str) -> str:
    """复制图片到/Images/Original

    :param post_id: 文章ID
    :param img_id: 图片ID
    :param img_dir: 图片目录
    :return: 图片路径
    """
    try:
        img_name = f"{post_id}-{img_id}{os.path.splitext(img_dir)[-1]}"
        new_dir = os.path.join(orig_path, img_name)
        shutil.copy(img_dir, new_dir)
        print("图片已复制至: " + new_dir)
        return new_dir
    except:
        return ""


def convert(img_dir: str) -> str:
    """图片转码为WebP

    :param img_dir: 原图路径
    :return: 图片路径
    """
    try:
        path = os.path.join(webp_path, os.path.splitext(os.path.basename(img_dir))[0] + ".webp")
        to_webp(img_dir, path)
        print("图片已转码至: " + path)
        return path
    except:
        return ""


def upload(img_dir: str) -> str:
    """上传图片至OSS

    :param img_dir: 原图路径
    :return:
    """
    try:
        link = upload_file(img_dir)
        print(f"图片已上传至OSS成功: {link}")
        return link
    except:
        return ""


def common_upload() -> bool:
    # 输出信息
    print(f"上传已就绪: {post_config['Post_ID']}-{post_config['Img_ID']}")
    # 输入图片路径并检测合法性
    print("输入图片路径: ", end="")
    input_str = input()
    if input_str == "q" or input_str == "Q":  # q键退出
        return False
    img_dir = check(input_str)
    if img_dir == "":  # 异常退出
        return False
    # 复制图片到/Images/Original
    ori_img_dir = copy(post_config["Post_ID"], post_config["Img_ID"], img_dir)
    if ori_img_dir == "":  # 异常退出
        return False
    # 图片转码为WebP
    webp_img_dir = convert(ori_img_dir)
    if webp_img_dir == "":  # 异常退出
        return False
    # 图片上传OSS
    link = upload(webp_img_dir)
    if link == "":  # 异常退出
        return False
    # 图片序号+1
    increase_id()
    return True


def custom_upload() -> bool:
    print("输入文章ID: ", end="")
    post_id = input()
    print("输入图片ID: ", end="")
    img_id = input()
    # 输出信息
    print(f"上传已就绪: {post_id}-{img_id}")
    # 输入图片路径并检测合法性
    print("输入图片路径: ", end="")
    input_str = input()
    if input_str == "q" or input_str == "Q":  # q键退出
        return False
    img_dir = check(input_str)
    if img_dir == "":  # 异常退出
        return False
    # 复制图片到/Images/Original
    ori_img_dir = copy(post_id, img_id, img_dir)
    if ori_img_dir == "":  # 异常退出
        return False
    # 图片转码为WebP
    webp_img_dir = convert(ori_img_dir)
    if webp_img_dir == "":  # 异常退出
        return False
    # 图片上传OSS
    link = upload(webp_img_dir)
    if link == "":  # 异常退出
        return False
    return True


if __name__ == "__main__":
    while True:
        print("1. 普通上传\n"
              "2. 自定上传\n"
              "q. 退出\n"
              "选择上传模式：", end="")
        choose = input()
        if choose == "q" or choose == "Q":
            break
        elif choose == "1":
            while common_upload():
                pass
        elif choose == "2":
            while custom_upload():
                pass
        else:
            print("输入异常.请重新输入")
