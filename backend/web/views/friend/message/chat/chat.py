import json

from langchain_core.messages import HumanMessage, AIMessage
from rest_framework.renderers import BaseRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import StreamingHttpResponse

from web.models.friend import Friend, Message
from web.views.friend.message.chat.graph import ChatGraph

class SSERenderer(BaseRenderer):
    media_type = 'text/event-stream'
    format = 'txt'
    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data

class MessageView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [SSERenderer]  # 引入渲染器
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

        # res = app.invoke(inputs)
        def event_stream():
            full_usage = {}
            full_output = ''
            for msg, metadata in app.stream(inputs, stream_mode="messages"):
                if isinstance(msg, AIMessage):
                    if msg.content:
                        yield f'data: {json.dumps({'content': msg.content}, ensure_ascii=False)}\n\n'
                        full_output += msg.content
                    if hasattr(msg, 'usage_metadata') and msg.usage_metadata:
                        full_usage = msg.usage_metadata
            yield 'data: [DONE]\n\n'
            input_tokens = full_usage.get('input_tokens', 0)
            output_tokens = full_usage.get('output_tokens', 0)
            total_tokens = full_usage.get('total_tokens', 0)
            Message.objects.create(
                friend=friend,
                user_message=message,
                input=json.dumps(
                    [m.model_dump() for m in inputs['messages']],
                    ensure_ascii=False
                )[:10000],
                output=full_output[:500],
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                total_tokens=total_tokens
            )

        response = StreamingHttpResponse(event_stream(), content_type="text/event-stream")
        response['Cache-Control'] = 'no-cache'
        return response
