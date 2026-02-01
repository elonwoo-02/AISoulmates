import dotenv
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
import os

class ChatView(APIView):
    permission_classes = [IsAuthenticated]

    dotenv.load_dotenv()
    os.environ['OPENAI_BASE_URL'] = os.getenv("OPENAI_BASE_URL")
    os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")

    def post(self, request):
        user_message = request.data.get('message')
        history_data = request.data.get('history', [])

        if not user_message:
            return Response({"error": "Message is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 初始化模型，LangChain 会自动读取 OPENAI_API_KEY 环境变量
            llm = ChatOpenAI(
                model="gpt-5-nano-2025-08-07",
                temperature=0.7,
            )

            # 构建提示词模板，包含系统角色和历史记录占位符
            prompt = ChatPromptTemplate.from_messages([
                ("system",
                 "你是一个专业的 AI 助手。请尽可能使用 Markdown 格式（如标题、列表、加粗、表格、代码块）来组织你的回答，使内容清晰易读。"),
                MessagesPlaceholder(variable_name="history"),
                ("human", "{input}"),
            ])

            # 转换历史记录格式为 LangChain 消息对象
            history = []
            for msg in history_data:
                if msg['role'] == 'user':
                    history.append(HumanMessage(content=msg['content']))
                elif msg['role'] == 'assistant':
                    history.append(AIMessage(content=msg['content']))

            # 构建链并调用
            chain = prompt | llm
            response = chain.invoke({
                "input": user_message,
                "history": history
            })

            return Response({
                "reply": response.content,
                "status": "success"
            })


        except Exception as e:

            # 关键修改：在终端打印出完整的错误堆栈

            import traceback

            print("======= AI CHAT ERROR START =======")

            traceback.print_exc()

            print("======= AI CHAT ERROR END   =======")

            return Response({

                "error": str(e),

                "status": "error"

            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
