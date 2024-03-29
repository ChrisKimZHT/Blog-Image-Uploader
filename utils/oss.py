import os

import oss2

from config.config_control import config

oss = []


def init_oss() -> bool:
    try:
        auth = oss2.Auth(config["auth"]["id"], config["auth"]["secret"])  # 初始化身份验证
        bucket = oss2.Bucket(auth, config["bucket"]["endpoint"], config["bucket"]["name"])  # 初始化Bucket
    except:
        return False
    oss.append(auth)
    oss.append(bucket)
    return True


def test_bucket() -> bool:
    """
    OSS测试，将会进行一次上传、下载操作，操作后会删除测试文件
    :return:
    """
    auth, bucket = oss
    try:
        bucket.put_object("BUCKET_TEST_FILE", b"Test File")
        test_object = bucket.get_object("BUCKET_TEST_FILE")
        bucket.delete_object("BUCKET_TEST_FILE")
    except:
        return False
    return test_object.read() == b"Test File"


def upload_file(local_file: str) -> str:
    """
    OSS上传文件
    :param local_file: 本地文件的路径
    :return: 上传对象的OSS链接
    """
    auth, bucket = oss
    file_name = os.path.basename(local_file)
    bucket.put_object_from_file(
        key=os.path.join(config["upload"]["bucket_dir"], file_name),
        filename=local_file,
        headers={"Content-Type": f"image/{config['upload']['trans_format']}"}
    )
    return config["bucket"]["public_link"] + "/" + config["upload"]["bucket_dir"] + file_name
