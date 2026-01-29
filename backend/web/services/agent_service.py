import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
from web.models.user import UserProfile
import json

@tool
def get_user_info_tool(username: str):
    """获取指定用户的个人资料信息。"""
    try:
        profile = UserProfile.objects.get(user__username=username)
        return json.dumps({
            "username": profile.user.username,
            "email": profile.user.email,
            "profile_text": profile.profile,
            "create_time": profile.create_time.strftime('%Y-%m-%d %H:%M:%S')
        })
    except UserProfile.DoesNotExist:
        return f"找不到用户 {username} 的信息。"

class SoulmateAgent:
    def __init__(self):
        # 显式禁用 streaming
        self.llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0, streaming=False)
        self.tools = {"get_user_info_tool": get_user_info_tool}
        self.llm_with_tools = self.llm.bind_tools([get_user_info_tool])
        
    def ask(self, query: str, username: str):
        system_msg = SystemMessage(content="你是一个 AISoulmates 项目的智能助手。你可以帮助用户查询个人信息。")
        user_msg = HumanMessage(content=f"当前登录用户是: {username}。用户问题: {query}")
        
        messages = [system_msg, user_msg]
        
        # 简化的 Agent 循环
        for _ in range(5): # 最多 5 轮工具调用
            response = self.llm_with_tools.invoke(messages)
            messages.append(response)
            
            if not response.tool_calls:
                break
                
            for tool_call in response.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]
                tool_func = self.tools[tool_name]
                
                # 执行工具
                observation = tool_func.invoke(tool_args)
                messages.append(ToolMessage(content=str(observation), tool_call_id=tool_call["id"]))
        
        return messages[-1].content

# 单例模式
agent_instance = SoulmateAgent()
