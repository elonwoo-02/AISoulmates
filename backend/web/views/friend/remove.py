from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from web.models.friend import Friend


class RemoveFriendView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            friend_id = request.data['friend_id']
            Friend.objects.filter(id=friend_id, me__user=request.user).delete()
            return Response({
                'result': 'success'
            })
        except:
            return Response({
                'result': 'failed'
            })