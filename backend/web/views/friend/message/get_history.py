from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from web.models.friend import Friend, Message

class GetHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            last_message_id = int(request.query_params.get('last_message_id'))
            friend_id = int(request.query_params.get('friend_id'))
            queryset = Message.objects.filter(friend_id=friend_id, friend__me__user=request.user)
            if last_message_id > 0:
                queryset = queryset.filter(pk__lt=last_message_id)
            messages_raw = queryset.order_by('-id')[:10]
            messages = []
            for m in messages_raw:
                messages.append({
                    'id': m.id,
                    'user_messages': m.user_messages,
                    'output': m.output,
                })
            return Response({
                'result': 'success',
                'messages': messages,
            })
        except Friend.DoesNotExist:
            return Response({
                "error": "Friend does not exist"
            }, status=404)
