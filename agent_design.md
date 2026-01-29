# AISoulmates LangChain Agent 设计方案

## 1. 目标
在 AISoulmates 项目中集成 LangChain Agent，使其能够通过自然语言与用户交互，并具备调用项目内部 API 或外部工具的能力。

## 2. 技术栈
- **LangChain**: 用于构建 Agent 逻辑。
- **OpenAI / Gemini**: 作为底层大语言模型（LLM）。
- **Django**: 后端框架，集成 Agent 接口。
- **SimpleJWT**: 保持 Agent 接口的安全性。

## 3. 架构设计

### 3.1 核心组件
- **Agent Service**: 封装 LangChain 逻辑，包括 Prompt Template, LLM, Tools 和 Memory。
- **Agent View**: Django 视图，接收前端请求并调用 Agent Service。
- **Tools**:
    - `get_user_info`: 获取当前用户信息。
    - `search_soulmates`: (预留) 搜索匹配的用户。
    - `send_message`: (预留) 发送消息。

### 3.2 接口定义
- **Endpoint**: `/api/agent/chat/`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "message": "你好，帮我看看我的个人信息"
  }
  ```
- **Response**:
  ```json
  {
    "reply": "你的用户名是 elonwoo，个人简介是..."
  }
  ```

## 4. 实现步骤
1. 安装依赖: `langchain`, `langchain-openai`, `langchain-community`。
2. 创建 `backend/web/services/agent_service.py`。
3. 创建 `backend/web/views/agent/chat.py`。
4. 注册路由 `api/agent/chat/`。
5. 编写测试脚本验证功能。
