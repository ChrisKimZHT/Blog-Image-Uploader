import os
import yaml

# OSS相关配置
oss_config = {
    "ID": "",
    "Secret": "",
    "Bucket": "",
    "Endpoint": "",
    "Directory": "",
    "Link": "",
}

# 图片命名的相关配置
post_config = {
    "Post_ID": "",
    "Img_ID": "",
}

# 该程序的设置
program_config = {
    "Original_Path": "",
    "WebP_Path": "",
}


def init_config() -> None:
    print("======OSS设置======")
    oss_config["ID"] = input("输入AccessKey ID: ")
    oss_config["Secret"] = input("输入AccessKey Secret: ")
    oss_config["Bucket"] = input("输入Bucket名: ")
    oss_config["Endpoint"] = input("输入Endpoint(不包含Bucket名): ")
    oss_config["Directory"] = input("输入上传路径(开头无/): ")
    oss_config["Link"] = input("输入外链链接(留空则自动拼接): ") or (oss_config["Bucket"] + "." + oss_config["Endpoint"])
    print("======文章设置======")
    post_config["Post_ID"] = input("输入文章ID: ")
    post_config["Img_ID"] = input("输入图片ID: ")
    print("======程序设置======")
    program_config["Original_Path"] = input("输入原图储存路径(留空默认为Images/Original/): ") or "Images/Original/"
    program_config["WebP_Path"] = input("输入WebP储存路径(留空默认为Images/WebP/): ") or "Images/WebP/"


def load_config() -> None:
    global oss_config, post_config, program_config
    with open("config.yaml", "r") as config_file:
        all_config = yaml.safe_load(config_file)
    oss_config = all_config["oss"]
    post_config = all_config["post"]
    program_config = all_config["program"]


def save_config() -> None:
    all_config = {
        "oss": oss_config,
        "post": post_config,
        "program": program_config,
    }
    with open("config.yaml", "w") as config_file:
        yaml.safe_dump(all_config, config_file, sort_keys=False)


def increase_id() -> None:
    global post_config
    img_id = int(post_config["Img_ID"]) + 1
    post_config["Img_ID"] = "{:02d}".format(img_id)
    save_config()


if os.path.exists("config.yaml"):
    load_config()
else:
    init_config()
    save_config()
