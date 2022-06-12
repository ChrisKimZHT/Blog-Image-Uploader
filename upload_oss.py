from logger import log
import os
import oss2
import yaml

log.info("开始初始化OSS上传组件")
with open("oss_config.yaml", "r", encoding="utf-8") as config_file:
    config = yaml.safe_load(config_file)
log.info("打开OSS配置文件完成")
access_key_id = config["ID"]
log.info("读取AccessKey ID完成")
access_key_secret = config["Secret"]
log.info("读取AccessKey Secret完成")
bucket_name = config["Bucket"]
log.info(f"读取Bucket Name完成: {bucket_name}")
endpoint = config["Endpoint"]
log.info(f"读取Endpoint完成: {endpoint}")
directory = config["Directory"]
log.info(f"读取上传路径完成: oss://{bucket_name}/{directory}")
link = config["Link"]
if config["Link"] == "":
    link = bucket_name + "." + endpoint
log.info(f"读取文件外链完成: {link}")

bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)


def upload_file(local_file: str) -> str:
    """OSS 上传文件

    :param local_file: 本地文件的路径和文件名
    :return: 文件OSS外链
    """
    file_name = os.path.basename(local_file)
    bucket.put_object_from_file(os.path.join(directory, file_name), local_file)
    log.info(f"OSS上传: {local_file} --> {os.path.join(directory, file_name)}")
    return link + "/" + directory + file_name
