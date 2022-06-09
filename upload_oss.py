import os
import oss2
import yaml

with open("oss_config.yaml", "r") as config_file:
    config = yaml.safe_load(config_file)

access_key_id = config["ID"]
print("[INFO] 读取AccessKey ID完成")
access_key_secret = config["Secret"]
print("[INFO] 读取AccessKey Secret完成")
bucket_name = config["Bucket"]
print(f"[INFO] 读取Bucket Name完成: {bucket_name}")
endpoint = config["Endpoint"]
print(f"[INFO] 读取Endpoint完成: {endpoint}")
directory = config["Directory"]
print(f"[INFO] 读取上传路径完成: {directory}")

bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)


def upload_file(local_file: str):
    """OSS 上传文件

    :param local_file: 本地文件的路径和文件名
    """
    file_name = os.path.basename(local_file)
    bucket.put_object_from_file(os.path.join(directory, file_name), local_file)
