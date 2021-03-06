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
    "Use_Move": False,
    "Image_Format": "",
}


def set_oss_config() -> None:
    print("------OSS设置------")
    oss_config["ID"] = input("输入AccessKey ID: ") or oss_config["ID"]
    oss_config["Secret"] = input("输入AccessKey Secret: ") or oss_config["Secret"]
    oss_config["Bucket"] = input("输入Bucket名: ") or oss_config["Bucket"]
    oss_config["Endpoint"] = input("输入Endpoint(不包含Bucket名): ") or oss_config["Endpoint"]
    oss_config["Directory"] = input("输入上传路径(开头无/): ") or oss_config["Directory"]
    oss_config["Link"] = input("输入外链链接(留空则自动拼接): ") or oss_config["Link"] or (
            oss_config["Bucket"] + "." + oss_config["Endpoint"])
    print("------设置完成------")
    for item in oss_config.items():
        print(item[0], ':', item[1])


def set_post_config() -> None:
    print("------文章设置------")
    post_config["Post_ID"] = input("输入文章ID: ") or post_config["Post_ID"] or "0001"
    post_config["Img_ID"] = input("输入图片ID: ") or post_config["Img_ID"] or "01"
    print("------设置完成------")
    for item in post_config.items():
        print(item[0], ':', item[1])


def set_program_config() -> None:
    print("------程序设置------")
    program_config["Original_Path"] = input("输入原图储存路径(留空默认为Images/Original/): ") or program_config[
        "Original_Path"] or "Images/Original/"
    program_config["WebP_Path"] = input("输入WebP储存路径(留空默认为Images/WebP/): ") or program_config[
        "WebP_Path"] or "Images/WebP/"
    if not os.path.exists(program_config["Original_Path"]):
        os.makedirs(program_config["Original_Path"])
    if not os.path.exists(program_config["WebP_Path"]):
        os.makedirs(program_config["WebP_Path"])
    temp = input("是否使用移动代替复制来归档图片(Y/N): ")
    if temp == "Y" or temp == "y":
        program_config["Use_Move"] = True
    else:
        program_config["Use_Move"] = False
    program_config["Image_Format"] = input("输入图片转码格式(jpeg/png/webp/gif): ") or "webp"
    print("------设置完成------")
    for item in program_config.items():
        print(item[0], ':', item[1])


def init_config() -> None:
    print("======初始设置======")
    set_oss_config()
    set_post_config()
    set_program_config()
    save_config()


def load_config() -> None:
    global oss_config, post_config, program_config
    try:
        with open("config.yaml", "r") as config_file:
            all_config = yaml.safe_load(config_file)
        oss_config = all_config["oss"]
        post_config = all_config["post"]
        program_config = all_config["program"]
    except:
        print("配置文件读取失败，请检查配置文件是否有格式错误")


def save_config() -> None:
    all_config = {
        "oss": oss_config,
        "post": post_config,
        "program": program_config,
    }
    try:
        with open("config.yaml", "w") as config_file:
            yaml.safe_dump(all_config, config_file, sort_keys=False)
    except:
        print("配置文件保存失败")


def change_config() -> None:
    while True:
        print("======修改设置======")
        print("进入后留空即代表不修改设置")
        print("1. OSS设置\n"
              "2. 文章设置\n"
              "3. 程序设置\n"
              "4. 重设所有\n"
              "q. 保存并退出")
        choice = input("请选择需要修改的项目: ")
        if choice == "q" or choice == "Q":
            break
        elif choice == "1":
            set_oss_config()
        elif choice == "2":
            set_post_config()
        elif choice == "3":
            set_program_config()
        elif choice == "4":
            init_config()
        else:
            print("输入异常.请重新输入")
    save_config()


def increase_id() -> None:
    global post_config
    img_id = int(post_config["Img_ID"]) + 1
    post_config["Img_ID"] = "{:02d}".format(img_id)
    save_config()


if os.path.exists("config.yaml"):
    load_config()
else:
    print("未找到配置文件，进行配置文件初始化")
    init_config()
