# 36 · 权威调研 MECE 汇总 v1.0（定稿）

> 创建: 2026-09-10 | 状态: **v1.0 定稿**（R2+R3+R4 三份一手权威调研全合流）
> 调研执行: OpenClaw（R2）+ dsh（R3）+ DeerFlow（R4），全部强制 MiniMax-M3，Hermes 队长交叉验证
> 定位: 回答「有没有做到 MECE 汇总分类总结」——把三份权威调研合成一张**不重不漏**的企业 AI 落地全景。这是 34 号全景地图的「权威弹药库」。

## 〇、调研方法学（三 agent + 队长验证）

| 项 | 做法 |
|---|---|
| 调研 agent | OpenClaw / dsh / DeerFlow 三个全上，**全部强制 MiniMax-M3** |
| 一手源铁律 | 禁二手解读/个人博客/中文社区书（范冰 xdash 明确列入排除清单）；只采原厂官网/官方文档/官方新闻稿/权威机构报告 |
| URL 验证 | 队长抽查 **10+ URL 全部真实可达**（jina reader 代理绕过官网反爬） |
| 内容一致性 | Palantir FDE 定义、OpenAI FDE 定义**逐字吻合**（非编造引用） |
| 交叉验证 | 失败率数据三家权威互证（MIT 95% / BCG 74% / Gartner 45%） |
| 诚实标注 | 抓不到的源明确标「未能访问」，不硬凑（R2 机构视角空白 / R4 ML Lens 反爬） |

## 一、MECE 拆分（三轨互斥且穷尽）

企业 AI 落地全景 = 三个互斥维度：

| 维度 | 回答的问题 | 调研 | 权威来源 |
|---|---|---|---|
| **① 卖/交付侧（模式）** | 以什么模式帮客户落地 AI？凭什么说是主流？ | R2 OpenClaw | Palantir/OpenAI/Anthropic 原厂官方 |
| **② 买/治理侧（方法）** | 企业怎么选、怎么管、怎么算回报？ | R3 dsh | Gartner/McKinsey/BCG/MIT/信通院 |
| **③ 工程/标准侧（实现）** | 系统按什么标准做才专业可持续？ | R4 DeerFlow | AWS/Azure/GCP/TOGAF/PMBOK/ISO 42001 |

**MECE 证明**：
- **互斥**：①讲「怎么接单交付」（模式），②讲「客户怎么评估治理」（方法），③讲「代码架构怎么达标」（实现）——三者回答不同问题，不重叠。
- **穷尽**：覆盖「获客/接单（①）→ 客户决策/治理（②）→ 工程实现/交付（③）→ 运维/退役（③）」全链路。企业 AI 项目要么问「什么模式做」要么问「怎么管」要么问「怎么实现」，无第四类。

## 二、三轨权威版图（核心结论）

### ① 卖/交付侧：FDE = 三原厂背书的官方交付模式（R2）
- **Palantir**（发明者）：官方文档定义 FDE = "product development paradigm... human equivalent of backpropagation" — palantir.com/docs/foundry/architecture-center/platforms
- **OpenAI**：官方业务页 "FDE is how OpenAI brings AI into production for complex, real-world use cases" + 成立 The OpenAI Deployment Company — openai.com/business/the-openai-deployment-company/
- **Anthropic**：Applied AI 团队设 FDE 岗（官方 JD: "embed directly with strategic customers to drive transformational AI adoption"）— anthropic.com/careers/jobs/5302966008
- **交付物形态**（原厂 JD 共识）：MCP servers / sub-agents / agent skills / agentic systems
- **结论**：FDE 是我们交付模式的**原厂背书**——不是自创，不是范冰书概念

### ② 买/治理侧：企业 AI 落地的权威数据与框架（R3）
- **失败率**（三家交叉）：MIT NANDA 95% GenAI 试点无营收 / BCG 74% 难规模化 / Gartner 45% 高成熟度才撑 3 年
- **归因共识**：技术不是瓶颈，**组织/流程/治理才是**（McKinsey: 88% 在用 AI 但仅 21% 完成职能再设计）
- **治理框架**：Gartner **AI TRiSM 五支柱**（可解释性/ModelOps/数据保护/应用安全/模型清单）
- **成熟度**：Gartner 5 级（Awareness→Transformational）
- **ROI**：McKinsey 双段法（单点节省 + EBIT 影响两层）
- **国内**：信通院四阶五层 + 工信部 AI+ 政策（客户可拿补贴）

### ③ 工程/标准侧：系统实现的权威框架（R4）
- **AWS/Azure/GCP 三家 Well-Architected**：支柱同构（Security/Reliability/Performance/Cost/Operational/Sustainability），强在 Design→Operate→Iterate 工程中段；AI 专门透镜（AWS ML Lens / Azure AI Workload 强调非确定性 / GCP AI&ML Perspective）
- **TOGAF 10 ADM**：企业架构层唯一强覆盖 Discover/Architect/Retire（H 变更管理）
- **PMBOK 8**：项目管理横切层（7 绩效域）
- **ISO/IEC 42001:2023**：治理合规横切层，强在 Discover（AI 影响评估）/Data（数据治理）/Retire（模型退役）——工程框架天然空白处
- **12 阶段对照**：三大 WAF 覆盖 B4-B11（Architect-Operate），TOGAF 补 B1/B4/B12，ISO 42001 补治理空白

## 三、对 34 号全景地图的权威增量

| 34 原有（v1） | 36 权威增量（v2 素材） |
|---|---|
| 09 业务 7 阶段（粗糙，溯源不足） | FDE 三原厂官方模式 + JD 流程佐证（R2） |
| 25 工程 12 阶段（溯源 SDLC/12-Factor） | **12 阶段 × 6 权威框架覆盖表**（R4 §7）——每阶段可查哪些标准给了要求 |
| 方法卡 FDE-001/002（引范冰书） | **源头升级为原厂官方文档**（R2 附录 A 8 个一手 URL） |
| 缺治理/成熟度/ROI 权威 | TRiSM 五支柱 / Gartner 5 级 / McKinsey ROI（R3）→ 可入决策卡与黄金集 |
| 缺国际标准 | ISO 42001 / TOGAF / PMBOK 8 / 云厂 WAF（R4）→ 可入交付质量门禁 |

## 四、诚实缺口（MECE 未覆盖项也要说清）

1. **权威机构对 FDE 本身的分析空白**（R2 诚实记录）：Gartner/Forrester/IDC 无公开一手 FDE 报告——若需机构背书需付费订阅
2. **AWS ML Lens 详细支柱未抓到**（R4 被反爬）——存在性确认但细分待补
3. **ISO 42001 Annex A 控制项只有摘要**（iso.org 动态渲染）——具体条款待补
4. **R3 失败率样本差异**：MIT/BCG/Gartner 口径不同（试点营收/规模化/运营年限），引用需带上下文
5. **方法卡源头待更新**：FDE-001/002 仍引范冰书，需换 R2 一手 URL

## 五、下一步

1. 升级 34 号全景地图 v2（把 36 的三轨权威并进去，更新缺口表）
2. 更新方法卡 FDE-001/002 源头（范冰书 → 原厂官方文档）
3. 交付汇报（R0-R7 全链路）
