import os
from typing import TypedDict, Annotated, Sequence

from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI
from langgraph.constants import END, START
from langgraph.graph import add_messages, StateGraph

class ChatGraph:
    @staticmethod
    def create_app():
        # 初始化 ChatOpenAI 模型，支持流式输出
        llm = ChatOpenAI(
            model = 'gpt-4o-mini-search-preview',
            openai_api_key = os.getenv('API_KEY'),
            openai_api_base = os.getenv('API_BASE'),
            streaming=True,
            model_kwargs={
                "stream_options": {
                    "include_usage": True,  # 输出使用多少token
                }
            }
        )

        # 定义 Agent 状态，包含消息历史
        class AgentState(TypedDict):
            messages: Annotated[Sequence[BaseMessage], add_messages]

        # LLM 调用函数，处理输入消息并返回模型响应
        def model_call(state: AgentState) -> AgentState:
            res = llm.invoke(state['messages'])
            return {'messages': [res]}

        # 构建状态图：添加节点、设置边、编译返回
        graph = StateGraph(AgentState)
        graph.add_node('agent', model_call)

        graph.add_edge(START, 'agent')
        graph.add_edge('agent', END)

        return graph.compile()
