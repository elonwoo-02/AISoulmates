from langchain_core.messages import HumanMessage
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from web.models.friend import Friend
from web.views.friend.message.chat.graph import ChatGraph


class MessageView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        friend_id = request.data.get('friend_id')
        message = request.data.get('message')
        if not message:
            return Response({
                'result': 'Please provide a message'
            })
        friends = Friend.objects.filter(pk=friend_id, me__user=request.user)
        if not friends.exists():
            return Response({
                'result': 'Please provide a friend'
            })
        friend = friends.first()
        app = ChatGraph.create_app()

        inputs = {
            'messages': [HumanMessage(message)],
        }
        res = app.invoke(inputs)
        print(res['messages'][:-1].content)

        return Response({
            'result': 'success'
        })

