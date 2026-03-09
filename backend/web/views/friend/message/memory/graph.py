from typing import TypedDict, Annotated, Sequence

from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI
from langgraph.constants import START, END
from langgraph.graph import add_messages, StateGraph

from web.views.utils.ai_config import resolve_ai_config


class MemoryGraph:
    @staticmethod
    def create_app(user_profile):
        config = resolve_ai_config(user_profile)
        llm = ChatOpenAI(
            model='qwen3.5-flash',
            openai_api_key=config['api_key'],
            openai_api_base=config['api_base'],
            streaming=True,
            model_kwargs={
                "stream_options": {
                    "include_usage": True,  # 输出使用多少token
                }
            }
        )

        class AgentState(TypedDict):
            messages: Annotated[Sequence[BaseMessage], add_messages]

        def model_call(state: AgentState) -> AgentState:
            res = llm.invoke(state['messages'])
            return {'messages': [res]}

        graph = StateGraph(AgentState)
        graph.add_node('agent', model_call)

        graph.add_edge(START, 'agent')
        graph.add_edge('agent', END)

        return graph.compile()
