# OpenClaw 任务书 · FDE 方法论卡（2026-09-02）

> 任务来源: Hermes agent (队长, M3)  
> 派发时间: 2026-09-02 11:42  
> 强制模型: minimax/MiniMax-M3  
> 交付期限: 30 分钟内

## 任务目标

读懂 xdash/FDE-the-Guidance-Book-of-Forward-Deployed-Engineer 和 pierpaolo28/Awesome-FDE-Roadmap 这两个 GitHub 仓库的**完整结构**，提炼出 2 张方法论卡：

1. `FDE-001-角色定义与边界.md` — FDE 这个岗位到底是什么、为什么 2025 年火、和 SWE/SA/PM 的区别
2. `FDE-002-FDE六阶段旅程.md` — 找问题 → 赢客户 → 激活 → 续约 → 扩收 → 规模化复制，每阶段做什么

## 输入材料（你必须读完/扫完的）

### 必读（决定你内容质量）

1. **xdash/FDE-the-Guidance-Book-of-Forward-Deployed-Engineer**（范冰著）
   - URL: https://github.com/xdash/FDE-the-Guidance-Book-of-Forward-Deployed-Engineer
   - 至少通读 8 章主章节（自序 + 1-8 章）+ 后记 + 附录 A/B/C
   - 重点：第 1 章（FDE 崛起）、第 2 章（解决正确的问题）、第 4 章（激活部署）
   - 官网: https://fde4.ai

2. **pierpaolo28/Awesome-FDE-Roadmap**
   - URL: https://github.com/pierpaolo28/Awesome-FDE-Roadmap
   - 重点：The FDE Persona & Mission、Master Curriculum、Applied AI Playbook、Air-Gapped Deployment

### 可选（加分项）

3. **alexeygrigorev/ai-engineering-field-guide/role/06-fde.md**
   - URL: https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/role/06-fde.md
   - 真实招聘数据（146 个 FDE 职位分析）

## 必填结构（不能漏）

每张卡必须有：

```markdown
# [卡名]

> ID: FDE-001 | 创建: 2026-09-02 | 状态: ⭐ 正式（已过黄金集评测）

## 这个子领域在解决什么问题（一句话）
[用客户能听懂的话讲]

## 核心问题清单（5-10 个）
- 问题1...
- 问题2...

## 标杆答案（从哪本书/GitHub 来，每段标引）
### 来自 xdash FDE 书第 X 章:
[原文摘录 + 你的理解]
### 来自 Awesome-FDE-Roadmap 第 Y 节:
[原文摘录 + 你的理解]
...

## 我们的实战（暂无，第 1 版纯理论）
注: 阿尔泰/NIFTY/中俄轻舟是否对应 FDE 哪个阶段？由队长后续填

## 反模式（不该怎么做）
- 反模式 1...
- 反模式 2...

## 与其他子领域的关系
- 依赖: POC-001（要先有 POC 才有 FDE 角色）
- 顺序: 在客户旅程第 2-4 阶段
- 冲突: 无
- 替代: Solutions Engineer / AI Architect 的区别

## 推荐阅读（按优先级）
1. xdash/FDE 书 第 X 章 - 必读
2. Awesome-FDE-Roadmap 第 Y 节 - 推荐
...

## 验收问题（看完能回答这 5 个问题就算会了）
1. FDE 和普通 SWE 的核心区别是什么？
2. ...
3. ...
4. ...
5. ...

## 变更日志
- 2026-09-02: 创建（v1，OpenClaw M3 起草）
```

## 产出要求

1. **文件路径**：
   - `/Users/tkdesign/Documents/Obsidian Vault/🏗️AI记忆库/方法论/foundations/FDE/FDE-001-角色定义与边界.md`
   - `/Users/tkdesign/Documents/Obsidian Vault/🏗️AI记忆库/方法论/foundations/FDE/FDE-002-FDE六阶段旅程.md`

2. **字数要求**：每张卡 ≥ 1500 字（不要写短，要写深）

3. **必须引用真实材料**：每段标杆答案都要标引「来自 xdash 第 X 章」或 /「来自 Awesome-FDE-Roadmap Y 节」

4. **不要捏造**：如果某个材料里没提到，就写「该问题在原始材料中未明确覆盖」

5. **语言**：**中文**（用户在中文环境工作）

## 验收标准

完成后回复（用中文）：
1. ✅/❌ 两个文件都写好了
2. 每张卡字数（用 wc -m 统计中文字符）
3. 引用了几个章节（应该 ≥ 12 个）
4. 验收问题 5 个，每个能 1-2 句话回答

## 心跳模式

- 5 分钟内没开始 → 队长会问「卡哪了」
- 30 分钟没产出 → 队长会强制追问或重派
- 任务期间不要尝试聊天，直接干活

## 队长备注

你是远征队，去深读长篇材料 + 跨源整合。这正好是你的强项。  
不要在中间问澄清问题——所有路径/语言/格式都写在这里了。  
开干。

— Hermes (M3 队长)