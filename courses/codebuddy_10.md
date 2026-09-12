# 1.10 CI/CD 自动化流程

> 来源：腾讯云培训认证《CodeBuddy 架构师认证课件》· 1.10 CI/CD 自动化流程 · 共 16 页幻灯片

## 第十章CI/CD 自动化流程

## 10.1 CLI 非交互模式

10.2 自动代码审查

10.3 自动测试生成

10.4 数据安全边界

10.5 练习作业

10.6 核心收获与课程回顾

## CI/CD 自动化流程

让AI 成为流水线上的一道工序

## 本讲导航

掌握-p 管道模式，AI 嵌入CI/CD 流水线

掌握CLI 非交互模式-p

自动代码审查+测试生成

理解数据安全边界

1 次git diff 管道

→ AI 代码审查

→ 结构化输出完整验证

前置依赖

学习目标

完成标准

卡点入口

已完成模块一CLI 使用

熟悉Shell 脚本基础

了解GitHub Actions 概念

codebuddy 命令找不到

检查npm 全局安装路径

是否已加入PATH

## 10.1 CLI 非交互模式与参数（1/2）

常见错误排查

核心参数速查

非交互模式-p

-p 打印后退出（基础）

•

--output-format json/text/stream-json

•

-y 跳过权限确认

•

--max-turns 限制轮数

•

--system-prompt-file 加载团队规则文件

•

--json-schema 验证输出结构

•

command not found

•

→ npm PATH 未设置

操作被拦截

•

→ 缺少-y 参数

JSON 解析失败

•

→ prompt 强调'只输出JSON'

登录态失效

•

→ CODEBUDDY_API_KEY

响应截断

•

→ max-turns 给太小

•

## 10.1 五种组合模式（2/2）

管道分析+ JSON

管道｜

将任意文本流传给CodeBuddy

-p

指定prompt（分析指令）

--output-formatjson

输出结构化JSON

jq

下游脚本解析JSON，串联自动化流程

-y

允许AI 写入/修改文件（默认只读）

--max-turns 10

限制最大轮次，防止任务无限执行

--system-prompt-file ./rules.md

加载团队统一规范文件

--append-system-prompt "..."

临时追加额外约束

文件修改+ 系统提示

限制轮次+ 多步串联

--max-turns 5

防超时

-c

继续上次对话

-r session-id

跨步骤保持上下文

注意：

-y 只在受控

CI 或信任脚本中使用

## 10.2 自动代码审查（1/2）

为什么需要AI 审查

不是替代人工，而是在人工之前先过一遍

滤掉低级错误

•

统一基础规范

•

让人工精力聚焦在业务逻辑+ 架构判断

•

基本用法：

git diff | codebuddy -p "审查安全/性能/边界/规范"

git diff HEAD~1 | codebuddy -p "...”

审查最近一次提交

git diff origin/main...HEAD | codebuddy -p "...”

审查整个PR

GitHub Actions 集成

本地审查命令

基本流程：

PR 触发

→ checkout 代码

→ setup-node

→ npm install codebuddy

→ git diff 获取变更

→ codebuddy -p "审查" --output-format json

→ Python 转Markdown

→ actions/github-script 发PR 评论

## 10.2 审查规则文件（2/2）

安全必查项

SQL 参数化查询

用户输入校验

禁止明文密钥/Token

HTTP 接口认证

TypeScript 禁用any

export 函数必须JSDoc

禁止空catch

错误处理规范

输出格式要求

规则文件使用

代码规范

.codebuddy/review-rules.md

CI 中引用：

cat diff | codebuddy -p

'$(cat rules)'

中文输出

严重程度/位置/建议

高严重程度

必须修复才能合并

## 10.3 自动测试生成

本地测试生成

生成测试

cat src/validators.ts | codebuddy -p "写完整单测" > test.ts

补PR 测试

git diff | codebuddy -p "为新增函数生成测试" -y

诊断失败

jest 2>&1 | codebuddy -p "分析失败原因"

CI 集成：PR 守门

test-coverage.yml：运行测试获取覆盖率

→ 找PR 新增无测试函数

→ 输出JSON 报告

→ 可选生成建议测试

定时补全（每周一）：

扫描覆盖率<50% 文件

→ AI 生成→ 自动创PR

Jest/Vitest 深度集成

package.json scripts：

test:diagnose 脚本

运行→ 捕获失败

→ AI 诊断→ 输出报告

每个问题给出：

失败原因

•

最小修复方案

•

是否影响生产

•

## 10.4 数据安全边界（1/2）

把AI 接入CI/CD 必须先明确的安全边界

数据安全边界

diff 过滤敏感文件

API Key 管理

-y 安全使用

diff 和文件内容会发到云端

禁止发送：密钥/Token/密码个人信息/内部IP涉密商业信息

排除.env*/secrets*

config/production*

*_key*/*_secret*

git diff -- '*.ts' ':!**/.env*'

环境隔离：开发/CI 不同Key

CI 通过Secret 注入

Key 轮换：检测明文混入阻断

只读分析：不用-y

写文件：限定工作目录

Bash 执行：审查prompt

生产环境配置：绝对禁止

## 10.4 私有化部署与合规清单（2/2）

企业级安全合规与私有化部署

合规清单①

Key 通过Secret 管理· diff 已排除

敏感文件

为什么私有化

基本架构

替代方案

金融/医疗/政务：数据不出境+审计+网络隔离

CLI → 内网AI 网关→ 私有化模型→ 企业

GPU

合规清单②

能力边界

AI 审查可能漏报· 不替代人工· -y 需制度约束

CI 日志不打印敏感· 已评估行业私有化需求

MCP 接本地Ollama，适合极高安全要求

## 10.5 练习作业

练习1（必做）

本地代码审查

练习2（必做）

GitHub Actions

练习3（进阶）

测试生成

交付要求

截图或粘贴输出

说明AI 发现/生成了什么

记录原始→建议→结果

## 10.6 核心收获

三个关键参数

PR 自动代码审查：

git diff → AI 审查

→ JSON 报告

→ PR 评论

自动测试生成：

检测未覆盖函数

→ AI 生成测试

→ 定时补全存量

两大CI 场景

Secret 管理Key

diff 过滤敏感文件

-y 限定受控范围

AI 审查不替代人工是人工前的第一道过滤

金句：三个命令AI 就进了CI

安全底线

Secret管理Key/diff过滤敏感/受控-y。

金句：git diff|codebuddy -p '审查'|jq '.issues’

——三个命令AI进CI

## 10.6 课程回顾

十个模块，一套完整的CodeBuddy 知识体系

十模块路径

安装使用→System Prompt →上下文工程

→Speckit →Skills →MCP

→Agent SDK →多Agent →CI/CD

最重要的事

构建了完整知识体系后，最重要的是持续实践，把每个模块的能力组合使用

核心能力

理解原理→动手验证→持续跟进

这不是终点，是起点

AI 工具迭代很快

金句

git diff | codebuddy -p '审查' | jq '.issues'

三个命令，AI 就进了CI

## 本课程小节

管道模式

-p 让AI 成为

流水线上的一道工序

通过本课程，我们掌握了CI/CD 自动化的管道模式、PR 审查、测试生成与数据安全规范

CI 集成

PR 审查+ 测试生成

自动化守门

安全底线

Secret / 过滤/ 受控-y

不替代人工Review

课程完结

十模块完整体系

理解→验证→跟进

## THANKS
