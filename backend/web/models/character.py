import uuid

from django.db import models
from django.utils.timezone import now, localtime

from web.models.user import UserProfile

def photo_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4().hex[:10]}.{ext}'
    return f'character/photos/{instance.author.user_id}_{filename}'

def background_image_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4().hex[:10]}.{ext}'
    return f'character/background_images/{instance.author.user_id}_{filename}'

class Character(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to=photo_upload_to)
    profile = models.TextField(max_length=100000)
    background_image = models.ImageField(upload_to=background_image_upload_to, blank=True, null=True) # 背景图片可以为空
    create_time = models.DateTimeField(default=now)
    update_time = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.author.user.username} - {self.name} - {localtime(self.create_time).strftime('%Y-%m-%d %H:%M:%S')}"