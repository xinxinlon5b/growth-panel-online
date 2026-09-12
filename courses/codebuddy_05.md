# 1.5 Speckit 规约驱动开发

> 来源：腾讯云培训认证《CodeBuddy 架构师认证课件》· 1.5 Speckit 规约驱动开发 · 共 23 页幻灯片

## 第五章Speckit 规约驱动开发

## 5.1 为什么需要 Speckit

5.2 三大核心概念

5.3 七步命令全景

5.4 环境准备与初始化

5.5 分步验收标准

5.6 Todo App 需求与宪法

5.7 旧项目Bug 修复

5.8 核心收获

## Speckit 规约驱动开发

从规约到实现的工程化闭环

## 本讲导航

掌握Speckit 核心概念与七步标准工作流

学习目标

掌握七步工作流

constitution → implement

独立完成从规约到实现闭环

完成标准

至少完整执行1 次全流程

并完成1 次analyze 检查

前置依赖

已能AI 基础代码生成

理解需求/方案/任务关系

卡点入口

先走快路径

plan → tasks → implement

跑通再补全完整链路

## 5.1 为什么需要Speckit

需求脱节

需求说一套，代码做另一套，边界条件频繁遗漏。

风格混乱

多人提示词不同，产出像拼接工程，协作成本极高。

不可复现

同需求不同时间，生成结果差异大，质量无法保障。

Speckit 本质

先写规约，再按规约执行, AI 时代的护栏系统

## 5.2 三大核心概念

规约驱动

Spec-driven

先定义做什么/不能做什么，验收标准是什么，再实现。

在规约驱动下：

调试= 修复规约

重构= 重构规约

代码自动重新生成

项目宪法

Constitution

项目最高原则

决定技术和质量底线：

Specify

维护软件= 维护规约

是否允许云端存储

测试覆盖最低要求

UI/语言规范

安全与性能优先级

防止AI自由发挥

clarify

先规划后施工闭环

七步闭环：

Constitution

→

clarify

→

Plan

Tasks

Analyze

Implement

每步有文档产出，可审计、可回溯。

## 5.3 七步命令全景表

specify 只谈需求· clarify 强烈建议· analyze 是返工预防器

/speckit.constitution

定义项目不可协商原则

constitution.md

/speckit.clarify

对模糊点提问补齐边界

更新spec.md

/speckit.tasks + analyze

任务拆解+ 一致性检查

返工预防器

/speckit.specify

用业务语言写需求WHAT

spec.md

/speckit.plan

生成技术方案HOW

plan.md

/speckit.implement

按任务顺序落地代码

可运行代码

## 5.4 环境准备与初始化（1/5）

CodeBuddy IDE / Code 均支持Speckit

安装Specify CLI

uv tool install specify-cli --from git+...spec-kit.git

或使用

进行一次性使用

uvx

项目初始化

specify init my-project

目录

下载模板、解压、Git 初始化，并生成

.specify

CodeBuddy 支持

IDE 和Code 环境都已支持

通过自定义指令实现Spec Coding 工作流

初始化后

项目包含

.specify/ specs/

在CodeBuddy 中打开，使用/speckit.* 命令

## 5.4 七步流程角色总览（2/5）

项目创始人：

制定宪法建立最高准则

技术栈/ 部署/ 三方库

产品经理：

自然语言定义WHAT

功能/ 用户故事/ 验收标准

描述越具体越好

需求侧角色

技术侧角色

架构师：

设计HOW

技术选型/ 架构/ 数据模型

你拥有最终决策权

审查者：

沙盘推演

检查spec / plan 矛盾遗漏

执行侧角色

项目经理：

拆解施工步骤

tasks.md 是核心界面

可随时调整优先级

程序员：

按顺序执行开发

复杂任务逐个执行

随时检查每步产出

## 5.4 实操：Step 1-3（3/5）

STEP 1

Constitution

/speckit.constitution

这是一个Next.js 问卷系统

AI 生成原则：

·

数据只存本地

·

交互简单直观

·

功能独立可测

存量项目直接/constitution

STEP 2

Specify

/speckit.specify

问卷系统/ 参考腾讯问卷

新建删除/ UI有活力/ 完成后鼓励动画

核心原则：

·

只描述'要什么'

·

不讨论'怎么实现'

STEP 3

Clarify

/speckit.clarify

进行需求澄清

·

AI 提问约5 个问题

·

每个spec 有Review Checklist

·

对每个问题给出：

明确规则+ 示例

虽可选但强烈建议执行

## 5.4 实操：Step 4-5（4/5）

技术方案与任务拆解

Plan

STEP 4

STEP 5

/speckit.plan执行

基于需求澄清生成方案

AI 方案不符预期可直接要求修改

可直接要求修改

tasks.md 是核心

与AI 协作核心界面

•

可随时介入调整优先级

•

任务按依赖排序

•

Tasks

按Phase 拆解详细任务

每个含验收标准+ 时间

关键提醒

specify 只谈需求不抢跑

•

plan 你有最终决策权

•

tasks 每个有目标+判定

•

/speckit.tasks

## 5.4 实操：Step 6-8（5/5）

Analyze

/speckit.analyze

进行全面分析

检测不一致性(重复/ 歧义/ 欠指定)

生成报告并协助修复

是"返工预防器"

尤其适合中大型项目

Implement

STEP 7

STEP 6

STEP 8

/speckit.implement

开始写代码

按顺序执行tasks.md

✓

每完成一个打勾

测试失败自动修复

复杂任务建议逐个

随时检查每步产出

验收

npm run dev

启动项目

按验收清单逐项检查

如需修改可继续

改spec 文档

中途暂停用--continue 继续执行

## 5.5 分步验收标准（1/2）

Constitution 验收

输入

项目底线规则

产出

constitution.md

验收

至少5 条可检查的规则

•

不通过怎么改

把'代码要规范'改为'必须通过ESLint 且无error'

Specify 验收

输入

用户任务/场景/结果

产出

spec.md

验收

包含主流程

边界条件+ 异常场景

•

不通过怎么改

删技术细节改为'用户行为+系统反馈'

Clarify 验收

输入

对关键问题明确回答

产出

补全后spec.md

验收

关键歧义问题已关闭

•

不通过怎么改

对每个问题给出明确规则+ 示例

## 5.5 分步验收标准（2/2）

Plan + Tasks 验收

Plan 验收

· 方案完整覆盖spec

· 不通过先补缺再重跑

Tasks 验收

· 每任务有目标+ 完成判定

· 不通过拆分+ 补验收

Analyze 验收

冲突/遗漏分析

产出

验收

无重大冲突

发现问题回溯

需求冲突→改spec

•

技术不可行→改plan

•

任务不足→重生tasks

•

问题回到文档层面

•

Implement 验收

产出

可运行代码

主流程可演示

验收•

关键边界可验证

•

不通过

· 回到上游文档修正后再实现

这就是规约驱动核心

问题回溯到规约

## 5.6 Todo App 需求与宪法（1/3）

用Todo App 走完整七步流程

需求目标

●新增任务（标题+描述）

●删除/ 标记完成

●状态筛选/ LocalStorage

执行路径

constitution →specify →clarify →plan →tasks →analyze → implement

宪法要点

●中文界面

●不用蓝紫渐变

●Lint/Format / 测试必须

验收清单

功能完整/ 数据持久

中文+清新/ 无报错

基础测试通过

## 5.6 Todo Step 1-4（2/3）

Step1

Constitution

定义中文/清新

Lint 统一/测试必须

LocalStorage 持久化

Step2

Specify

描述五大功能需求

UI 简洁清新

列表清晰/操作直观

Step3

Clarify

描述必填？

删除要确认弹窗？

完成切换要动画？

Step4

Plan

React + TypeScript

项目结构/数据模型

LocalStorage 策略

## 5.6 Todo Step 5-9（3/3）

Step 5

Tasks

四Phase 拆解

搭建→核心

持久化→测试优化

Step 6-7

Analyze+Implement

检查一致性

按顺序执行打勾

测试失败自动修复

Step 8-9

运行验收

npm run dev

功能/数据/界面

测试全部通过

管理技巧

编辑tasks.md 调优先

--continue 继续

Application 清Storage

## 5.6 Todo App FAQ

修改优先级

· 直接编辑specs/xxx/tasks.md 调整任务顺序

· 然后重新执行命令/speckit.implement

tasks.md 是你与AI 协作的核心界面

中途暂停

· 在implement 执行中直接打断对话

·下次使用/speckit.implement --continue 继续

AI 将从上次停止的任务继续执行

数据清空

· 浏览器开发者工具Application 面板

· 手动清空LocalStorage

· 或在代码中添加“清空数据”按钮

这也可以作为新需求走一遍Speckit 流程

## 5.7 旧项目Bug 修复

用Speckit 建立规范化的修复流程

场景与流程:图片异常/产品缺失→ 六步修复闭环

specify init . → /speckit.specify 描述缺陷+

完整命令闭环

init . →specify →plan →tasks →implement →dev

Step 5-6 执行+验证

Step 3-4 策略+任务

Step 1-2 初始化+描述

期望

/speckit.plan 根因分析→/speckit.tasks 拆解

核心价值

拍脑袋修bug

有依据的修复闭环，新旧项目通用

/speckit.implement → npm run dev

按清单检查

## 5.8 核心收获与下一讲预告

Speckit 的核心不是多一套命令，而是开发范式升级。

规约是源头

AI 时代最重要能力之一

把需求转成可执行规约

维护软件= 维护规约

ANALYZE 是保险

编码前发现矛盾和遗漏

先一致后加速

降低返工成本

CONSTITUTION 是护栏

防止AI 关键决策自由发挥

技术选型/ 质量标准/ 安全底线

都写进宪法

下一讲预告

Skills 技能系统

理解Agent Skills 的核心价值和触发机制

## 本课程小节

通过本课程，我们掌握了Speckit 规约驱动开发的核心概念与七步标准工作流。

规约驱动

• 先定义再实现

质量保障

• Constitution 定底线

• Analyze 查一致性

• constitution → implement

• 维护规约而非代码

七步闭环

• 全程有据可查

新旧通用

• 新项目全流程

• 旧项目修复闭环

## THANKS

## THANKS
