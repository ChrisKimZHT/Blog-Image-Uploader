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


def increase_id() -> None:
    """将图片序号+1并更新当前序号"""
    global id_config
    img_id = int(id_config["Img_ID"])
    img_id += 1
    id_config["Img_ID"] = "{:02d}".format(img_id)
    try:
        with open("id_config.yaml", "w") as temp_config_file:
            yaml.safe_dump(id_config, temp_config_file)
        log.info("ID配置更新成功")
    except:
        log.error("ID配置更新失败")


def main() -> bool:
    """程序主逻辑

    :return: 返回True即循环运行，False代表退出程序
    """
    # 输出信息
    print(f"上传已就绪: {id_config['Post_ID']}-{id_config['Img_ID']}")
    # 输入图片路径并检测合法性
    while True:
        print("输入图片路径: ", end="")
        img_dir = input()
        if img_dir == "q" or img_dir == "Q":
            return False
        # 替换\为/
        img_dir = re.compile(r"\\").sub("/", img_dir)
        # 删除多余引号
        img_dir = re.compile("\"").sub("", img_dir)
        if os.path.exists(img_dir):
            break
        log.warning("路径异常，请重新输入。")
    # 复制图片到/Images/Original
    try:
        img_name = f"{id_config['Post_ID']}-{id_config['Img_ID']}{os.path.splitext(img_dir)[-1]}"
        shutil.copy(img_dir, os.path.join(orig_path, img_name))
        print("图片已复制至: " + os.path.join(orig_path, img_name))
        log.info("图片已复制至: " + os.path.join(orig_path, img_name))
    except:
        log.error("图片复制失败")
        return True
    # 图片转码为WebP
    try:
        new_dir = to_webp(os.path.join(orig_path, img_name), webp_path)
        print("图片已转码至: " + new_dir)
        img_name = os.path.basename(new_dir)
    except:
        log.error("图片转码失败")
        return True
    # 图片上传OSS
    try:
        link = upload_file(os.path.join(webp_path, img_name))
        print(f"图片已上传至OSS成功: {link}")
    except:
        log.error("图片上传至OSS失败")
        return True
    # 图片序号+1
    increase_id()
    return True


if __name__ == "__main__":
    load_id_config()
    while main():
        log.info("主函数完成")
    log.info("==========程序退出==========")
