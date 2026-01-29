from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from web.models.user import UserProfile


class LoginView(APIView):
    def post(self, request):
        try:
            # 1. 获取用户名和密码
            username = request.data['username'].strip()
            password = request.data['password'].strip()
            if not username or not password: # 用户名或密码为空
                return Response({'result': 'Please provide both username and password'})

            # 2. 验证用户名和密码
            user = authenticate(username=username, password=password)
            # 2.1 用户名和密码正确
            if user:
                user_profile = UserProfile.objects.get(user=user) # 对数据库的操作必须加object
                refresh = RefreshToken.for_user(user)  # 生成jwt
                response = Response({
                    'result': 'success',
                    'access': str(refresh.access_token),
                    'user_id': user.id,
                    'username': user.username,
                    'photo': user_profile.photo.url if user_profile.photo else '', # 必须加url
                    'profile': user_profile.profile,
                })
                response.set_cookie(
                    key='refresh_token',
                    value=str(refresh),
                    httponly=True,
                    samesite='Lax',
                    secure=True,
                    max_age=86400 * 7,
                )
                return response
            # 2.2 用户名和密码不正确
            return Response({'result': 'Username & password went wrong'})
        except:
            import traceback
            print(traceback.format_exc())
            return Response({"result": "System went wrong, try it later"})