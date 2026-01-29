from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from web.services.agent_service import agent_instance

class AgentChatView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        message = request.data.get('message')
        if not message:
            return Response({"error": "Message is required"}, status=400)
        
        username = request.user.username
        try:
            reply = agent_instance.ask(message, username)
            return Response({"reply": reply})
        except Exception as e:
            return Response({"error": str(e)}, status=500)
