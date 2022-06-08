import oss2
import yaml

with open("oss_config.yaml") as config_file:
    config = yaml.safe_load(config_file)

access_key_id = config["ID"]
access_key_secret = config["Secret"]
bucket_name = config["Bucket"]
endpoint = config["Endpoint"]

bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)


def upload_file(local, remote):
    bucket.put_object_from_file(remote, local)
