# 1.8 CodeBuddy Agent SDK

> 来源：腾讯云培训认证《CodeBuddy 架构师认证课件》· 1.8 CodeBuddy Agent SDK · 共 16 页幻灯片

## 第八章CodeBuddy Agent SDK

## 8.1 query() API

8.2 Session API

8.3 档案生成器

8.4 实战：智能聊天应用

8.5 多智能体研究助理

8.6 更多案例

8.7 核心收获

## CodeBuddy Agent SDK

以编程方式构建AI 智能体

## 仓库总览与前置条件

CodeBuddy Agent SDK 演示项目集合

SDK 定位

以编程方式构建AI 智能体

SDK 启动CLI 作为子进程

stdin/stdout 通信自主执⾏

前置条件

Bun 或Node.js 18+

已安装已认证CodeBuddy CLI

npm install @tencent-ai/agent-sdk typescript @types/node tsx zod

可用示例

7 个演示项目：

• 快速入门/V2会话/档案⽣成

• 智能聊天/研究助理

• 表格助手/邮件助理

快速开始

git clone https://cnb.cool/codebuddy/agent-sdk-demos

cd 具体示例目录

export CODEBUDDY_API_KEY=...

## 8.1 query() API 核心（1/2）

基本结构

query({prompt, options})

返回异步可迭代消息

for await 循环处理

查询选项

maxTurns 最大轮数

cwd ⼯作目录

model 模型选择

allowedTools ⼯具列表

架构流程

SDK 启动CLI ⼦进程

stdin/stdout 通信

智能体在cwd 中运⾏

消息类型

system 系统消息

assistant AI 响应

result 工具执⾏结果

## 8.1 工具、钩子与消息类型（2/2）

可用工具

文件操作：

•

Read/Write/Edit/MultiEdit/NotebookEdit

搜索：Glob/Grep/WebSearch

•

执行：Bash/Task

•

实用工具：

•

TodoWrite/WebFetch/BashOutput/KillBash

规划：ExitPlanMode

•

钩子机制

在工具执行前拦截

PreToolUse

正则匹配⼯具名

matcher

'Write|Edit|MultiEdit'

允许

continue: true

返回

拒绝

decision: block

返回

示例：强制.js/.ts 文件只能写入

custom_scripts/

提取响应文本

判断

message.type === 'assistant'

遍历

message.content

type === 'text'

找

提取

text

字段

这是获取AI 回复的标准模式

## 8.2 Session API 多轮对话

query() 单次自动化· Session 多轮对话

query() vs Session

✓上下文管理上，query() 需要手动管理，Session 原

生支持多轮对话

✓会话恢复上，query() 不支持，Session 可以通过

session_id 恢复

✓运行方式上，query() 是启动本地子进程，Session

是直接连接云服务

✓适用场景上，query() 更适合单次任务自动化和

CI/CD，Session 更适合多轮对话交互和交互式调试

适用场景

多轮代码审查· 交互调试· 需求澄清· 重构

核心特性

上下文保持· 会话管理· 状态维护

认证配置

CODEBUDDY_API_KEY（海外/ 中国版地址不同）

API 用法

createSession → send → stream

→resumeSession

四种模式

basic · multi-turn · one-shot · resume

## 8.3 实战：档案生成器

网络搜索+ 自动⽣成专业简历

功能定位

网络搜索研究人物背景

•

自动生成专业单页简历

•

输出.docx 格式文件

•

使用方法

cd profile-builder

•

npm install

•

npm start '人名'

•

输出→ resume.docx

•

工作原理四步

1. WebSearch 研究职业背景

2. 收集职位/经历/技能

3. 生成JS 脚本调用docx

4. 执行脚本生成.docx

技术要点

SDK 调用WebSearch 工具

•

搜索LinkedIn/GitHub/新闻

•

钩子限制文件写入范围

•

SDK+工具+生成完整闭环

•

## 8.4 实战：智能聊天应用

React + Express + WebSocket 全栈架构

技术架构

React(Vite) + Express + WebSocket 实时通信

前端5173 / 后端3001

npm run dev 同时启动

生产注意事项

隔离SDK 到单独容器

持久化替换内存ChatStore

会话记录需同步SDK 状态

添加用户⾝份认证

展示能力

SDK 与Web 应用集成

实时WebSocket 推送

AI 驱动的对话交互

核心价值

命令⾏到Web 服务的路径

为生产部署提供架构参考

SDK 集成到真实应用

## 8.5 多智能体研究助理（1/2）

主智能体

协调整个研究流程

拆分2-4 个子主题

Task 工具委派

研究员

WebSearch + Write

并行搜索网络

保存research_notes/

数据分析师

Glob/Read/Bash/Write

提取指标生成图表

保存charts/

报告撰写者

Skill/Write/Bash

整合PDF 报告

保存reports/

## 8.5 钩子跟踪与日志输出（2/2）

钩子跟踪机制

两个钩子

pre_tool_use

调用前→ 记录

post_tool_use

执行后→ 记录

跟踪四维度

谁→ 哪个智能体

•

什么→ 工具名

•

何时→ 时间戳

•

I/O → 输入/输出

•

关键字段

parent_tool_use_id

把工具调用归属到对应子智能体

不只是安全拦截更是可观测性↑

斜杠命令

开始研究

/research<主题>

竞品分析

/competitive-analysis

行业趋势

/market-trends

事实核查

/fact-check

总结发现

/summarize

日志输出

transcript.txt 人类可读

[RESEARCHER-1] → WebSearch

输入: query=‘量子计算’

tool_calls.jsonl

结构化

event/agent_id/tool_name

success/output_size

两种格式满足不同需求

## 8.6 更多案例：表格助手与邮件助理

SDK 在不同场景下的集成方式

表格助手

AI 驱动电子表格创建/分析

带公式、格式、多⼯作表

React+Express+Python

支持上传xlsx/PDF/Word

Python 支持

研究助理用uv + python

表格助手用openpyxl

SDK 不限于JS/TS

也支持Python 生态

邮件助理

IMAP 邮件客户端+AI 辅助

收件箱/智能搜索/AI 功能

支持Gmail 等

仅限本地使用（安全警告）

共同模式

设置API Key → 安装→ npm run dev 或uv run

生产化：隔离+持久化+认证

文档：codebuddy.cn/docs/cli/sdk

## 8.7 核心收获

Agent SDK 让你以编程⽅式构建具有CodeBuddy 能力的AI 智能体

ReAct 模式（Reasoning + Acting）

Reasoning（推理）

Acting（行动）

循环

举例

Agent System Prompt 设计四要素

角色定位

工具使用边界

任务执行策略

输出格式要求

工具调用异常处理

可重试错误（网络超时、服务临时不可用）→ 自动重试2-3 次，加指数退避

需人工介入的错误（权限不足、认证失败、资源不存在）→ 停止执行，反馈给用户，等待处理

Agent SDK vs 直接调用LLM API

Pipeline（流水线）架构

Human-in-the-Loop（HITL）

RAG（检索增强生成）处理长文档

## 本课程小节

两大API

query() 单次自动化

Session 多轮对话

通过本课程，我们掌握了Agent SDK 的两大API、钩子机制与多智能体开发模式

钩子安全

PreToolUse 拦截控制

保障安全边界

多智能体

主智能体+子智能体

Task 委派并行执行

案例路径

入门→档案→聊天

→研究→表格→邮件

## THANKS

## THANKS
