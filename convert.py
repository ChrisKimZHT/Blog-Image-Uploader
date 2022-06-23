from PIL import Image


def to_webp(original_file: str, webp_path: str) -> None:
    Image.open(original_file).save(webp_path, "WEBP")
