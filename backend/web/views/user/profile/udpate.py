from django.contrib.auth.models import User
from django.utils.timezone import now
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from web.models.user import UserProfile


class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request) :
        try:
            # 1. 用户信息准备
            # 1.1 获取发出请求的用户
            user = request.user
            # 1.2 获取用户请求更新的信息
            username = request.data.get('username').strip()
            profile = request.data.get('profile').strip()[:500]
            photo = request.FILES.get('photo', None)
            # 1.3 通过user取得用户资料
            user_profile = UserProfile.objects.get(user=user)

            # 2. 处理敏感操作（不能相信）
            # 2.1 用户名和个人简洁不能为空
            if not username:
                return Response({
                    'result':'username is required',
                })
            if not profile:
                return Response({
                    'result':'profile is required',
                })
            # 2.2 不能改为其它人的用户名
            if username != user.username and User.objects.filter(username=username).exists():
                return Response({
                    'result':'username is taken',
                })

            # 3. 更新并保存更新的用户信息
            if photo:   # 头像需要先删除原头像再更新
                # remove_old_photo(user_profile.photo)    # todo: 不删除旧头像是否可行，方便用户撤回
                user_profile.photo = photo

            user_profile.profile = profile
            user_profile.update_time = now()    # 只修改更新时间，不修改创建时间
            user_profile.save()

            user.username = username
            user.save()

            # 4. 返回更新结果
            return Response({
                'result':'success',
                'user_id':user.id,
                'username':user.username,
                'profile':user_profile.profile,
                'photo':user_profile.photo.url,
            })
        except:
            return Response({
                'result':'system error',
            })