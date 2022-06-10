from upload_oss import upload_file
from image_convert import to_webp
import yaml
import re
import os
import shutil

# 文件名配置
file_name_config = {
    "Post_ID": "01",
    "Img_ID": "01",
}

# 图片路径
orig_path = "Images/Original/"
webp_path = "Images/WebP/"


def load_file_name_config() -> None:
    """加载文件名配置，读取得到文章ID和当前图片序号"""
    global file_name_config
    try:
        with open("id_config.yaml", "r") as temp_config_file:
            file_name_config = yaml.safe_load(temp_config_file)
        print(f"[INFO] 文件名配置读取成功: {file_name_config['Post_ID']}-{file_name_config['Img_ID']}")
        return
    except FileNotFoundError:
        print("[ERROR] 未找到文件名配置，开始生成新的文件名配置。")
        print("设置文章ID: ", end="")
        file_name_config["Post_ID"] = input()
        print("设置图片ID起始: ", end="")
        file_name_config["Img_ID"] = input()
        with open("id_config.yaml", "w") as temp_config_file:
            yaml.safe_dump(file_name_config, temp_config_file)
        print("[INFO] 文件名配置生成完成")
        return


def increase_id() -> None:
    """将图片序号+1并更新当前序号"""
    global file_name_config
    img_id = int(file_name_config["Img_ID"])
    img_id += 1
    file_name_config["Img_ID"] = "{:02d}".format(img_id)
    try:
        with open("id_config.yaml", "w") as temp_config_file:
            yaml.safe_dump(file_name_config, temp_config_file)
        print("[INFO] 文件名配置更新成功")
    except:
        print("[ERROR] 文件名配置更新失败")


def main() -> bool:
    """程序主逻辑

    :return: 返回True即循环运行，False代表退出程序
    """
    # 输出信息
    print(f"[INFO] 上传已就绪: {file_name_config['Post_ID']}-{file_name_config['Img_ID']}")
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
        print("[ERROR] 路径异常，请重新输入。")
    # 复制图片到/Images/Original
    print("[INFO] 开始复制图片")
    try:
        img_name = f"{file_name_config['Post_ID']}-{file_name_config['Img_ID']}{os.path.splitext(img_dir)[-1]}"
        shutil.copy(img_dir, os.path.join(orig_path, img_name))
        print("[INFO] 图片已复制至: " + os.path.join(orig_path, img_name))
    except:
        print("[ERROR] 图片复制失败")
        return True
    # 图片转码为WebP
    print("[INFO] 开始图片转码")
    try:
        new_dir = to_webp(os.path.join(orig_path, img_name), webp_path)
        print("[INFO] 图片已转码至: " + new_dir)
        img_name = os.path.basename(new_dir)
    except:
        print("[ERROR] 图片转码失败")
        return True
    # 图片上传OSS
    print("[INFO] 开始图片上传")
    try:
        link = upload_file(os.path.join(webp_path, img_name))
        print(f"[INFO] 图片已上传至OSS成功: {link}")
    except:
        print("[ERROR] 图片上传至OSS失败")
        return True
    # 图片序号+1
    increase_id()
    return True


if __name__ == "__main__":
    load_file_name_config()
    while main():
        pass
