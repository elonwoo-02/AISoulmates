import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now, localtime


def photo_upload_to(instance, filename):
    ext = filename.split('.')[-1] # 取文件的扩展名（最后一个点的后面）
    filename = f'{uuid.uuid4().hex[:10]}.{ext}' # 取随机字符串（转化成16进制）的前十位
    return f'user/photos/{instance.user_id}_{filename}'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(default='user/photos/default.jpg', upload_to=photo_upload_to)
    profile = models.TextField(default="Thanks for your following", max_length=500)
    create_time = models.DateTimeField(default=now)
    update_time = models.DateTimeField(default=now)

    def __str__(self):
        return f'{self.user.username} - {localtime(self.create_time).strftime('%Y-%m-%d %H:%M:%S')}'
