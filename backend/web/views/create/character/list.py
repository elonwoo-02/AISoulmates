from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from web.models.character import Character

# 角色列表查询接口
class ListCharacterView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            characters = Character.objects.filter(author__user=request.user).order_by('-update_time')
            character_list = []
            for character in characters:
                character_list.append({
                    "id": character.id,
                    "name": character.name,
                    "profile": character.profile[:100] + "..." if len(character.profile) > 100 else character.profile,
                    "photo": character.photo.url,
                    "background_image": character.background_image.url if character.background_image else None,
                    "create_time": character.create_time.isoformat(),
                    "update_time": character.update_time.isoformat(),
                })
            return Response({
                "result": "success",
                "characters": character_list
            })
        except:
            return Response({
                "result": "An error occurred while retrieving the character list."
            })
