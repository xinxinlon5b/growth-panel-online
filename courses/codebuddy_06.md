# 1.6 Skills 技能系统

> 来源：腾讯云培训认证《CodeBuddy 架构师认证课件》· 1.6 Skills 技能系统 · 共 17 页幻灯片

## 第六章Skills 技能系统

## 6.1 背景与起源

6.2 概念与核心机制

6.3 SKILL.md 与实操

6.4 Skills vs MCP 对比

6.5 课后作业

6.6 核心收获

## Skills 技能系统

Agent Skills 的价值、机制与实操

## 本讲导航

理解Agent Skills 核心价值与触发机制

学习目标

•

理解Agent Skills 核心价值

•

掌握SKILL.md 基础结构

•

完成一次可复现的Skill 调用

完成标准

•

独立创建1 个可触发Skill

•

完成输入→触发→输出验证

•

理解三级加载机制

前置依赖

•

了解基础Prompt 使用

•

能在项目目录中创建文件

•

已完成前五模块学习

卡点入口

Skill 未触发时检查：

•

description 是否足够具体

•

目录和SKILL.md 命名（大小写）

## 6.1 背景与起源

起源

2025.10 Anthropic

推出Agent Skills

提升特定任务表现

开放标准

行业迅速跟进

发布为开放标准

AI Agent 通用设计模式

Prompt 的问题

重复写协作协议

太密模型忽略约束

Token 成本直线上升

CodeBuddy 支持

完整⽀持

代码助手

Agent Skills

即装即用

## 6.2 概念与核心机制

Agent Skills 的核心概念与工作机制

定义

扩展AI 功能的模块化能力包，包含指令/元数据/资源。

先触发再加载

先看description 匹配才加载，装多个不占上下文。

Token 节省

只触发时才加载，不需全塞进Prompt。

三大优势

专精· 减少重复· 整合能力

vs 临时Prompt

Skills 自动按流程，Prompt 每次从零交代。

跨平台复用

开放标准，同一SKILL.md 多平台通用。

## 6.3 SKILL.md 格式与三级加载（1/4）

SKILL.md 基本格式

一级：元数据

启动时

始终加载(启动时)

name + description

二级：指令

触发时

触发时加载

SKILL.md 正文

三级：资源和代码

按需

按需加载

reference.md / 脚本

三级加载机制

分阶段加载信息，而非预先获取上下文

指令

灵活指导

代码

可靠性

资源

事实查找

轻量与强大并存

设计哲学

分阶段加载

而非预获取

## 6.3 实操：目录结构与会议纪要Skill（2/4）

在.codebuddy/skills/ 下创建技能目录

目录结构

.codebuddy/skills/

meeting-minutes/

SKILL.md

expense-reimbursement/

SKILL.md

reference.md

关键设计点

Output 可直接贴文档库

•

缺失信息标注UNKNOWN

•

检测费用话题触发报销Skill

•

meeting-minutes

Input 就是你要给AI 什么——会议文本、背景、输出偏好

•

Output 定义固定结构——背景与目标、结论摘要、决策、•

待办（含Owner/Deadline）、未决问题、风险与依赖

Procedure 是四步执行流程

•

Acceptance 是验收标准。

•

Skill 间协作

一个Skill 可以在流程里声明调用另一个Skill。

Skill 不一定是单打独斗的，它可以跟其他Skill 搭配出更完整的工作流。

## 6.3 报销Skill + reference.md + 验证（3/4）

SKILL.md

Description 关键词:

报销标准

•

所需材料

•

审批步骤

•

Input(4项必填):

expense_type

•

Amount

•

occurrence_date

•

pre_approved

•

Output（5项必填）:

①reimbursable — YES / NO / NEED_MORE

②policy_reference — 引用§章节

③approval_chain — 审批链分支

④required_documents — 材料清单

⑤common_rejection_reasons — 驳回原因

reference.md 设计

定位：

三级资源文件，用到才加载，不占上下文

覆盖四类：

• 费用类型→ 标准/上限

• 金额阈值→ 审批链

• 按类型→ 材料清单

• 例外+ 驳回原因

硬规则：严禁瞎编政策。reference.md 没写的→ 必须输出NEED_MORE_INFO。报销政策是事实性信息，"看起来合理" ≠ 正确。信息不足就说信息不足。

验证Skill 生效

Step 1：

>list skills

确认列表中可见

Step 2：

模拟会议记录触发

meeting-minutes

成功标准：

• 输出含固定栏目（决策/ 待办/ 风险与依赖）

• 待办含Owner + Deadline

• 结构对= 成功；回答了但结构不对= 失败

## 6.3 触发流程总结（4/4）

Step 1

元数据匹配

启动时加载所有

name + description

用户输入后判断匹配

Step 2

指令加载

匹配成功

读取SKILL.md 正文

加载完整指令

Step 3

资源引用

执行过程中按需

加载reference.md

不需要时不加载

Step 4

结构化输出

按Output 定义

生成固定结构

缺失标注UNKNOWN

## 6.4 Skills vs MCP 对比

Skills 管流程规范· MCP 管外部能力

Skills 解决什么

MCP 解决什么

经验/方法论→ 可复用SOP，输出稳定可验收

安全标准化调用外部工具和数据源

最强组合

本质差异

Skills 指挥流程+ MCP 提供手和眼睛

Skills = 行为规范· MCP = 能力接口

没有它会怎样

选择指南

无Skills 写法不一· 无MCP 只能凭上下文猜

按格式流程→ Skills · 拿数据调工具→ MCP

## 6.5 课后作业（二选一）（1/2）

独立完成一次Skill 配置与触发验证

选题A：SOP Skill

会议纪要/报销/周报三选一

准备输入材料（≥10轮/150字）

触发Skill 拿到结构化输出

截图要求

输入截图+ 输出截图+ Skill 被调用证据（固定结构=生效证据）

选题B：Web Skill

生成落地页index.html

Hero/卖点/FAQ/CTA 四模块

必须浏览器可直接打开

作业提交

存放在homework 文件夹

两个选题都需截图证明

Skill 触发和生效

## 6.5 必交感想与评判标准（2/2）

必交感想文档

输出必须出现固定结构（背景/决策/待办/风险）

待办含Owner + Deadline

缺失信息标注UNKNOWN 而非编造

涉及费用→ 触发报销联动

SOP Skill 评判

浏览器可直接打开

至少4 模块（Hero/卖点/FAQ/CTA）

代码结构清晰，CSS 可维护

有验收Checklist 或固定栏目

证明Skill 生效

Web Skill 评判标准

基本要求：浏览器直接打开，页面能用

必含4 模块（Hero/卖点/FAQ/CTA）

代码要求：结构清晰，CSS 可维护

验收Checklist：

浏览器可直接打开

4 模块齐全

HTML 结构语义化

CSS 无内联/可维护

固定栏目输出完整

页面能看+ 代码经得起查

## 6.6 核心收获与下一讲预告

Agent Skills = 把临时Prompt 升级为可复用SOP 的能力封装

核心价值

稳定性、复用性、可验收。

让AI 在正确场景自动加载正确⽅法，输出更稳定。

Skills vs MCP

Skills 管流程规范（怎么做）

MCP 管外部能⼒（用什么做）

最强是组合使用

三级加载

元数据始终加载→ 指令触发时加载→ 资源按需加载。

轻量且强大，装很多Skill 不影响上下文。

下一讲预告

模块七：MCP 集成与工具开发

让AI 从"封闭空间里的助手"变成"能连接一切的Agent"

## 本课程小节

通过本课程，我们掌握了Agent Skills 的核心价值、触发机制与实操方法

核心价值

稳定性、复用性、可验收

从临时Prompt 升级为SOP

三级加载

元数据→ 指令→ 资源

轻量且强大

Skills vs MCP

流程规范vs 外部能力

组合使用效果最佳

实操闭环

配置→ 验证→ 触发

→ 结构化输出验收

## THANKS

## THANKS
