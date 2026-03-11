import asyncio
import json
import os
import uuid

import websockets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class STTView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        audio = request.FILES.get('audio')
        if not audio:
            return Response({"result": "No audio file provided"})
        pcm_data = audio.read()
        text = asyncio.run(self.run_stt_tasks(pcm_data))
        return Response({
            'result': 'success',
            'text': text,
        })


    async def stt_sender(self, pcm_data, ws, task_id):
        chunk = 3200
        for i in range(0, len(pcm_data), chunk):
            await ws.send(pcm_data[i:i + chunk])
            await asyncio.sleep(0.01)
        await ws.send(json.dumps({
            "header": {
                "action": "finish-task",
                "task_id": task_id,
                "streaming": "duplex"
            },
            "payload": {
                "input": {}
            }
        }))

    async def stt_receiver(self, ws):
        text = ''
        async for msg in ws:
            data = json.loads(msg)
            event = data['header']['event']
            if event == 'result-generated':
                output = data['payload']['output']
                if output.get('transcription', None) and output['transcription']['sentence_end']:
                    text = output['transcription']['text']
                elif event in ['task-finished', 'task-failed']:
                    break
        return text

    async def run_stt_tasks(self, pcm_data):
        task_id = uuid.uuid4().hex
        api_key = os.getenv('API_KEY')
        wss_url = os.getenv('WSS_URL')
        headers = {
            'Authorization': f'Bearer {api_key}',
        }
        async with websockets.connect(wss_url, additional_headers=headers) as ws:
            await ws.send(json.dumps({
                "header": {
                    "streaming": "duplex",
                    "task_id": task_id,
                    "action": "run-task"
                },
                "payload": {
                    "model": "gummy-realtime-v1",
                    "parameters": {
                        "sample_rate": 16000,
                        "format": "pcm",
                        "transcription_enabled": True,
                    },
                    "input": {},
                    "task": "asr",
                    "task_group": "audio",
                    "function": "recognition"
                }
            }))
            async for msg in ws:
                if json.load(msg)['header']['event'] == 'task-started':
                    break

            _, text = await asyncio.gather(
                self.stt_sender(pcm_data, ws, task_id),
                self.stt_receiver(ws),
            )
            return text