import os
import oss2
import yaml

with open("oss_config.yaml", "r") as config_file:
    config = yaml.safe_load(config_file)

access_key_id = config["ID"]
access_key_secret = config["Secret"]
bucket_name = config["Bucket"]
endpoint = config["Endpoint"]

bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)


def upload_file(local_file: str, remote_path: str) -> bool:
    """OSS 上传文件

    :param local_file: 本地文件的路径和文件名
    :param remote_path: 上传的远程路径
    :return: 是否上传成功
    """
    try:
        file_name = os.path.basename(local_file)
        bucket.put_object_from_file(remote_path + file_name, local_file)
        return True
    except Exception:
        return False
