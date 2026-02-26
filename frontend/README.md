# AISoulmates Frontend

AISoulmates 的前端项目，基于 Vue 3 + Vite，负责角色创建、用户账户与个人资料、首页与社交相关页面展示。

## 技术栈

- Vue 3
- Vue Router
- Pinia
- Axios
- Vite
- Tailwind CSS
- DaisyUI
- Croppie

## 环境要求

- Node.js `^20.19.0 || >=22.12.0`
- npm

## 开发命令

安装依赖：

```bash
npm install
```

启动开发环境：

```bash
npm run dev
```

构建生产包：

```bash
npm run build
```

本地预览构建结果：

```bash
npm run preview
```

## 与后端联调

- 当前前端 HTTP 请求统一封装在 `src/js/http/api.js`
- 默认后端地址为：`http://127.0.0.1:8000`
- 开发前请先启动后端服务（见仓库根目录 `README.md`）

## 目录结构（核心）

```text
frontend/
├── src/
│   ├── views/            # 页面级视图
│   ├── components/       # 可复用组件
│   ├── router/           # 路由配置
│   ├── stores/           # Pinia 状态管理
│   ├── js/http/          # Axios 实例与请求拦截
│   └── assets/           # 静态资源与样式
├── package.json
└── vite.config.js
```

## 开发约定

- 页面放在 `src/views/`，通用组件放在 `src/components/`
- 路由统一在 `src/router/index.js` 中维护
- 全局状态统一放在 `src/stores/`
- API 调用建议统一通过 `src/js/http/api.js` 进行，避免分散创建 Axios 实例
