from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from web.models.character import Character

# 角色删除接口
class RemoveCharacterView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            character_id = request.data['character_id']
            Character.objects.filter(id=character_id, author__user=request.user).delete()
            return Response({
                "result": "Character removed successfully."
            })
        except:
            return Response({
                "result": "An error occurred while removing the character."
            })