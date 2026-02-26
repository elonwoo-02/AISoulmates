from django.contrib import admin

from web.models.character import Character
from web.models.friend import Friend
from web.models.user import UserProfile

# Register your models here.

# 使用装饰器注册模型，并指定admin.ModelAdmin类来定制管理界面
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',) # 逗号不要删，加逗号传入的就是列表，不加逗号传入的就是字符串，导致报错

@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    raw_id_fields = ('author',)

@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    raw_id_fields = ('me', 'character',)
