import os
from PIL import Image


def to_webp(original_file: str, webp_path: str) -> str:
    """图片转 WebP

    :param original_file: 原图路径和文件名
    :param webp_path: 转换后图片路径
    :return: 转换后的图片路径
    """
    ori = Image.open(original_file)
    path = os.path.join(webp_path, os.path.splitext(os.path.basename(original_file))[0] + ".webp")
    ori.save(path, "WEBP")
    return path
