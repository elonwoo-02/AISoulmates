from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from web.models.character import Character
from web.views.utils.photo import remove_old_photo


# 角色删除接口，删除角色时会删除角色的头像和背景图
class RemoveCharacterView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            character_id = request.data['character_id']
            character = Character.objects.get(id=character_id, author__user=request.user)
            remove_old_photo(character.photo)
            remove_old_photo(character.background_image)
            character.delete()
            return Response({
                "result": "success"
            })
        except:
            return Response({
                "result": "An error occurred while removing the character."
            })