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
    """SSE 流式响应渲染器"""
    media_type = 'text/event-stream'
    format = 'txt'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data

class MessageView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [SSERenderer]  # 引入渲染器

    def post(self, request):
        """
        处理聊天消息请求

        参数:
            request: DRF 请求对象，包含用户信息和请求数据

        返回:
            StreamingHttpResponse: SSE 流式响应
        """
        friend = self._validate_request(request)  # 验证请求并获取好友对象
        if isinstance(friend, Response):
            return friend  # 验证失败，返回错误响应

        app = self._create_chat_app()  # 创建聊天应用
        inputs = {
            'messages': [HumanMessage(request.data.get('message'))],  # 构建输入消息
        }

        def event_stream():
            gen = self._stream_chat_response(app, inputs)  # 获取流式响应生成器
            try:
                while True:
                    chunk = next(gen)  # 获取下一个响应块
                    yield chunk  # 输出SSE事件
            except StopIteration as e:
                full_output, full_usage = e.value  # 获取完整输出和使用量
                self._save_message(friend, request.data.get('message'), inputs, full_output, full_usage)  # 保存消息到数据库

        response = StreamingHttpResponse(event_stream(), content_type="text/event-stream")  # 创建SSE响应
        response['Cache-Control'] = 'no-cache'  # 禁用缓存
        return response

    def _validate_request(self, request):
        """
        验证请求参数

        参数:
            request: DRF 请求对象

        返回:
            Friend: 验证通过时返回好友对象
            Response: 验证失败时返回错误响应
        """
        message = request.data.get('message')
        if not message:
            return Response({
                'result': 'Please provide a message'
            })
        friend_id = request.data.get('friend_id')
        friends = Friend.objects.filter(pk=friend_id, me__user=request.user)
        if not friends.exists():
            return Response({
                'result': 'Please provide a friend'
            })
        return friends.first()

    def _create_chat_app(self):
        """
        创建聊天应用实例

        参数:
            无

        返回:
            ChatGraph 应用实例
        """
        return ChatGraph.create_app()

    def _stream_chat_response(self, app, inputs):
        """
        流式处理聊天响应

        参数:
            app: ChatGraph 应用实例
            inputs: 包含消息的输入字典

        返回:
            tuple: (完整输出字符串, 使用元数据字典)
        """
        full_usage = {}
        full_output = ''
        for msg, metadata in app.stream(inputs, stream_mode="messages"):
            if isinstance(msg, AIMessage):
                if msg.content:
                    yield f'data: {json.dumps({"content": msg.content}, ensure_ascii=False)}\n\n'
                    full_output += msg.content
                if hasattr(msg, 'usage_metadata') and msg.usage_metadata:
                    full_usage = msg.usage_metadata
        yield 'data: [DONE]\n\n'
        # 返回值通过生成器的 StopIteration 获取
        return full_output, full_usage

    def _save_message(self, friend, message, inputs, full_output, full_usage):
        """
        保存聊天消息到数据库

        参数:
            friend: Friend 实例
            message: 用户发送的消息
            inputs: 输入消息字典
            full_output: AI 完整响应
            full_usage: token 使用元数据

        返回:
            Message: 创建的消息实例
        """
        # 从元数据中提取 token 使用量
        input_tokens = full_usage.get('input_tokens', 0)
        output_tokens = full_usage.get('output_tokens', 0)
        total_tokens = full_usage.get('total_tokens', 0)
        # 创建并保存消息记录
        return Message.objects.create(
            friend=friend,
            user_message=message,
            # 将消息列表序列化为 JSON 字符串，截取前 10000 字符
            input=json.dumps(
                [m.model_dump() for m in inputs['messages']],
                ensure_ascii=False
            )[:10000],
            # 截取 AI 输出前 500 字符
            output=full_output[:500],
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens
        )
