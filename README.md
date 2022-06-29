# Blog-Image-Uploader

博客图片转码、重命名、上传 OSS 一网打尽。

由于我的博客使用阿里云 OSS + CDN 托管图片，每次写博客如果要上传图片，都要手动转码图片、上传 OSS、复制链接。

这操作又麻烦又浪费时间，因此随手摸了个程序解决这些问题。如果你和我有一样的困扰，可以试下我这渣作。

### 所需模块

- OSS2
    - `pip install oss2`
- Pillow
    - `pip install pillow`
- PyYAML
    - `pip install PyYAML`
- pyperclip
    - `pip install pyperclip`
