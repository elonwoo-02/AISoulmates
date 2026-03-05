import os
from typing import TypedDict, Annotated, Sequence

from django.utils.timezone import localtime, now
from langchain_core.messages import BaseMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.constants import END, START
from langgraph.graph import add_messages, StateGraph
from langgraph.prebuilt import ToolNode


class ChatGraph:
    @staticmethod
    def create_app():
        @tool
        def get_time() -> str:
            """当需要查询精确时间时，调用此函数。返回格式为：[年-月-日 时:分:秒]"""
            return localtime(now()).strftime('%Y-%m-%d %H:%M:%S')

        tools = [get_time]

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
        ).bind_tools(tools)

        # 定义 Agent 状态，包含消息历史
        class AgentState(TypedDict):
            messages: Annotated[Sequence[BaseMessage], add_messages]

        # LLM 调用函数，处理输入消息并返回模型响应
        def model_call(state: AgentState) -> AgentState:
            res = llm.invoke(state['messages'])
            return {'messages': [res]}

        def should_continue(state: AgentState) -> str:
            last_message = state['messages'][-1]
            if last_message.tool_calls:
                return "tools"
            return "end"

        tool_node = ToolNode(tools)

        graph = StateGraph(AgentState)
        graph.add_node('agent', model_call)
        graph.add_node('tools', tool_node)

        graph.add_edge(START, 'agent')
        graph.add_edge('agent', END)
        graph.add_conditional_edges(
            'agent',
            should_continue,
            {
                'tools': 'tools',
                'end': END,
            }
        )
        graph.add_edge('tools', 'agent')

        return graph.compile()
