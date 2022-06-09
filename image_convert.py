import os
from PIL import Image


def to_webp(original_file: str, webp_path: str) -> bool:
    """图片转 WebP

    :param original_file: 原图路径和文件名
    :param webp_path: 转换后图片路径
    :return: 是否转换成功
    """
    try:
        file_name = os.path.basename(original_file)
        ori = Image.open(original_file)
        ori.save(webp_path + file_name, "WEBP")
        return True
    except Exception:
        return False
