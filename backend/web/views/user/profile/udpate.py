from django.contrib.auth.models import User
from django.utils.timezone import now
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from web.models.user import UserProfile


class UpdateProfileView(APIView):
    """
    API 接口：更新用户资料
    ----------------------
    URL: /api/user/profile/update
    方法: POST
    权限: 登录用户（IsAuthenticated）

    请求参数:
        - username (str): 新用户名
        - profile (str): 个人简介（最多500字符）
        - photo (file, optional): 新头像图片文件

    返回结果:
        - 成功:
            {
                'result': 'success',
                'user_id': <int>,
                'username': <str>,
                'profile': <str>,
                'photo': <str, url>
            }
        - 失败:
            {
                'result': <错误信息>
            }
    """

    # -------------------- 权限控制 --------------------
    permission_classes = [IsAuthenticated]  # 仅允许登录用户访问

    def post(self, request):
        """
        处理 POST 请求，更新当前登录用户的资料
        """
        try:
            # -------------------- 1. 用户信息准备 --------------------
            user = request.user  # 当前请求的用户（通过认证系统获取）

            # 获取用户提交的数据
            username = request.data.get('username', '').strip()  # 新用户名
            profile = request.data.get('profile', '').strip()[:500]  # 个人简介（截断500字符）
            photo = request.FILES.get('photo', None)  # 上传头像（可选）

            # 通过user获取用户资料对象（UserProfile）
            user_profile = UserProfile.objects.get(user=user)

            # -------------------- 2. 验证用户输入 --------------------
            # 2.1 用户名不能为空
            if not username:
                return Response({'result': 'username is required'})

            # 2.2 个人简介不能为空
            if not profile:
                return Response({'result': 'profile is required'})

            # 2.3 用户名唯一性检查
            # 如果用户名改变了，且新用户名已存在，返回错误
            if username != user.username and User.objects.filter(username=username).exists():
                return Response({'result': 'username is taken'})

            # -------------------- 3. 更新用户信息 --------------------
            if photo:
                # 头像更新
                # todo: 这里可以先删除旧头像，也可以保留原图（方便用户撤回）
                # remove_old_photo(user_profile.photo)
                user_profile.photo = photo

            # 更新个人简介
            user_profile.profile = profile
            # 更新资料更新时间
            user_profile.update_time = now()  # 只更新时间，不修改创建时间
            user_profile.save()

            # 更新用户名（User 模型）
            user.username = username
            user.save()

            # -------------------- 4. 返回结果 --------------------
            return Response({
                'result': 'success',
                'user_id': user.id,
                'username': user.username,
                'profile': user_profile.profile,
                'photo': user_profile.photo.url if user_profile.photo else '',
            })

        except UserProfile.DoesNotExist:
            # 用户资料不存在
            return Response({'result': 'user profile not found'})

        except Exception as e:
            # 捕获其他异常
            # 可在调试阶段打印 e
            # print(e)
            return Response({'result': 'system error'})
