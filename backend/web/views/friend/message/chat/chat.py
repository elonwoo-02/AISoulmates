"""
AI好友实时聊天API视图

本模块提供:
- SSE (Server-Sent Events) 流式传输聊天响应
- 集成TTS (Text-to-Speech) 语音合成服务
- 消息历史记录和记忆管理功能
"""
import asyncio
import base64
import json
import os
import threading
import uuid
from queue import Queue

import websockets
from django.http import StreamingHttpResponse
from langchain_core.messages import HumanMessage, BaseMessageChunk, SystemMessage, AIMessage
from rest_framework.renderers import BaseRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from web.models.friend import Friend, Message, SystemPrompt
from web.views.friend.message.chat.graph import ChatGraph
from web.views.utils.ai_config import resolve_model_config
from web.views.friend.message.memory.update import update_memory


class SSERenderer(BaseRenderer):
    """SSE响应渲染器 - 用于处理服务器发送事件(Server-Sent Events)的响应格式"""
    media_type = 'text/event-stream'
    format = 'txt'
    def render(self, data, accepted_media_type=None, renderer_context=None):
        """渲染SSE响应数据"""
        return data

# todo: 参考龙虾的设计，增加系统的prompt，支持文件上传
def add_system_prompt(state, friend):
    """
    添加系统提示词到消息状态中
    
    参数:
        state: 当前消息状态字典
        friend: 好友对象
    
    返回:
        包含系统提示词的新消息状态
    """
    msgs = state['messages']
    # 获取系统预设的提示词
    system_prompts = SystemPrompt.objects.filter(title='回复').order_by('order_number')
    prompt = ''
    for sp in system_prompts:
        prompt += sp.prompt
    # 添加角色性格和长期记忆
    prompt += f'\n【角色性格】\n{friend.character.profile}\n'
    prompt += f'【长期记忆】\n{friend.memory}\n'
    return {'messages': [SystemMessage(prompt)] + msgs}


def add_recent_messages(state, friend):
    """
    添加最近的聊天记录到消息状态中
    
    参数:
        state: 当前消息状态字典
        friend: 好友对象
    
    返回:
        包含最近聊天记录的新消息状态
    """
    msgs = state['messages']
    # 获取最近的10条消息记录(按时间倒序)
    message_raw = list(Message.objects.filter(friend=friend).order_by('-id')[:10])
    message_raw.reverse()  # 反转顺序为时间正序
    messages = []
    # 将消息转换为HumanMessage和AIMessage格式
    for m in message_raw:
        messages.append(HumanMessage(m.user_message))
        messages.append(AIMessage(m.output))
    # 保留原始消息的第一条和最后一条
    return {'messages': msgs[:1] + messages + msgs[-1:]}


class MessageChatView(APIView):
    """
    消息聊天视图 - 处理与AI好友的实时聊天交互
    
    功能:
    - 处理用户发送的消息
    - 生成AI回复
    - 通过SSE流式传输响应
    """
    permission_classes = [IsAuthenticated]  # 需要认证用户
    renderer_classes = [SSERenderer]  # 使用SSE渲染器
    
    def post(self, request):
        """
        处理POST请求 - 用户发送聊天消息
        
        参数:
            request: 包含好友ID和消息内容的请求对象
        
        返回:
            StreamingHttpResponse: SSE流式响应
        """
        # 获取请求参数
        friend_id = request.data['friend_id']
        message = request.data['message'].strip()
        
        # 验证消息内容
        if not message:
            return Response({
                'result': '消息不能为空'
            })
            
        # 验证好友关系
        friends = Friend.objects.filter(pk=friend_id, me__user=request.user)
        if not friends.exists():
            return Response({
                'result': '好友不存在'
            })
            
        friend = friends.first()
        app = ChatGraph.create_app()  # 创建聊天应用

        # 构建输入消息
        inputs = {
            'messages': [HumanMessage(message)]
        }
        # 添加系统提示和最近消息
        inputs = add_system_prompt(inputs, friend)
        inputs = add_recent_messages(inputs, friend)

        # 返回SSE流式响应
        response = StreamingHttpResponse(
            self.event_stream(app, inputs, friend, message),
            content_type='text/event-stream',
        )
        response['Cache-Control'] = 'no-cache'
        response['X-Accel-Buffering'] = 'no'
        return response


    async def tts_sender(self, app, inputs, mq, ws, task_id):
        """
        TTS发送器 - 将AI生成的文本消息发送到TTS服务
        
        参数:
            app: 聊天应用实例
            inputs: 输入消息
            mq: 消息队列
            ws: WebSocket连接
            task_id: 任务ID
        """
        # 流式处理AI生成的回复消息
        async for msg, metadata in app.astream(inputs, stream_mode="messages"):
            if isinstance(msg, BaseMessageChunk):
                if msg.content:
                    # 发送文本到TTS服务
                    await ws.send(json.dumps({
                        "header": {
                            "action": "continue-task",
                            "task_id": task_id,  # 随机uuid
                            "streaming": "duplex"
                        },
                        "payload": {
                            "input": {
                                "text": msg.content,
                            }
                        }
                    }))
                    # 将消息内容放入队列
                    mq.put_nowait({'content': msg.content})
                # 记录token使用情况
                if hasattr(msg, 'usage_metadata') and msg.usage_metadata:
                    mq.put_nowait({'usage': msg.usage_metadata})
                    
        # 发送任务完成通知
        await ws.send(json.dumps({
            "header": {
                "action": "finish-task",
                "task_id": task_id,
                "streaming": "duplex"
            },
            "payload": {
                "input": {}  # input不能省去，否则会报错
            }
        }))


    async def tts_receiver(self, mq, ws):
        """
        TTS接收器 - 接收TTS服务返回的音频数据
        
        参数:
            mq: 消息队列
            ws: WebSocket连接
        """
        async for msg in ws:
            if isinstance(msg, bytes):
                # 处理二进制音频数据
                audio = base64.b64encode(msg).decode('utf-8')
                mq.put_nowait({'audio': audio})
            else:
                # 处理JSON格式的消息
                data = json.loads(msg)
                event = data['header']['event']
                # 任务完成或失败时退出循环
                if event in ['task-finished', 'task-failed']:
                    break


    async def run_tts_tasks(self, app, inputs, mq):
        """
        运行TTS任务 - 管理TTS服务的整个生命周期
        
        参数:
            app: 聊天应用实例
            inputs: 输入消息
            mq: 消息队列
        """
        # 生成唯一任务ID
        task_id = uuid.uuid4().hex
        # 获取API配置
        api_key = os.getenv('API_KEY')
        wss_url = os.getenv('WSS_URL')
        model_config = resolve_model_config()
        headers = {
            "Authorization": f"Bearer {api_key}"
        }
        
        # 建立WebSocket连接
        async with websockets.connect(wss_url, additional_headers=headers) as ws:
            # 发送TTS任务请求
            await ws.send(json.dumps({
                "header": {
                    "action": "run-task",
                    "task_id": task_id,  # 随机uuid
                    "streaming": "duplex"
                },
                "payload": {
                    "task_group": "audio",
                    "task": "tts",
                    "function": "SpeechSynthesizer",
                    "model": model_config['tts_model'],
                    "parameters": {
                        "text_type": "PlainText",
                        "voice": "longanyang",  # 音色
                        "format": "mp3",  # 音频格式
                        "sample_rate": 22050,  # 采样率
                        "volume": 50,  # 音量
                        "rate": 1.25,  # 语速
                        "pitch": 1  # 音调
                    },
                    "input": {  # input不能省去，不然会报错
                    }
                }
            }))
            
            # 等待任务启动
            async for msg in ws:
                if json.loads(msg)['header']['event'] == 'task-started':
                    break
                    
            # 并行运行发送器和接收器
            await asyncio.gather(
                self.tts_sender(app, inputs, mq, ws, task_id),
                self.tts_receiver(mq, ws),
            )


    def work(self, app, inputs, mq):
        """
        工作线程 - 在单独线程中运行TTS任务
        
        参数:
            app: 聊天应用实例
            inputs: 输入消息
            mq: 消息队列
        """
        try:
            # 运行TTS任务
            asyncio.run(self.run_tts_tasks(app, inputs, mq))
        finally:
            # 确保任务结束时发送None到队列
            mq.put_nowait(None)


    def event_stream(self, app, inputs, friend, message):
        """
        事件流生成器 - 生成SSE格式的聊天响应
        
        参数:
            app: 聊天应用实例
            inputs: 输入消息
            friend: 好友对象
            message: 用户原始消息
        
        返回:
            生成器，产生SSE格式的事件数据
        """
        # 创建消息队列和工作线程
        mq = Queue()
        thread = threading.Thread(target=self.work, args=(app, inputs, mq))
        thread.start()

        # 初始化完整输出和token使用记录
        full_output = ''
        full_usage = {}
        
        # 处理消息队列中的事件
        while True:
            msg = mq.get()
            if not msg:
                break
                
            # 处理文本内容消息
            if msg.get('content', None):
                full_output += msg['content']
                yield f'data: {json.dumps({'content': msg['content']}, ensure_ascii=False)}\n\n'
                
            # 处理音频消息
            if msg.get('audio', None):
                yield f'data: {json.dumps({'audio': msg['audio']}, ensure_ascii=False)}\n\n'
                
            # 记录token使用情况
            if msg.get('usage', None):
                full_usage = msg['usage']

        # 发送流结束标志
        yield 'data: [DONE]\n\n'
        
        # 提取token使用统计
        input_tokens = full_usage.get('input_tokens', 0)
        output_tokens = full_usage.get('output_tokens', 0)
        total_tokens = full_usage.get('total_tokens', 0)
        
        # 保存聊天记录到数据库
        Message.objects.create(
            friend=friend,
            user_message=message[:500],
            input=json.dumps(
                [m.model_dump() for m in inputs['messages']],
                ensure_ascii=False,
            )[:10000],
            output=full_output[:500],
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
        )
        
        # 定期更新好友记忆
        if Message.objects.filter(friend=friend).count() % 1 == 0:
            update_memory(friend)
