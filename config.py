import os
import yaml

oss_config = {
    "ID": "",
    "Secret": "",
    "Bucket": "",
    "Endpoint": "",
    "Directory": "",
    "Link": "",
}

post_config = {
    "Post_ID": "",
    "Img_ID": "",
}


def init_config() -> None:
    print("======OSS设置======")
    print("输入AccessKey ID: ", end="")
    oss_config["ID"] = input()
    print("输入AccessKey Secret: ", end="")
    oss_config["Secret"] = input()
    print("输入Bucket名: ", end="")
    oss_config["Bucket"] = input()
    print("输入Endpoint(不包含Bucket名): ", end="")
    oss_config["Endpoint"] = input()
    print("输入上传路径(开头无/): ", end="")
    oss_config["Directory"] = input()
    print("输入外链链接(留空则自动拼接): ", end="")
    oss_config["Link"] = input()
    if oss_config["Link"] == "":
        oss_config["Link"] = oss_config["Bucket"] + "." + oss_config["Endpoint"]
    print("======文章设置======")
    print("输入文章ID: ", end="")
    post_config["Post_ID"] = input()
    print("输入图片ID: ", end="")
    post_config["Img_ID"] = input()


def load_config() -> None:
    global oss_config, post_config
    with open("config.yaml", "r") as config_file:
        all_config = yaml.safe_load(config_file)
    oss_config = all_config["oss"]
    post_config = all_config["post"]


def save_config() -> None:
    all_config = {
        "oss": oss_config,
        "post": post_config,
    }
    with open("config.yaml", "w") as config_file:
        yaml.safe_dump(all_config, config_file, sort_keys=False)


def increase_id() -> None:
    global post_config
    img_id = int(post_config["Img_ID"])
    img_id += 1
    post_config["Img_ID"] = "{:02d}".format(img_id)
    save_config()


if os.path.exists("config.yaml"):
    load_config()
else:
    init_config()
    save_config()
