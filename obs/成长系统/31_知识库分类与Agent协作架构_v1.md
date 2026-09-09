# 31 · 知识库分类与 Agent 协作架构 v1

> 创建: 2026-09-09 | 定位: 「Obsidian 知识库 + Agent」协作的**设计定稿**
> 配套: AGENT_PROTOCOL.md（执行宪法）· 28_库脑脸蓝图（架构总纲）
> 一句话: **知识按「离决策的距离」分五层，每篇知识带 frontmatter 元数据，agent 接新项目按「画像→索引→匹配→取用→组装带 why 的方案」五步走。**

---

## 〇、30 秒看懂

你问的是：**「来一个新项目 → 我把基础信息给你 → 你通过 Obsidian 里的信息帮我判断：用什么架构/载体/通道/节点/内容，且每条都说清为什么。」**

回答：**能。而且我们已经有了 80% 的零件**（7 张决策卡 + 19 张方法论卡 + 4 个真实项目 + 复盘区 + 黄金集 + ai-architect skill）。缺的不是「再来个系统」，是**三件事**：
1. 知识统一贴「元数据标签」（frontmatter）→ agent 秒级找到该用哪几张卡，不用全库翻
2. 一条「新项目检索编排」工具 → 输入项目画像，自动吐「该读哪几张卡 + 哪几个坑 + 哪个老项目」清单
3. 输出模板升级成「方案蓝图」（架构/载体/通道/节点/内容 + 每条带 why + 出处）

---

## 一、GitHub 真实调研结论（2026-09-09 API 实测 star）

**结论先行：GitHub 上没有「Obsidian 知识库一键变咨询顾问」的现成系统。** 最接近的几个，都是「教 agent 用 vault / 把 vault 变成可检索库」的积木，不是成品决策机。我们要做的是**借鉴它们的模式，拼我们自己的图**（我们的业务卡/复盘/黄金集是独有资产，换任何系统都丢）。

| 项目 | ★(实测) | 借鉴什么 |
|---|---|---|
| kepano/obsidian-skills（Obsidian 创始人本人） | 48,071 | **agent 用 Obsidian 是官方方向**；Obsidian Flavored Markdown / properties(frontmatter) / CLI 是标准 |
| claude-obsidian | 14,766 | 完整知识循环 = **Capture(捕获原文)→Ground(每条论断带出处/权威/新鲜度/置信度/审核状态)→Connect(连页面/MOC)→Use(检索复用，不从零开始)**。我们的「证据链 ≥3」就是 Ground 的雏形，要补成「每个方案输出都带 source」 |
| anthropics/skills（Anthropic 官方） | 175,383 | **Agent Skills = 把方法论封装成 agent 可自动调用的 skill**（我们已有 ai-architect，方向正确） |
| khoj | 37,228 | 自托管 AI 第二大脑：从你的 docs 检索答案（印证「库 + 检索 = agent 问答底座」） |
| mcp-obsidian / obsidian-local-rest-api | 4,377 / 2,903 | 把 vault 暴露成 agent 可读写接口 |
| obsidian-copilot / smart-connections | 7,689 / 5,443 | 库内语义检索/RAG（**Phase 5 可选**，先用关键词+索引够） |
| obra/superpowers | 283,834 | skill + 方法论结构（我们已在用） |
| microsoft/graphrag | 35,910 | 图检索（复杂关系时再上，现在**不引入**，避免过度工程） |

**一句话**：方向 = 学 claude-obsidian 的 Ground（溯源）+ anthropics 的 Skills（封装）+ 我们已有的决策卡体系，**不换骨、不装新系统**。

---

## 二、知识分类方案：五层资产栈（按「离决策的距离」分，不是按主题分）

> 为什么按这个分：agent 接项目时最怕「不知道去哪翻」。五层 = 五种用途，agent 永远从 L0 往下走，每层只干一件事。

```
方法论/
├── L0 寻址层（agent 必先读）
│   ├── AGENT_PROTOCOL.md        # 执行宪法：先读库/禁凭记忆/溯源
│   ├── CLAUDE.md                # 交接手册：库地图
│   ├── README.md
│   ├── 成长系统/28~31           # 架构蓝图（本文件=31）
│   └── cards/index.json         # 决策卡机器索引
│
├── L1 决策层（新项目匹配用）
│   └── cards/*.md               # 7 张决策卡：场景→档位→架构→报价
│       └── candidates/          # 候选卡（未审核）
│
├── L2 方法层（取用方法）
│   └── foundations/<域>/*.md    # 19 张方法论卡（FDE/AR/PRICE/SALES/POC/EVAL...）
│
├── L3 实证层（找先例/避坑）
│   ├── 项目库/*.md              # 4 个真实项目档案
│   ├── 复盘区/*.md              # 坑/反模式/审核报告/每日复盘
│   └── 方案库/
│
└── L4 原料层（未提炼，agent 学习用）
    ├── raw/                     # 主动学习原料
    ├── 学习池/                  # 外部资料/学习总结
    └── 候选池/
```

**现有结构已基本是这个形**（不用大改目录！）——缺的是**每篇知识的元数据**，让 agent 不必读全文就知道「这张卡管什么场景」。

### 统一 frontmatter 标准（每篇 .md 顶部 YAML，Obsidian 原生支持）

```yaml
---
type: decision-card | method-card | project | review | note | raw
domain: [FDE, AR, PRICE, SALES, EVAL, POC]      # 属于哪个方法论域
tags: [跨境, 本地化, 顾问, 近企业, 迁移]          # 语义标签（决策卡已有）
triggers: [物流, 货代, 工厂, 制造业, 电商]        # ★新：出现这些词就该调这张卡
status: 正式 | 候选 | 已驳回 | 进行中
updated: 2026-09-09
evidence: [项目库/xx.md, 复盘区/xx.md]            # ★新：这张卡被哪些实战证明过
---
```

- **手机/桌面 Obsidian 原生显示**，agent 读 frontmatter 秒级建索引，不用全文扫
- `triggers` = 让「来项目」匹配从「靠感觉」变「靠规则」的关键字段
- `evidence` = Ground（溯源）落到卡级别：每次实战验证后 +1，卡被用 ≥2 次 = 成熟（治「看起来能用」）

---

## 三、Agent 配合规则：新项目五步协议

```
你（用户）说：     「来客户了，xx 行业，预算 xx，想要 xx」
                    ↓  第 0 步：结构化画像（缺的问，不猜）
项目画像 JSON：    {行业, 规模, 预算, 已有数据/现状, 目标, 交付形态, 关键约束}
                    ↓  第 1 步：读 L0（AGENT_PROTOCOL + index.json + frontmatter 索引）
                    ↓  第 2 步：匹配 L1（决策卡 triggers ∩ 画像 → 命中 0~2 张）
                    ↓  第 3 步：取用 L2/L3（命中卡 → 关联方法论卡 + 同域项目先例 + 复盘坑）
                    ↓  第 4 步：组装「方案蓝图」（见下）+ 诚实标缺口
你（用户）收到：   一份能直接拿去谈/开工的方案
                    ↓  项目干完
                    ↓  第 5 步：复盘回流 → 更新卡 evidence +1 → 跑黄金集 → 更新 index.json
```

### 输出模板：「方案蓝图」（每条都带 why + 出处）

```markdown
## 一句话结论（这单能不能接 / 值多少 / 核心风险）
### 一、架构 —— 推荐用 XX 架构 + 为什么
### 二、载体 —— 网页 / App / 桌面 / 对话，选哪个 + 为什么（引老项目）
### 三、通道 —— 触达/服务通道有哪些 + 为什么
### 四、节点 —— 项目流程分几步、每步产出 + 为什么这么分
### 五、内容 —— 要交付/沉淀的内容清单
### 六、报价档位 + 理由
### 七、风险与坑（引用复盘区具体文件）
### 八、诚实缺口（没做过的部分 + 下一步）
出处规则：每段末尾带 [来源: 卡 ID / 复盘文件]，找不到出处 = 明说「这是推断，无库内证据」
```

---

## 四、缺口清单（我们有什么 / 缺什么）

**已有（别重造）：** 决策卡 7 张+index.json / 方法论卡 19 张 / 项目库 4 个 / 复盘区 / 黄金集 v1.1 / ai-architect skill（8 步流程）/ AGENT_PROTOCOL / 8895 的 /api/ask（真 agent 问答通道）

**缺（按优先级）：**

| # | 缺什么 | 做什么 | 量级 |
|---|---|---|---|
| 1 | frontmatter 标准没落地 | 定 schema + 给现有 26 张卡/复盘批量补 frontmatter（半自动脚本 + 抽查） | 中 |
| 2 | 没有「新项目检索编排」工具 | 写 `retrieve_for_project.py`：输入画像 → 吐「该读哪几张卡 + 哪几个坑 + 哪个老项目」清单 → agent 拿清单组装 | 小-中 |
| 3 | 输出没有统一蓝图模板 | 升级决策卡模板 + ai-architect skill 的输出段（加架构/载体/通道/节点/内容 + why + 出处） | 小 |
| 4 | 黄金集只测「命中卡」 | 升级成「方案蓝图完整性」评测（断言 5 段齐全 + 有出处） | 中 |
| 5 | 回流闭环是手动的 | 项目完成 → 复盘 → 卡 evidence +1 自动化（半自动：agent 提醒 + 一键） | 小 |
| 6 | （可选 Phase 5）语义检索 | 上 embedding（obsidian-copilot 思路）——先不用，关键词+frontmatter 索引在 100 张卡规模够 | 延后 |

---

## 五、落地计划（分阶段，每阶段可验收）

- **P0 设计定稿**（本文件）：分类五层 + frontmatter schema + 五步协议 + 蓝图模板 —— 你过目
- **P1 分类基建**：写补 frontmatter 脚本 → 给现有卡/复盘批量补 → 抽查 5 张验证
- **P2 检索工具**：写 `retrieve_for_project.py` + 项目画像模板 + 蓝图模板 → **拿 1 个新项目真实跑一遍**（模拟输入）
- **P3 协议升级**：ai-architect skill 接入检索工具 + 输出改蓝图模板；AGENT_PROTOCOL 补第 31 号引用
- **P4 黄金集升级**：评测从「命中卡」→「蓝图完整」；跑全量看分数
- **P5 回流闭环**：项目复盘 → evidence +1 → 黄金集 —— 半自动跑通一次
- **P6 真实演练**：你给一个真实项目，全程走一遍，你验收「这方案能不能拿去用」

**需要你做的**：① 过目本设计（尤其「方案蓝图」的 8 段长这样对不对）；② 以后来项目按画像字段给信息（或直接大白话，我负责结构化）；③ 项目干完说一声，让 agent 写复盘回流。

---

## 六、落地状态（2026-09-09 更新）

| 阶段 | 状态 | 证据 |
|---|---|---|
| P0 设计定稿 | ✅ | 本文档 |
| P1 分类基建 | ✅ 完成 | 42 文件补 frontmatter（type/domain/tags/triggers/status/evidence）；YAML 42/42 可解析；网页 mdToHtml 加 YAML 剥离 |
| P2 检索工具 | ✅ 完成 | `~/.hermes/scripts/growth_kb/retrieve_for_project.py` + 画像/蓝图模板；3 模拟项目跑通 |
| P3 协议升级 | ✅ 完成 | ai-architect skill 加「第 0.5 步先跑检索工具」+ 输出改 8 段蓝图；AGENT_PROTOCOL 加「来项目」路由 |
| P4 黄金集升级 | ✅ 完成 | `eval_retrieval.py` + 12 条真实画像评测集 → 召回率 **1.00**（12/12） |
| P5 回流闭环 | ✅ 完成 | `bump_evidence.py` 复盘→卡 evidence +1（幂等实测）；AR-002 已挂 9/3 复盘 |
| P6 真实演练 | ✅ 演示 | 方案库/蓝图样例_五金厂质检AI_演示.md（完整 8 段带出处） |

**工具链速查**（都放 `~/.hermes/scripts/growth_kb/`）：
- 来项目 → `retrieve_for_project.py --text "画像"`（拿检索包）
- 复盘完 → `bump_evidence.py --review "复盘区/xxx.md"`（卡 evidence +1）
- 改完卡/词 → `eval_retrieval.py`（回归召回率 ≥0.7）
- 补 frontmatter → `add_frontmatter.py --apply`（新卡入库后跑）
