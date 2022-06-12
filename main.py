from upload_oss import upload_file
from image_convert import to_webp
from logger import log
import yaml
import re
import os
import shutil

# 文件名配置
id_config = {
    "Post_ID": "01",
    "Img_ID": "01",
}

# 图片路径
orig_path = "Images/Original/"
webp_path = "Images/WebP/"


def load_id_config() -> None:
    """加载ID配置，读取得到文章ID和当前图片序号"""
    global id_config
    try:
        with open("id_config.yaml", "r") as temp_config_file:
            id_config = yaml.safe_load(temp_config_file)
        log.info(f"ID配置读取成功: {id_config['Post_ID']}-{id_config['Img_ID']}")
        return
    except FileNotFoundError:
        print("未找到文件名配置，开始生成新的文件名配置。")
        print("设置文章ID: ", end="")
        id_config["Post_ID"] = input()
        print("设置图片ID起始: ", end="")
        id_config["Img_ID"] = input()
        with open("id_config.yaml", "w") as temp_config_file:
            yaml.safe_dump(id_config, temp_config_file)
            log.info(f"文件名配置生成成功: {id_config['Post_ID']}-{id_config['Img_ID']}")
        return


def increase_id() -> bool:
    """将图片序号+1并更新当前序号"""
    global id_config
    img_id = int(id_config["Img_ID"])
    img_id += 1
    id_config["Img_ID"] = "{:02d}".format(img_id)
    try:
        with open("id_config.yaml", "w") as temp_config_file:
            yaml.safe_dump(id_config, temp_config_file)
        log.info("ID配置更新成功")
        return True
    except:
        log.error("ID配置更新失败")
        return False


def main():
    """主函数"""
    while True:
        # 选择功能
        print("1. 普通上传\n"
              "2. 封面上传\n"
              "3. 覆盖上传\n"
              "0. 退出\n"
              "选择上传模式：", end="")
        choose = input()
        if choose == "0":
            break
        elif choose == "1":
            while common_upload():
                pass
        elif choose == "2":
            while cover_upload():
                pass
        elif choose == "3":
            while overwrite_upload():
                pass
        else:
            print("输入异常。请重新输入")


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
        log.info("输入路径: " + input_dir)
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
        log.info("图片已复制至: " + new_dir)
        print("图片已复制至: " + new_dir)
        return new_dir
    except:
        log.error("图片复制失败")
        return ""


def convert(img_dir: str) -> str:
    """图片转码为WebP

    :param img_dir: 原图路径
    :return: 图片路径
    """
    try:
        new_dir = to_webp(img_dir, webp_path)
        log.info("图片已转码至: " + new_dir)
        print("图片已转码至: " + new_dir)
        return new_dir
    except:
        log.error("图片转码失败")
        return ""


def upload(img_dir: str) -> str:
    """上传图片至OSS

    :param img_dir: 原图路径
    :return:
    """
    try:
        link = upload_file(img_dir)
        log.info(f"图片已上传至OSS成功: {link}")
        print(f"图片已上传至OSS成功: {link}")
        return link
    except:
        log.error("图片上传至OSS失败")
        return ""


def common_upload() -> bool:
    """普通上传

    :return: 返回真则继续循环，假停止循环
    """
    log.info("开始普通上传")
    # 输出信息
    print(f"上传已就绪: {id_config['Post_ID']}-{id_config['Img_ID']}")
    # 输入图片路径并检测合法性
    print("输入图片路径: ", end="")
    input_str = input()
    if input_str == "q" or input_str == "Q":  # q键退出
        return False
    img_dir = check(input_str)
    if img_dir == "":  # 异常退出
        return False
    # 复制图片到/Images/Original
    ori_img_dir = copy(id_config["Post_ID"], id_config["Img_ID"], img_dir)
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
    return increase_id()


def cover_upload() -> bool:
    """封面上传

    :return: 返回真则继续循环，假停止循环
    """
    log.info("开始封面上传")


def overwrite_upload() -> bool:
    """覆盖上传

    :return: 返回真则继续循环，假停止循环
    """
    log.info("开始覆盖上传")


if __name__ == "__main__":
    load_id_config()
    main()
    log.info("==========程序退出==========")
