import os.path

from PIL import Image


def image_convert(original_file: str, converted_file: str) -> None:
    new_suffix = os.path.splitext(converted_file)[-1][1:]  # 新图片后缀（不带点）
    img = Image.open(original_file)
    img.save(converted_file, new_suffix)
