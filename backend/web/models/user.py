import uuid # 用于生成唯一的文件名

from django.contrib.auth.models import User # Django内置的用户模型，包含用户名、密码、邮箱等字段，可以直接使用，不需要重新定义
from django.db import models # 用于定义数据库模型
from django.utils.timezone import now, localtime # 用于获取当前时间和将时间转换为本地时间

# 定义一个函数，用于生成上传照片的路径和文件名
# 这个函数会根据上传的文件名生成一个随机的文件名，并将其保存在user/photos/目录下
# 文件名格式为用户ID_随机文件名，例如123_a1b2c3d4e5.jpg
def photo_upload_to(instance, filename): # instance是上传的文件所在的模型实例，filename是上传的文件名
    ext = filename.split('.')[-1] # 取文件的扩展名（最后一个点的后面）
    filename = f'{uuid.uuid4().hex[:10]}.{ext}' # 取随机字符串（转化成16进制）的前十位
    return f'user/photos/{instance.user_id}_{filename}'


# 定义一个用户资料模型，包含用户的照片、简介、创建时间和更新时间等字段
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(default='user/photos/default.png', upload_to=photo_upload_to)
    profile = models.TextField(default="Thanks for your following", max_length=500) # TextField的最大长度无效
    create_time = models.DateTimeField(default=now)
    update_time = models.DateTimeField(default=now)

    # 定义一个字符串表示方法，返回用户的用户名和创建时间，格式为YYYY-MM-DD HH:MM:SS
    def __str__(self):
        return f'{self.user.username} - {localtime(self.create_time).strftime('%Y-%m-%d %H:%M:%S')}'

# 注意：需要注册到admin.py中才能在Django管理后台看到这个模型，并且需要运行makemigrations和migrate命令来创建数据库表