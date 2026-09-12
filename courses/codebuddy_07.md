# 1.7 MCP 集成与工具开发

> 来源：腾讯云培训认证《CodeBuddy 架构师认证课件》· 1.7 MCP 集成与工具开发 · 共 18 页幻灯片

## 第七章MCP 集成与工具开发

## 7.1 MCP 基本概念

7.2 常用 Server 与对比

7.3 配置实操

7.4 实战场景

7.5 练习作业

7.6 核心收获

## MCP 集成与工具开发

让AI 连接一切外部服务

## 本讲导航

了解MCP 基本概念，把外部数据源接到AI 上下文

学习目标

·

了解MCP 概念与接入方式

·

把外部数据源接到AI 上下文

·

让生成代码更贴近真实系统

·

成功连接1 个MCP Server

·

完成一次元数据驱动代码生成

·

走通读取→生成→验证闭环

完成标准

卡点入口

前置依赖

·

已理解Agent 工具调用

·

具备基本密钥安全意识

·

Token 不硬编码不提交Git

·

连接失败先独立验证

·

Server 进程与权限

·

终端手动npx 测试

## 7.1 信息孤岛与MCP（1/2）

AI 能做的

读取项目文件

修改代码

运行终端命令

搜索项目内代码

AI 做不到的

查询数据库

调用第三方API

读取实时数据

操作GitHub/Figma

MCP 是什么

Model Context Protocol

Anthropic 开放标准

连接AI 与外部服务

一句话定位

MCP = AI 的感官延伸

看到数据库

触摸GitHub

搜索互联网

## 7.1 核心概念与工作流程（2/2）

六个核心概念让AI 连接外部服务

MCP Host

AI 应用本身（CodeBuddy），发起请求的一方

MCP Server

提供工具和数据的服务程序（如SQLite Server）

六步工作流

请求→ 判断→ Client → Server → 返回→ AI 生成代码

MCP Client

在Host 中负责与Server 建立连接和通信

知识概览

Host 是AI 应用

•

Client 是通信组件

•

Server 是能力提供方

•

Tools 是可执行动作

•

Resources 是可读取数据

•

Prompts 是可复用模板

•

Sampling 是Server 反过来请求模型生成

•

Transports 是双方通信的通道

•

## 7.2 常用MCP Server 一览（1/2）

数据库类

SQLite

本地数据库操作，最简单的入门例子

PostgreSQL

读表结构、跑查询

MySQL

同样支持表结构读取和查询

数据库类MCP 最适合做元数据驱动开发

7.2

平台集成类

GitHub

管Issues、PR、仓库

Slack

读团队讨论、同步消息

Puppeteer

浏览器自动化、网页截图

Fetch

获取任意URL 网页内容

Memory

持久化记忆，跨对话记住信息

平台集成类的价值在于让AI 进入真实研发协作系统

搜索与知识类

Brave Search

实时网络搜索

DuckDuckGo Search

隐私友好的搜索

Filesystem

安全访问指定目录

知识库MCP

连企业知识库、产品文档或内部FAQ

搜索和知识类解决的是"知识更新"和"组织知识沉淀“

的问题

## 7.2 MCP vs 传统API 对比（2/2）

四个维度看本质差异

调用者不同

传统人类写代码调用

AI 自主判断何时调用，通过Tool 描述自动理解

MCP

集成成本不同

传统

每个服务单独对接

MCP

统一协议即插即用，一个JSON 文件搞定

交互方式不同

程序化、固定流程

传统

对话式、灵活路由，AI 根据上下文动态选择

MCP

认知层不同

传统

开发者知API 细节

MCP

AI 通过Tool schema 自动理解能力和参数

## 7.3 SQLite MCP 配置实操（1/3）

Step 1-2 创建+配置

重新加载CodeBuddy

让MCP 连接生效

测试输⼊：

请列出当前数据库中

'

所有表及其字段结构'

配置正确则AI 通过

MCP Server 返回

真实表结构信息

Step 3-4 重启+验证

标准JSON 格式

mcpServers 下每个key 是server 名称

包括：

command (启动命令)(参数数组)

args

env (环境变量，可选)

多个Server 可并列配置

mcp.json 格式

{

"mcpServers": {

"sqlite": {

"command": "npx",

"args": ["-y", "mcp-server-sqlite", "data/app.db"]

}

## 7.3 GitHub + 搜索MCP 配置（2/3）

扩展AI 的外部连接能力

GitHub MCP 配置

获取Token

Settings → Developer settings → PAT

勾选repo / issues / PR 权限

用@teolin/mcp-github

搜索MCP 配置

DuckDuckGo Search

安装命令(无需API Key)

npx -y @anthropic/mcp-server-duckduckgo-search

GitHub 使用示例

查看仓库最近5 个issues

根据issue 描述自动创建任务

AI 通过MCP 调用GitHub API

搜索使用示例

"我遇到这个错误[粘贴]，请搜索最新解决方案，然后帮我修复"

＋

AI 搜索

自动修复

一步完成复杂排查与解决

## 7.3 常见问题FAQ（3/3）

查看MCP 配置

在'我的MCP'面板

查看所有已配置Server

列表和运行状态

配置出错

查看错误日志

复制给CodeBuddy 修复

常见：JSON 格式/路径错

开关MCP 服务

点击服务右侧按钮

关闭或开启

不用的Server 临时关闭

连接失败排查

终端手动npx 验证

检查数据库路径

Token 有效性/网络

## 7.4 传统vs MCP + 实战场景（1/2）

传统vs MCP 流程

传统

打开数据库客户端→ 查表结构→ 手

动复制到文档→ 喂给AI → 写代码→

发现漏了再回去查

MCP

你说"写个用户订单查询接口" → AI 自

己查数据库表结构→ 基于真实结构写

代码→ 一步到位

场景1：Prisma Schema

流程：

AI 通过MCP

↓ 读数据库完整表结构

↓ 生成Schema

必须正确识别：

外键关系

中文注释

@@index 注解

@@map 注解

额外输出：

字段来源证据：每个字段标注来自哪张表/哪列

验收标准：

◼外键→ @relation 对

◼注释= 中文且准确

◼@@index 覆盖查询列

◼@@map 映射原表名

◼字段来源可追溯

场景2：自动CRUD

读取users 表结构

生成完整CRUD 接口：

GET 列表（分页+搜索）

GET 详情

POST 创建（参数校验）

PUT 更新

DELETE 删除

✦Prisma ORM + 类型安全+错误处理

## 7.4 智能查询+ 数据库变更同步（2/2）

MCP 的真正威力

场景3 智能查询

需求：统计分类下商品数量、平均价格、总销售额。

流程：AI 先查表结构确认字段，再生成Prisma 查询。

MCP 的威力

AI 直接感知数据库变化，在代码侧同步落地。从表结构到全栈更新，真正做到“一句话搞定”。

高级：变更同步

示例：users 表加phone 字段。

自动化：AI 通过MCP 确认表结构，自动更新Schema/类型/API

/前端表单+变更清单。

最佳实践

始终让AI 通过MCP 确认真实数据再生成。不要凭记忆告诉表结构，直接让AI自己查。

## 7.5 练习作业

练习1（必做）

SQLite MCP 配置

创建一个包含至少4 张表的SQLite 数据库

配置SQLite MCP Server

让AI 通过MCP 读取表结构

让AI 基于真实表结构生成Prisma Schema

练习2（必做）

MCP 驱动的CRUD 生成

基于练习1 的数据库

AI 通过MCP 自动生成完整CRUD 接口

验证代码能正确运行

关键：元数据驱动

AI 必须通过MCP 读取

练习3（进阶）

编写自定义MCP Server

提供以下能力之一：

读取Git 历史（最近20 条commit）

分析项目依赖树（package.json）

读取ESLint 检查结果

核心要求：

• 定义Tool：name / description / inputSchema

• 独立调试后再接入CodeBuddy

• 最小权限原则（只读操作）

• description 清晰（影响AI 工具选择）

## 7.6 核心收获与下一讲预告

MCP = AI 的感官延伸，从封闭助手变成连接一切的Agent

打破信息孤岛

没有MCP，AI 只能看到你给的文件。

有了MCP，AI 能看到数据库、触摸GitHub、搜索互联网。

不可逆操作三件套

description 标注"不可逆"

二次确认（confirm: true）

审计日志

元数据驱动

AI 通过MCP 读取真实表结构生成代码。

一次走通，减少来回补信息。

统一协议

一个JSON 配置文件即插即用。

比传统API 集成成本低一个数量级。

单一职责

每个Server 只负责一个业务领域（database-server / github-server）。

Next 下一讲预告

CodeBuddy Agent SDK

用SDK 编排多步骤Agent 工作流，从单工具调用到完整自动化流水线。

## 本课程小节

通过本课程，我们掌握了MCP 的基本概念、配置方法与实战应用

打破孤岛

MCP 连接AI 到

数据库/GitHub/搜索

统一协议

JSON 配置即插即用

集成成本极低

元数据驱动

AI 读真实表结构

生成代码一次走通

感官延伸

看到/触摸/搜索

从助手变Agent

## THANKS

## THANKS
