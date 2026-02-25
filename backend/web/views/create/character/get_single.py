from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from web.models.character import Character

# 角色单个查询接口
class GetSingleCharacterView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            character_id = request.query_params['character_id']
            character = Character.objects.get(id=character_id, author__user=request.user)
            return Response({
                "result": "Character retrieved successfully.",
                "character": {
                    "id": character.id,
                    "name": character.name,
                    "profile": character.profile,
                    "photo": character.photo.url,
                    "background_image": character.background_image.url if character.background_image else None,
                }
            })
        except:
            return Response({
                "result": "An error occurred while retrieving the character."
            })