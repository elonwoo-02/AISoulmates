from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.timezone import localtime

from web.models.friend import Message

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
                    'user_message': m.user_message,
                    'output': m.output,
                    'created_at': localtime(m.create_time).isoformat(),
                })
            return Response({
                'result': 'success',
                'messages': messages,
            })
        except Exception as e:
            return Response({
                "error": "An error occurred while fetching message history."
            })
