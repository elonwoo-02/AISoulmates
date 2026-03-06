import os
from pathlib import Path
from typing import TypedDict, Annotated, Sequence

import lancedb
from django.conf import settings
from django.utils.timezone import localtime, now
from langchain_community.vectorstores import LanceDB
from langchain_core.messages import BaseMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.constants import START, END
from langgraph.graph import add_messages, StateGraph
from langgraph.prebuilt import ToolNode

from web.documents.utils.custom_embeddings import CustomEmbeddings


class AgentState(TypedDict):
    """Agent 状态定义"""
    messages: Annotated[Sequence[BaseMessage], add_messages]  # 消息历史，add_messages 自动处理消息追加


class ChatGraph:
    """聊天图构建器，使用缓存优化性能"""

    _vector_db_cache: LanceDB | None = None  # 向量数据库连接缓存，避免重复初始化
    _app_cache = None  # 编译后的图实例缓存，提升重复调用性能

    @staticmethod
    def _create_tools() -> list:
        """创建并返回工具列表"""
        get_time = ChatGraph._create_get_time_tool()  # 时间查询工具
        search_knowledge_base = ChatGraph._create_search_knowledge_base_tool()  # 知识库搜索工具
        return [get_time, search_knowledge_base]

    @staticmethod
    def _create_get_time_tool():
        """创建获取时间的工具"""
        @tool  # 使用 @tool 装饰器将函数注册为 LangChain 工具
        def get_time() -> str:
            """当需要查询精确时间时，调用此函数。返回格式为：[年-月-日 时:分:秒]"""
            return localtime(now()).strftime('%Y-%m-%d %H:%M:%S')  # 返回本地时区的格式化时间

        return get_time

    @staticmethod
    def _get_vector_db() -> LanceDB:
        """连接知识库向量数据库（带缓存）"""
        if ChatGraph._vector_db_cache is None:  # 检查缓存是否存在
            # 使用 BASE_DIR 构建绝对路径，避免工作目录影响
            db_path = Path(settings.BASE_DIR) / 'web' / 'documents' / 'lancedb_storage'
            db = lancedb.connect(str(db_path))  # 连接 LanceDB 数据库
            embeddings = CustomEmbeddings()  # 初始化自定义嵌入模型
            ChatGraph._vector_db_cache = LanceDB(
                connection=db,
                embedding=embeddings,
                table_name='my_knowledge_base',  # 指定表名
            )
        return ChatGraph._vector_db_cache

    @staticmethod
    def _format_search_results(docs: list) -> str:
        """格式化搜索结果为可读文本"""
        # 将多个文档片段合并为带编号的文本
        context = '\n\n'.join(
            f'内容片段：{i + 1}\n{doc.page_content}'
            for i, doc in enumerate(docs)
        )
        return f'从知识库中找到以下相关信息：\n\n{context}\n'

    @staticmethod
    def _create_search_knowledge_base_tool():
        """创建知识库搜索工具"""
        @tool
        def search_knowledge_base(query: str) -> str:
            """当用户查询阿里云百炼平台的相关信息时，调用此函数。输入为要查询的问题，输出为查询结果。"""
            vector_db = ChatGraph._get_vector_db()  # 获取向量数据库连接（使用缓存）
            docs = vector_db.similarity_search(query, k=3)  # 执行相似性搜索，返回前3个结果
            return ChatGraph._format_search_results(docs)  # 格式化并返回结果

        return search_knowledge_base

    @staticmethod
    def _create_llm(tools: list) -> ChatOpenAI:
        """初始化 ChatOpenAI 模型，支持流式输出"""
        return ChatOpenAI(
            model='gpt-5-mini',  # 使用的模型名称
            openai_api_key=os.getenv('API_KEY'),  # 从环境变量获取 API Key
            openai_api_base=os.getenv('API_BASE'),  # 从环境变量获取 API 基础地址
            streaming=True,  # 启用流式输出
            model_kwargs={
                "stream_options": {
                    "include_usage": True,  # 在流式输出中包含 token 使用统计
                }
            }
        ).bind_tools(tools)  # 将工具绑定到 LLM，使其能够调用

    @staticmethod
    def _create_model_call(llm: ChatOpenAI):
        """创建 LLM 调用函数"""
        def model_call(state: AgentState) -> dict:
            res = llm.invoke(state['messages'])  # 调用 LLM 处理消息历史
            return {'messages': [res]}  # 返回新消息，会被 add_messages 自动追加到历史

        return model_call

    @staticmethod
    def _create_should_continue():
        """创建条件边判断函数，决定是否继续调用工具"""
        def should_continue(state: AgentState) -> str:
            last_message = state['messages'][-1]  # 获取最后一条消息（LLM 的响应）
            if last_message.tool_calls:  # 如果 LLM 决定调用工具
                return "tools"  # 路由到工具节点
            return "end"  # 否则结束对话

        return should_continue

    @staticmethod
    def _build_graph(
        model_call,
        should_continue,
        tools: list
    ):
        """构建并编译 StateGraph"""
        tool_node = ToolNode(tools)  # 创建工具执行节点

        graph = StateGraph(AgentState)  # 使用 AgentState 作为状态类型
        graph.add_node('agent', model_call)  # 添加 agent 节点（LLM 调用）
        graph.add_node('tools', tool_node)  # 添加 tools 节点（工具执行）

        # 定义图的边和流程
        graph.add_edge(START, 'agent')  # 入口点 -> agent 节点
        graph.add_conditional_edges(
            'agent',  # 从 agent 节点出发
            should_continue,  # 条件判断函数
            {
                'tools': 'tools',  # 需要调用工具时 -> tools 节点
                'end': END,  # 不需要调用工具时 -> 结束
            }
        )
        graph.add_edge('tools', 'agent')  # tools 节点执行完毕后 -> 回到 agent 节点继续处理

        return graph.compile()  # 编译图，返回可执行的应用

    @staticmethod
    def create_app():
        """创建并返回聊天图应用（带缓存）"""
        if ChatGraph._app_cache is not None:  # 如果缓存存在，直接返回
            return ChatGraph._app_cache

        # 构建应用的各个组件
        tools = ChatGraph._create_tools()
        llm = ChatGraph._create_llm(tools)
        model_call = ChatGraph._create_model_call(llm)
        should_continue = ChatGraph._create_should_continue()

        # 构建并缓存图应用
        ChatGraph._app_cache = ChatGraph._build_graph(
            model_call, should_continue, tools
        )
        return ChatGraph._app_cache

    @staticmethod
    def clear_cache():
        """清除缓存（用于测试或配置变更时）"""
        ChatGraph._vector_db_cache = None
        ChatGraph._app_cache = None
