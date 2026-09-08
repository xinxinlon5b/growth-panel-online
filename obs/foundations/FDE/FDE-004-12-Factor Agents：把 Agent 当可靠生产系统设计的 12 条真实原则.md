# 12-Factor Agents：把 Agent 当可靠生产系统设计的 12 条真实原则

- **状态**：正式
- **审核时间**：2026-09-03 19:54
- **审核方式**：人工在工作台审核通过
- **收录时间**：2026-09-03（v2 重写：按原仓库真实 12 条修正，不再混用 12-Factor App）
- **来源**：github.com/humanlayer/12-factor-agents（★25.7k，关键词学习"llm production"采集）
- **建议分类**：FDE
- **适用场景**：设计/架构企业级 AI Agent 应用时（对应 09 关卡地图阶段 3-5）

## 是什么
12-Factor Agents 是把软件工程经典《12-Factor App》方法论迁移到 LLM Agent 开发的一套生产级设计原则（作者 Dex，HumanLayer 创始人）。核心主张：**好 Agent 不是"给个 prompt + 一袋工具 + 循环到目标"，而是"大部分确定性代码 + 在关键点撒 LLM 步骤"**。所以 Agent 应用要用软件工程的可靠性标准来设计，而不是当"魔法黑盒"。

> ⚠️ 注意：它叫"12-Factor"但**内容不是** 12-Factor App 的 12 条（代码库/依赖/配置那套）。它是专门针对 LLM/Agent 场景的 12 条新原则——别混淆。

## 真实 12 条（v2 按原仓库修正）

| # | 原则（英文原名） | 大白话 | 我们的实战印证（阿尔泰/NIFTY/轻舟） |
|---|----------------|--------|----------------------------------|
| 1 | Natural Language to Tool Calls | 自然语言→结构化工具调用：LLM 只负责把"人话"翻译成结构化指令，剩下交给确定性代码 | 我们的 Agent 该学：不要让它自由发挥执行，让它输出结构化动作（如 send_vk/改pdf）再执行 |
| 2 | Own your prompts | Prompt 所有权归你：别外包给框架的黑盒 Agent(role/goal/personality) | 我们自己写话术引擎/系统提示词 = 对的方向；框架黑盒 = 失控 |
| 3 | Own your context window | 拥有你的上下文窗口：每次调用喂什么、不喂什么，你来决定 | RAG/上下文工程 = 决定"喂什么"；不控制 = 贵+乱 |
| 4 | Tools are just structured outputs | 工具调用=结构化输出：让模型输出 schema 化的工具意图，而不是让它直接执行副作用 | 触达/发消息前先出结构化意图再校验执行 = 安全闸门思想 |
| 5 | Unify execution state & business state | 统一执行状态与业务状态：执行到哪一步=业务状态，别两套账 | 任务队列/journal（NIFTY）= 统一状态的实践 |
| 6 | Launch / Pause / Resume | 用简单 API 支持启动/暂停/恢复：长任务可中断可续跑 | NIFTY 任务取消/恢复 = 方向对 |
| 7 | Contact humans with tool calls | 联系人类也用工具调用：转人工是一个"工具"，不是旁路 | 阿尔泰 [[TRANSFER]] 转人工 = 完全对应！ |
| 8 | Own your control flow | 拥有你的控制流：流程怎么走你代码说了算，不是让 Agent 自己乱绕 | 确定性编排 + Agent 只做决策点 = 我们的分层 |
| 9 | Compact errors into context | 把错误压缩进上下文：失败信息提炼后喂回，别把原始堆栈全塞 | 错误处理该学：结构化错误反馈而非堆栈倾倒 |
| 10 | Small, focused agents | 小而专注的 Agent：一个 Agent 干一件事，别造全能怪 | 单功能 agent（采/筛/发分离）= 对的方向 |
| 11 | Trigger from anywhere | 从任何地方触发：邮件/IM/API 都能唤起 Agent | 多平台触达（VK/TG/WA）的架构基础 |
| 12 | Make your agent a stateless reducer | Agent 做成无状态 reducer：状态外置，Agent 是"输入+状态→输出"的纯函数 | 重启不丢状态 = 我们任务 journal 的方向 |

## 什么时候需要
- 给企业客户做 Agent/智能体应用（不是玩具 demo）
- 任何"要长期跑、多用户用、出问题要负责"的 AI 应用
- 对照检查自己/客户的项目：12 条缺哪几条 = 未来哪里会炸

## 怎么做（步骤）
1. 读原仓库 README + 各 factor 章节：https://github.com/humanlayer/12-factor-agents（每条都有独立 md）
2. 新项目架构设计时（09 关卡地图阶段 3）逐条问："我的 Agent 怎么满足这条？"
3. 已有项目做架构审计时：逐条过，缺的标风险（第 7 条转人工、第 5 条状态统一最容易漏）
4. 给客户讲方案时：用 12 条证明"我们不是随便调模型的，是按生产标准设计的"

## 不该怎么做（反模式）
- 把 12-Factor App 的旧 12 条（代码库/配置/并发）当这个用——**完全不同**，混用=误导
- 只收藏不研读——每条 factor 都有真实代码案例，要看
- 用框架的黑盒 Agent（给 role/goal 就完事）——违反第 2、8 条（失控）
- 让 Agent 直接执行副作用（发消息/扣费）不经过结构化输出校验——违反第 1、4 条

## 可借鉴点
真实高星开源项目（humanlayer/12-factor-agents ★25.7k），作者是 HumanLayer 创始人（专门做 Agent 联系人类的基建），12 条每条有独立 md + 代码示例，是业界公认的 Agent 生产化 check-list。

## 我们的实战映射（待补全）
- 阿尔泰转人工 [[TRANSFER]] → 对应第 7 条（Contact humans with tool calls）✅ 已验证
- NIFTY 任务 journal/取消 → 对应第 5、6 条（状态统一/暂停恢复）✅ 方向对
- 轻舟 API 打通确定性代码 → 对应第 1 条（自然语言只做翻译，执行走确定代码）✅
- **待补**：第 3 条（上下文窗口控制）我们在 RAG/提示词管理上还没系统化

## 我的评论
v2 重写说明：初版我把 12-Factor App 的 12 条误当成 12-Factor Agents 的内容（结构审打回，1.5/5）。已按原仓库真实内容修正。教训：**写卡必须先读原仓库，不能凭印象**（铁律：证据关）。
