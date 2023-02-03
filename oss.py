from config import oss_config, program_config
import oss2
import os

# 初始化身份验证
auth = oss2.Auth(oss_config["ID"], oss_config["Secret"])
# 初始化Bucket
bucket = oss2.Bucket(auth, oss_config["Endpoint"], oss_config["Bucket"])


def test_bucket() -> bool:
    try:
        bucket.put_object("BUCKET_TEST_FILE", b"Test File")
        test_object = bucket.get_object("BUCKET_TEST_FILE")
        bucket.delete_object("BUCKET_TEST_FILE")
    except oss2.exceptions.ServerError:
        return False
    return test_object.read() == b"Test File"


def upload_file(local_file: str) -> str:
    """OSS上传文件

    :param local_file: 本地文件的路径
    :return: 上传对象的OSS链接
    """
    file_name = os.path.basename(local_file)
    bucket.put_object_from_file(os.path.join(oss_config["Directory"], file_name), local_file,
                                headers={"Content-Type": f"image/{program_config['Image_Format']}"})
    return oss_config["Link"] + "/" + oss_config["Directory"] + file_name


if not test_bucket():
    print("OSS Bucket上传测试失败，请检查配置是否正确")
