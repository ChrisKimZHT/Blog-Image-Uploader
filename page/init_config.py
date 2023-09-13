from InquirerPy import inquirer

from config.config_model import ConfigModel


def init_config() -> dict:
    new_config = ConfigModel().dict()
    try:
        print("> 配置文件初始化")
        ####################################
        print("> [1] 账号设置")
        key_id = inquirer.text(
            message="Access Key ID:",
            validate=lambda result: len(result) > 0,
            invalid_message="ID不可为空",
        ).execute()

        key_secret = inquirer.secret(
            message="Access Key Secret:",
            validate=lambda result: len(result) > 0,
            invalid_message="Secret不可为空",
        ).execute()

        # TODO: OSS TEST
        new_config["auth"]["id"] = key_id
        new_config["auth"]["secret"] = key_secret
        ####################################
        print("> [2] 储存桶设置")
        bucket_name = inquirer.text(
            message="储存桶名称:",
            validate=lambda result: len(result) > 0,
            invalid_message="名称不可为空",
        ).execute()
        new_config["bucket"]["name"] = bucket_name

        bucket_endpoint = inquirer.text(
            message="Endpoint:",
            validate=lambda result: len(result) > 0,
            invalid_message="Endpoint不可为空",
        ).execute()
        new_config["bucket"]["endpoint"] = bucket_endpoint

        bucket_public_link = inquirer.text(
            message="储存桶公网链接(如果没有请保持默认):",
            default=bucket_name + "." + bucket_endpoint,
            validate=lambda result: len(result) > 0,
            invalid_message="公网链接不可为空",
        ).execute()
        bucket_public_link.removesuffix("/")
        new_config["bucket"]["public_link"] = bucket_public_link
        ####################################
        print("> 设置完成，更多设置请前往菜单")
        inquirer.confirm(
            message="继续?",
            default=True,
            confirm_letter="y",
        ).execute()
        return new_config
    except KeyboardInterrupt:
        exit(0)
