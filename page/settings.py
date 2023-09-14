import oss2
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
from InquirerPy.validator import PathValidator

from config.config_control import config, update_config
from utils.breadcrumb import print_breadcrumb, push_breadcrumb, pop_breadcrumb
from utils.clear_screen import clear_screen


def settings() -> None:
    while True:
        clear_screen()
        print_breadcrumb()
        edited_config = config
        try:
            action = inquirer.select(
                message="选择设置项目:",
                choices=[
                    Choice(value=0, name="账号设置"),
                    Choice(value=1, name="储存桶设置"),
                    Choice(value=2, name="上传设置"),
                    Choice(value=3, name="命名设置"),
                    Separator(),
                    Choice(value=-2, name="返回"),
                    Choice(value=-1, name="保存并返回"),
                ],
                default=None,
            ).execute()
        except KeyboardInterrupt:
            return
        if action == -2:
            return
        elif action == -1:
            update_config(edited_config)
            return
        elif action == 0:
            push_breadcrumb("账号设置")
            edited_config = auth_settings(edited_config)
            pop_breadcrumb()
        elif action == 1:
            push_breadcrumb("储存桶设置")
            edited_config = bucket_settings(edited_config)
            pop_breadcrumb()
        elif action == 2:
            push_breadcrumb("上传设置")
            edited_config = upload_settings(edited_config)
            pop_breadcrumb()
        elif action == 3:
            push_breadcrumb("命名设置")
            edited_config = raname_settings(edited_config)
            pop_breadcrumb()


def auth_settings(edited_config: dict) -> dict:
    while True:
        clear_screen()
        print_breadcrumb()
        try:
            action = inquirer.select(
                message="选择设置项目:",
                choices=[
                    Choice(value=0, name="Access Key ID"),
                    Choice(value=1, name="Access Key Secret"),
                    Separator(),
                    Choice(value=-1, name="返回"),
                ],
            ).execute()
        except KeyboardInterrupt:
            return edited_config
        if action == -1:
            return edited_config
        elif action == 0:
            clear_screen()
            push_breadcrumb("Access Key ID")
            print_breadcrumb()
            pop_breadcrumb()
            try:
                key_id = inquirer.text(
                    message="Access Key ID:",
                    validate=lambda result: len(result) > 0,
                    invalid_message="ID不可为空",
                    default=edited_config["auth"]["id"]
                ).execute()
            except KeyboardInterrupt:
                continue
            edited_config["auth"]["id"] = key_id
        elif action == 1:
            clear_screen()
            push_breadcrumb("Access Key Secret")
            print_breadcrumb()
            pop_breadcrumb()
            try:
                key_secret = inquirer.secret(
                    message="Access Key Secret:",
                    validate=lambda result: len(result) > 0,
                    invalid_message="Secret不可为空",
                    default=edited_config["auth"]["secret"]
                ).execute()
                edited_config["auth"]["secret"] = key_secret
            except KeyboardInterrupt:
                continue


def bucket_settings(edited_config: dict) -> dict:
    while True:
        clear_screen()
        print_breadcrumb()
        try:
            action = inquirer.select(
                message="选择设置项目:",
                choices=[
                    Choice(value=0, name=f"储存桶名称: {edited_config['bucket']['name']}"),
                    Choice(value=1, name=f"Endpoint: {edited_config['bucket']['endpoint']}"),
                    Choice(value=2, name=f"公网链接: {edited_config['bucket']['public_link']}"),
                    Separator(),
                    Choice(value=-1, name="返回"),
                ],
            ).execute()
        except KeyboardInterrupt:
            return edited_config
        if action == -1:
            return edited_config
        elif action == 0:
            clear_screen()
            push_breadcrumb("储存桶名称")
            print_breadcrumb()
            pop_breadcrumb()
            try:
                bucket_name = inquirer.text(
                    message="储存桶名称:",
                    validate=lambda result: len(result) > 0,
                    invalid_message="名称不可为空",
                    default=edited_config["bucket"]["name"]
                ).execute()
            except KeyboardInterrupt:
                continue
            edited_config["bucket"]["name"] = bucket_name
        elif action == 1:
            clear_screen()
            push_breadcrumb("Endpoint")
            print_breadcrumb()
            pop_breadcrumb()
            try:
                bucket_endpoint = inquirer.text(
                    message="Endpoint:",
                    validate=lambda result: len(result) > 0,
                    invalid_message="Endpoint不可为空",
                    default=edited_config["bucket"]["endpoint"]
                ).execute()
                edited_config["bucket"]["endpoint"] = bucket_endpoint
            except KeyboardInterrupt:
                continue
        elif action == 2:
            clear_screen()
            push_breadcrumb("公网链接")
            print_breadcrumb()
            pop_breadcrumb()
            try:
                bucket_public_link = inquirer.text(
                    message="储存桶公网链接(如果没有请保持默认):",
                    default=edited_config["bucket"]["public_link"],
                    validate=lambda result: len(result) > 0,
                    invalid_message="公网链接不可为空",
                ).execute()
            except KeyboardInterrupt:
                continue
            bucket_public_link.removesuffix("/")
            edited_config["bucket"]["public_link"] = bucket_public_link
            try:
                oss2.Bucket(
                    oss2.Auth(
                        edited_config["auth"]["key"],
                        edited_config["auth"]["secret"]
                    ),
                    edited_config["bucket"]["endpoint"],
                    edited_config["bucket"]["name"]
                )
            except oss2.exceptions.ClientError:
                print("OSS测试失败，请检查配置是否正确")


def upload_settings(edited_config: dict) -> dict:
    while True:
        clear_screen()
        print_breadcrumb()
        try:
            action = inquirer.select(
                message="选择设置项目:",
                choices=[
                    Choice(value=0, name=f"远程上传路径: {edited_config['upload']['bucket_dir']}"),
                    Choice(value=1, name=f"本地原图路径: {edited_config['upload']['local_original_dir']}"),
                    Choice(value=2, name=f"本地转码路径: {edited_config['upload']['local_trans_dir']}"),
                    Choice(value=3, name=f"转码格式: {edited_config['upload']['trans_format']}"),
                    Choice(value=4, name=f"移动图片: {'是' if edited_config['upload']['use_move'] else '否'}"),
                    Separator(),
                    Choice(value=-1, name="返回"),
                ],
            ).execute()
        except KeyboardInterrupt:
            return edited_config
        if action == -1:
            return edited_config
        elif action == 0:
            clear_screen()
            push_breadcrumb("远程上传路径")
            print_breadcrumb()
            pop_breadcrumb()
            try:
                bucket_dir: str = inquirer.text(
                    message="远程上传路径:",
                    default=edited_config['upload']['bucket_dir'],
                ).execute()
            except KeyboardInterrupt:
                continue
            if bucket_dir.startswith("/"):
                bucket_dir = bucket_dir.removeprefix("/")
            edited_config['upload']['bucket_dir'] = bucket_dir
        elif action == 1:
            clear_screen()
            push_breadcrumb("本地原图路径")
            print_breadcrumb()
            pop_breadcrumb()
            try:
                local_original_dir = inquirer.filepath(
                    message="本地原图路径:",
                    validate=PathValidator(is_dir=True, message="路径不合法"),
                    default=edited_config['upload']['local_original_dir'],
                    only_directories=True
                ).execute()
            except KeyboardInterrupt:
                continue
            local_original_dir: str = local_original_dir.strip().replace("\\", "/")
            if not local_original_dir.endswith("/"):
                local_original_dir += "/"
            edited_config['upload']['local_original_dir'] = local_original_dir
        elif action == 2:
            clear_screen()
            push_breadcrumb("本地转码路径")
            print_breadcrumb()
            pop_breadcrumb()
            try:
                local_trans_dir = inquirer.filepath(
                    message="本地转码路径:",
                    validate=PathValidator(is_dir=True, message="路径不合法"),
                    default=edited_config['upload']['local_trans_dir'],
                    only_directories=True
                ).execute()
            except KeyboardInterrupt:
                continue
            local_trans_dir: str = local_trans_dir.strip().replace("\\", "/")
            if not local_trans_dir.endswith("/"):
                local_trans_dir += "/"
            edited_config['upload']['local_trans_dir'] = local_trans_dir
        elif action == 3:
            clear_screen()
            push_breadcrumb("转码格式")
            print_breadcrumb()
            pop_breadcrumb()
            try:
                trans_format: str = inquirer.text(
                    message="转码格式:",
                    default=edited_config['upload']['trans_format'],
                    validate=lambda result: len(result) > 0,
                    invalid_message="格式不可为空",
                ).execute()
            except KeyboardInterrupt:
                continue
            edited_config['upload']['trans_format'] = trans_format
        elif action == 4:
            clear_screen()
            push_breadcrumb("移动图片")
            print_breadcrumb()
            pop_breadcrumb()
            try:
                use_move: bool = inquirer.select(
                    message="使用移动代替复制:",
                    choices=[
                        Choice(value=True, name="是"),
                        Choice(value=False, name="否"),
                    ],
                    default=edited_config['upload']['use_move'],
                ).execute()
            except KeyboardInterrupt:
                continue
            edited_config['upload']['use_move'] = use_move


def raname_settings(edited_config: dict) -> dict:
    while True:
        clear_screen()
        print_breadcrumb()
        try:
            action = inquirer.select(
                message="选择设置项目:",
                choices=[
                    Choice(value=0, name=f"文章ID: {edited_config['rename']['post_id']}"),
                    Choice(value=1, name=f"图片ID: {edited_config['rename']['img_id']}"),
                    Separator(),
                    Choice(value=-1, name="返回"),
                ],
            ).execute()
        except KeyboardInterrupt:
            return edited_config
        if action == -1:
            return edited_config
        elif action == 0:
            clear_screen()
            push_breadcrumb("文章ID")
            print_breadcrumb()
            pop_breadcrumb()
            try:
                post_id = inquirer.text(
                    message="文章ID:",
                    validate=lambda result: len(result) > 0,
                    invalid_message="ID不可为空",
                    default=edited_config["rename"]["post_id"]
                ).execute()
            except KeyboardInterrupt:
                continue
            edited_config["rename"]["post_id"] = post_id
        elif action == 1:
            clear_screen()
            push_breadcrumb("图片ID")
            print_breadcrumb()
            pop_breadcrumb()
            try:
                img_id = inquirer.text(
                    message="图片ID:",
                    validate=lambda result: len(result) > 0,
                    invalid_message="ID不可为空",
                    default=edited_config["rename"]["img_id"]
                ).execute()
            except KeyboardInterrupt:
                continue
            edited_config["rename"]["img_id"] = img_id
