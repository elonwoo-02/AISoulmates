# OpenClaw 机制参考方案（后端）

本方案基于 OpenClaw 的思想（Soul / Identity / Memory / Capabilities），适配本项目现有架构，强调渐进式落地，避免推翻现有逻辑。

## 目标
- Soul：稳定人格与价值观
- Identity：语言呈现方式（口吻、称呼、格式）
- Memory：长期记忆（结构化 + 检索）
- Capabilities：功能/工具开关

---

## 数据结构方案

### A. 角色层（持久化）
1. `Character` 增加字段
- `soul_text`（人格内核）
- `identity_text`（表达风格）
- `capabilities`（JSON：工具/功能开关）

2. `SystemPrompt` 继续作为全局策略与安全规则库

### B. 好友层（个性化）
1. `Friend` 保留 `memory` 字段
- 内容改为 JSON（summary + items）
- 用于“稳定记忆”

2. 向量库 `memory_items`
- 使用 LanceDB 保存可检索记忆（非数据库表）

---

## 运行时注入顺序（建议）
1. 安全与规则（SystemPrompt）
2. Soul（人格内核）
3. Identity（表达方式）
4. 稳定记忆（summary + items）
5. 相关记忆（检索结果）
6. 最近对话（短期上下文）

---

## Memory 更新机制
- 每 N 次对话触发更新（建议默认 N=10）
- LLM 输出 JSON
  - `summary`：一句话总结
  - `items`：结构化条目（category + content + confidence）

---

## Memory 检索机制
- 输入当前用户问题 → 向量检索 TopK
- 过滤 `friend_id`
- 注入到 prompt

---

# 落地步骤（按顺序）

## 阶段 1：字段准备
1. `Character` 增加 `soul_text` / `identity_text` / `capabilities`
2. 创建/编辑角色时可维护这三块内容

## 阶段 2：系统注入流程
1. 构造 `system_prompt` 时拼接：
- 全局 SystemPrompt
- Soul
- Identity
- Memory（结构化 + 检索）
2. 保持现有 LangGraph 不变

## 阶段 3：记忆升级
1. `Friend.memory` 改为 JSON
2. 每 N 次对话更新一次
3. 结构化 items 入向量库
4. 聊天时检索并注入

---

# 模板示例

## Soul 模板
```
你是一个真实、有温度的角色。
你对用户表现出关心与边界感。
你在事实未知时会明确说“不确定”，不会编造。
你优先提出有助于用户情绪稳定和行动的建议。
```

## Identity 模板
```
语气：温柔但坚定
称呼：称用户为“你”
回复长度：不超过 6 句
多用短句，避免冗长解释
```


# 电脑操作能力

实现“影子浏览器”功能，与后期像 Manus 那样的智能化扩展。