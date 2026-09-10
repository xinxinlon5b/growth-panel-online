# 第 4 章 · 三份权威调研（读原文入口 + 每份的独门弹药）

> 本章是「调研2_」三份完整报告的导读——每份的调研范围、权威源、独门弹药，以及「想看全文去哪看」。
> 完整版: Obsidian `方法论/成长系统/调研2_FDE一手权威_OpenClaw_20260910.md` / `调研2_企业AI治理权威_dsh_20260910.md` / `调研2_工程标准权威_DeerFlow_20260910.md`

---

## 一、为什么是三份、为什么是这三个 agent

你 2026-09-10 批评「一轮调研用的是过去找过的内容（范冰书）」「要用 3 个 agent」「要验证、要 MECE」后，二轮调研按**三轨分工**派出：

| Agent | 轨 | 为什么它适合 | 强制模型 |
|---|---|---|---|
| **OpenClaw** | A FDE 交付模式 | 现场交付视角（找原厂官方定义） | MiniMax-M3 |
| **dsh** | C 企业治理与采用 | 数据/报告挖掘（Gartner/McKinsey） | MiniMax-M3 |
| **DeerFlow** | B 工程实现标准 | 长任务多源抓取（云厂 WAF/ISO） | MiniMax-M3 |

三份报告 = 三轨独立调研 = MECE 基础（互斥：不同轨；穷尽：覆盖交付/实现/治理全程）。

---

## 二、报告 ① FDE 一手权威（OpenClaw）

**调研范围**：FDE 的定义、六阶段旅程、与四种岗位边界——全部换成**原厂一手**（Palantir/OpenAI/Anthropic），弃用社区书。

**独门弹药**：
- Palantir 官方：FDE = "product development paradigm, human equivalent of backpropagation"（产品开发范式）
- OpenAI 官方："FDE is how OpenAI brings AI into production" + 工作法「先解决具体问题、交付早期价值、迭代到规模化」
- Anthropic 官方 JD：FDE 岗「embed directly with strategic customers」+ 现场学的东西反哺平台
- 诚实附录：明确列出**弃用的二手源**（范冰书等）+ 未达成的检索（Gartner 对 FDE 视角空白——不硬凑）

**完整版 31KB** → Obsidian `成长系统/调研2_FDE一手权威_OpenClaw_20260910.md`

## 三、报告 ② 企业 AI 治理权威（dsh）

**调研范围**：企业 AI 采用现状、失败率真相、治理框架、成熟度、ROI、国内政策——20 份一手机构报告。

**独门弹药**：
- **失败率三源交叉**：MIT 95% 试点无营收 / BCG 74% 难规模化 / Gartner 45%（高成熟度才撑 3 年）
- **AI TRiSM 五支柱**（Gartner）：可解释性 / ModelOps / 数据保护 / 应用安全 / 模型清单——治理章节直接挂
- **5 级成熟度**（Gartner）：Awareness → Active → Operational → Systemic → Transformational
- **McKinsey 双段 ROI**：单点节省 + EBIT 影响——报价必配
- **国内权威**：信通院四阶五层 + 工信部 AI+ 政策——帮客户拿补贴

**完整版 27KB** → Obsidian `成长系统/调研2_企业AI治理权威_dsh_20260910.md`

## 四、报告 ③ 工程标准权威（DeerFlow）

**调研范围**：软件工程/架构交付的国际标准与云厂框架——AWS/Azure/GCP Well-Architected + TOGAF 10 + PMBOK 8 + ISO 42001，6 框架 × 12 阶段覆盖对照。

**独门弹药**：
- **12×6 覆盖表**：工程 12 段（Discover→Retire）每段标哪些框架强覆盖（●直接要求/○间接/·交其它）
- **缺口洞察**：三云厂在 Discover/Eval 弱（需求靠 REQ 方法学）；Retire 只有 TOGAF H + ISO 覆盖——正是我们补 RETIRE-001 的原因
- **诚实记录**：AWS ML Lens 反爬未直采、ISO 动态渲染只采到摘要——不装全

**完整版 18KB** → Obsidian `成长系统/调研2_工程标准权威_DeerFlow_20260910.md`

---

## 五、三份报告怎么配合用

**给客户讲专业度**（要权威数据）→ 报告②（失败率/TRiSM/成熟度/ROI）
**设计交付方案**（要工程标准）→ 报告③（12 段每段有云厂/ISO 可挂）
**规划交付动作**（要怎么走六阶段）→ 报告①（原厂 FDE 打法）

**一句话**：报告①告诉你怎么做对，报告②告诉你凭什么让客户信，报告③告诉你怎么做扎实。

---

*看完整报告：Obsidian 成长系统/ 下「调研2_」开头的 3 个文件。*
