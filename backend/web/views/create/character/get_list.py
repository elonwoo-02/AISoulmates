from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView

from web.models.character import Character
from web.models.user import UserProfile


class GetListCharacterView(APIView):
    def get(self, request):
        try:
            items_count = int(request.GET.get("items_count"))
            user_id = int(request.query_params.get("user_id"))
            user = User.objects.get(id=user_id)
            user_profile = UserProfile.objects.get(user=user)
            character_raw = Character.objects.filter(
                author=user_profile
            ).order_by("-id")[items_count: items_count + 20]
            characters = []
            for character in character_raw:
                author = character.author
                characters.append({
                    "id": character.id,
                    "name": character.name,
                    "profile": character.profile,
                    "photo": character.photo.url,
                    'background_image': character.background_image.url if character.background_image else None,
                    'author': {
                        "user_id": author.user.id,
                        "username": author.user.username,
                        "photo": author.photo.url
                    },
                })
            return Response({
                "result": "success",
                "user_profile": {
                    "user_id": user.id,
                    "username": user.username,
                    "profile": user_profile.profile,
                    "photo": user_profile.photo.url,
                },
                "characters": characters
            })
        except:
            return Response({
                "result": "An error occurred while retrieving the character list."
            })

# 测试：访问http://127.0.0.1:8000/api/create/character/get_list/?items_count=0&user_id=1
# 结果：返回用户1的角色列表，包含角色的id、name、profile、photo、background_image和作者信息（user_id、username、photo）。如果发生错误，返回错误信息。