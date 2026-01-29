from django.contrib import admin
from web.models.user import UserProfile

# Register your models here.

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',) # 逗号不要删，加逗号传入的就是列表