# AISoulmates

AISoulmates 是一个前后端分离的 AI 角色社交项目：用户可以创建虚拟角色、维护个人资料、把角色加入好友列表，并与角色进行流式对话。当前仓库由 Django 后端和 Vue 3 前端组成，前端构建产物会输出到 Django 静态目录，由 Django 统一托管。

## 当前能力

- 用户注册、登录、登出、JWT 刷新、获取当前用户信息
- 用户资料编辑，支持头像和背景图上传
- 角色创建、列表、详情、更新、删除
- 首页角色流与搜索
- 好友创建或获取、好友列表、删除
- 聊天历史获取
- 基于 SSE 的流式 AI 对话
- 基于 LangGraph + LanceDB 的知识库检索
- 基于对话上下文的长期记忆更新能力

## 技术栈

### Frontend

- Vue 3
- Vue Router
- Pinia
- Axios
- Vite
- Tailwind CSS v4
- DaisyUI
- Croppie
- `@microsoft/fetch-event-source`

### Backend

- Django 6
- Django REST Framework
- Simple JWT
- django-cors-headers
- Pillow
- python-dotenv
- LangChain / LangGraph
- OpenAI 兼容接口
- LanceDB

## 仓库结构

```text
AISoulmates/
├── backend/
│   ├── backend/                     # Django 项目配置
│   ├── web/
│   │   ├── models/                 # UserProfile / Character / Friend / Message / SystemPrompt
│   │   ├── views/
│   │   │   ├── user/               # 账户与资料接口
│   │   │   ├── create/             # 角色创建与管理接口
│   │   │   ├── friend/             # 好友、消息、记忆接口
│   │   │   └── homepage/           # 首页数据接口
│   │   ├── documents/              # 知识库原始文本、向量库与工具脚本
│   │   └── templates/              # Django 渲染入口页
│   ├── static/                     # Django 静态资源，包含前端构建产物
│   ├── media/                      # 运行期上传文件
│   ├── .env                        # 后端环境变量
│   └── manage.py
├── frontend/
│   ├── src/
│   │   ├── views/                  # 页面级视图
│   │   ├── components/             # 复用组件
│   │   ├── router/                 # 前端路由
│   │   ├── stores/                 # Pinia 状态
│   │   └── js/http/                # Axios 与 SSE 请求封装
│   ├── public/
│   ├── package.json
│   └── vite.config.js
├── AGENTS.md
└── README.md
```

## 快速开始

### 环境要求

- Node.js `^20.19.0 || >=22.12.0`
- npm
- Python 3.12+ 推荐

### 1. 克隆仓库

```bash
git clone https://github.com/elandwoo-02/AISoulmates.git
cd AISoulmates
```

### 2. 启动后端

在 `backend/` 目录下创建虚拟环境并安装依赖：

```bash
python -m venv .venv
.venv\Scripts\activate
pip install django djangorestframework djangorestframework-simplejwt django-cors-headers pillow python-dotenv openai lancedb langchain-community langchain-openai langchain-text-splitters langgraph
```

创建或补充 `backend/.env`：

```env
API_KEY=your_api_key
API_BASE=your_openai_compatible_base_url
```

运行后端：

```bash
cd backend
python manage.py migrate
python manage.py runserver
```

后端默认地址：

- API: `http://127.0.0.1:8000`
- Django 管理后台: `http://127.0.0.1:8000/admin/`

### 3. 启动前端开发服务器

在 `frontend/` 目录安装依赖并启动：

```bash
cd frontend
npm install
npm run dev
```

前端开发地址：

- Vite: `http://localhost:5173`

说明：

- 前端请求默认指向 `http://127.0.0.1:8000`
- 当前 Django `CORS_ALLOWED_ORIGINS` 和 `CSRF_TRUSTED_ORIGINS` 只配置了 `http://localhost:5173`
- 本地联调时请优先通过 `http://localhost:5173` 打开前端，而不是 `http://127.0.0.1:5173`

### 4. 构建并交给 Django 托管

前端生产构建会输出到 `backend/static/frontend`：

```bash
cd frontend
npm run build
```

构建完成后，运行 Django 并访问：

- `http://127.0.0.1:8000`

仓库当前已经配置了前端回退路由：

- 根路径由 Django 渲染 `index.html`
- 非 `media/`、`static/`、`assets/` 的路径会回退到前端页面

## AI 相关运行前提

### 聊天与记忆

好友聊天接口会调用 OpenAI 兼容模型，并通过 SSE 向前端流式返回文本。当前后端代码使用：

- 聊天模型：`gpt-5-mini`
- 记忆模型：`gpt-4o-mini`

这两个模型名都写在代码里；如果你的兼容服务不支持，需要先改后端实现再运行。

### 知识库检索

聊天图会从本地 LanceDB 中检索知识库内容，默认路径为：

- `backend/web/documents/lancedb_storage`

原始文本默认来自：

- `backend/web/documents/data.txt`

如果你需要重新构建向量库，可以在 `backend/` 目录通过 Django shell 调用脚本入口：

```bash
python manage.py shell
```

然后执行：

```python
from web.documents.utils.insert_documents import insert_documents
insert_documents()
```

该流程同样依赖 `.env` 中的 `API_KEY` 和 `API_BASE`。

## 核心接口概览

### 用户账户

- `POST /api/user/account/register/`
- `POST /api/user/account/login/`
- `POST /api/user/account/logout/`
- `POST /api/user/account/refresh_token/`
- `GET /api/user/account/get_user_info/`

### 用户资料

- `PUT /api/user/profile/update`

### 角色

- `POST /api/create/character/create/`
- `GET /api/create/character/get_list/`
- `GET /api/create/character/get_single/`
- `PUT /api/create/character/update/`
- `DELETE /api/create/character/remove/`

### 好友与消息

- `POST /api/friend/get_or_create/`
- `GET /api/friend/get_list/`
- `DELETE /api/friend/remove/`
- `POST /api/friend/message/chat/`
- `GET /api/friend/message/get_history/`

### 首页

- `GET /api/homepage/index/`

## 开发命令

### Backend

```bash
cd backend
python manage.py check
python manage.py test
python manage.py runserver
```

### Frontend

```bash
cd frontend
npm run dev
npm run build
npm run preview
```

## 测试与现状

- 仓库当前包含 Django 测试，已覆盖首页搜索和好友列表等后端行为
- 前端暂无自动化测试套件
- 当前已验证 `python manage.py check` 可通过
- 当前已验证 `npm run build` 可成功输出静态资源
- 构建时存在一条 DaisyUI 相关的 CSS `@property` 警告，但不阻塞打包

## 已知约束

- 仓库未提供 `requirements.txt`，后端依赖需要按 README 或代码导入自行安装
- 当前默认数据库为 SQLite，适合本地开发
- `backend/db.sqlite3`、`backend/media/`、前端构建产物等都属于运行期文件，不应视为核心源码
- 当前 README 只描述开发与本地运行，不代表生产部署方案已经完善

## 贡献

提交建议遵循现有 Conventional Commit 风格，例如：

- `feat(frontend): ...`
- `feat(auth): ...`
- `docs: ...`
- `chore: ...`

提交 PR 时建议说明：

- 影响范围：`backend`、`frontend` 或两者
- 行为变化或接口变化
- 如果涉及模型变更，附上迁移说明
- 如果涉及 UI 变更，附上截图

## License

仓库当前未提供 `LICENSE` 文件，如需开源分发，建议后续补充。
