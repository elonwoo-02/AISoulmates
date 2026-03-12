import asyncio
import json
import os
import uuid

import websockets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from web.views.utils.ai_config import resolve_model_config

class STTView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        """处理语音转文本的POST请求"""
        # 1. 从请求中获取音频文件
        audio = request.FILES.get('audio')
        if not audio:
            return Response({"result": "No audio file provided"})
        # 2. 读取音频文件的二进制数据
        pcm_data = audio.read()
        # 3. 运用协程，异步调用STT服务进行语音转文本
        text = asyncio.run(self.run_stt_tasks(pcm_data))
        # 4. 返回转换后的文本
        return Response({
            'result': 'success',
            'text': text,  # 返回转换成功的文本
        })


    async def stt_sender(self, pcm_data, ws, task_id):
        """
        发送音频数据到STT服务
        
        参数:
            pcm_data: PCM格式的音频数据
            ws: WebSocket连接对象
            task_id: 任务ID
        """
        chunk = 3200  # 每次发送的音频数据块大小
        for i in range(0, len(pcm_data), chunk):
            await ws.send(pcm_data[i:i + chunk])  # 分块发送音频数据
            await asyncio.sleep(0.01)  # 短暂延迟以避免拥塞
        # 发送任务结束信号
        await ws.send(json.dumps({
            "header": {
                "action": "finish-task",  # 动作类型：结束任务
                "task_id": task_id,  # 任务ID
                "streaming": "duplex"  # 双工流模式
            },
            "payload": {
                "input": {}  # 空输入表示结束
            }
        }))

    async def stt_receiver(self, ws):
        """
        接收STT服务返回的文本结果
        
        参数:
            ws: WebSocket连接对象
            
        返回:
            str: 转换后的文本
        """
        text = ''  # 初始化返回文本
        async for msg in ws:  # 持续监听WebSocket消息
            data = json.loads(msg)  # 解析JSON格式的消息
            event = data['header']['event']  # 获取事件类型
            if event in ['task-finished', 'task-failed']:  # 如果任务结束或失败
                break  # 退出循环
            if event == 'result-generated':  # 如果是结果生成事件
                output = data['payload']['output']  # 获取输出内容
                transcription = output.get('transcription')
                if transcription:
                    # 先记录最新文本，避免没有 sentence_end 导致最终为空
                    text = transcription.get('text', text)
                    # 如果检测到句子结束，可提前结束接收
                    if transcription.get('sentence_end'):
                        break
        return text  # 返回最终文本

    async def run_stt_tasks(self, pcm_data):
        """
        运行STT任务
        
        参数:
            pcm_data: PCM格式的音频数据
            
        返回:
            str: 转换后的文本
        """
        task_id = uuid.uuid4().hex  # 生成唯一任务ID
        api_key = os.getenv('API_KEY')  # 从环境变量获取API密钥
        wss_url = os.getenv('WSS_URL')  # 从环境变量获取WebSocket URL
        model_config = resolve_model_config()
        headers = {
            'Authorization': f'Bearer {api_key}',  # 设置认证头
        }
        # 建立WebSocket连接
        async with websockets.connect(wss_url, additional_headers=headers) as ws:
            # 发送任务启动消息
            await ws.send(json.dumps({
                "header": {
                    "streaming": "duplex",  # 双工通信模式
                    "task_id": task_id,  # 任务ID
                    "action": "run-task"  # 运行动作
                },
                "payload": {
                    "model": model_config['stt_model'],  # 使用的模型
                    "parameters": {
                        "sample_rate": 16000,  # 采样率
                        "format": "pcm",  # 音频格式
                        "transcription_enabled": True,  # 启用转录
                    },
                    "input": {},  # 初始输入为空
                    "task": "asr",  # 任务类型:自动语音识别
                    "task_group": "audio",  # 任务组:音频
                    "function": "recognition"  # 功能:识别
                }
            }))
            # 等待任务开始确认
            async for msg in ws:
                if json.loads(msg)['header']['event'] == 'task-started':
                    break

            # 并行运行发送和接收任务
            _, text = await asyncio.gather(
                self.stt_sender(pcm_data, ws, task_id),  # 发送音频数据
                self.stt_receiver(ws),  # 接收识别结果
            )
            return text
