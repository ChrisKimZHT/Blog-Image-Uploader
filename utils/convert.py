import os

from PIL import Image


def image_convert(original_file: str, converted_file: str) -> None:
    """
    将图片转换为对应格式，格式取决于参数中的后缀名
    :param original_file: 原图路径
    :param converted_file: 转换后图片路径
    """
    new_suffix = os.path.splitext(converted_file)[-1][1:]  # 新图片后缀（不带点）
    img = Image.open(original_file)
    img.save(converted_file, new_suffix)
