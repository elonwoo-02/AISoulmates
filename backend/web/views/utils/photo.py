import os

from django.conf import settings


def remove_old_photo(photo):
    # 默认头像不需要修改
    if photo and photo.name == 'user/photos/default.png':
        return
    if photo and photo.name == 'user/background_images/default.png':
        return
    # 否则，删除原头像
    old_path = settings.MEDIA_ROOT / photo.name # 头像路径：用户上传文件的默认根目录 / 头像名
    if os.path.exists(old_path):
        os.remove(old_path)