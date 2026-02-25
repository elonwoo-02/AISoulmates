from django.urls import path, re_path

from web.views.create.character.create import CreateCharacterView
from web.views.create.character.get_single import GetSingleCharacterView
from web.views.create.character.list import ListCharacterView
from web.views.create.character.remove import RemoveCharacterView
from web.views.create.character.update import UpdateCharacterView

from web.views.index import index

from web.views.user.account.get_user_info import GetUserInfoView
from web.views.user.account.login import LoginView
from web.views.user.account.logout import LogoutView
from web.views.user.account.refresh_token import RefreshTokenView
from web.views.user.account.register import RegisterView

from web.views.user.profile.udpate import UpdateProfileView

urlpatterns = [
    # 用户账户相关接口
    path('api/user/account/login/', LoginView.as_view()),
    path('api/user/account/logout/', LogoutView.as_view()),
    path('api/user/account/register/', RegisterView.as_view()),
    path('api/user/account/refresh_token/', RefreshTokenView.as_view()),
    path('api/user/account/get_user_info/',GetUserInfoView.as_view()),

    # 用户资料相关接口
    path('api/user/profile/update', UpdateProfileView.as_view()),

    # 角色相关接口
    path('api/create/character/create/', CreateCharacterView.as_view()),
    path('api/create/character/list/', ListCharacterView.as_view()),
    path('api/create/character/update/', UpdateCharacterView.as_view()),
    path('api/create/character/remove/', RemoveCharacterView.as_view()),
    path('api/create/character/get_single/', GetSingleCharacterView.as_view()),

    # 前端页面路由
    path('', index),
    # 兜底路由，正则式匹配不以静态文件开头的url，返回前端页面
    re_path(r'^(?!media/|static/|assets/).*$', index),
]