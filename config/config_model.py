from pydantic import BaseModel


class ConfigModel(BaseModel):
    class Auth(BaseModel):
        id: str = ""
        secret: str = ""

    class Bucket(BaseModel):
        name: str = ""
        endpoint: str = ""
        public_link: str = ""

    class Upload(BaseModel):
        bucket_dir: str = "/"
        local_original_dir: str = "Images/Original/"
        local_trans_dir: str = "Images/Transcoded/"
        trans_format: str = "webp"
        use_move: bool = False

    class Rename(BaseModel):
        post_id: str = "0001"
        img_id: str = "01"

    auth: Auth = Auth()
    bucket: Bucket = Bucket()
    upload: Upload = Upload()
    rename: Rename = Rename()
