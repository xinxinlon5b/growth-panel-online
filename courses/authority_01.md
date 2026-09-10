# 第 1 章 · 全景地图 v2：三轨合流

> 本章是「企业 AI 落地全景地图 v2」的读书区版——把 FDE 交付模式 × 工程实现标准 × 企业治理方法，拧成一张「有法可依」的全景图。
> 完整版: Obsidian `方法论/成长系统/34_企业AI落地全景地图_工作台.md`

---

## 一、30 秒看懂这张图

```
轨 A（FDE 交付模式 · 三原厂背书）——回答「怎么接住一个客户并交付」
 ①解决正确问题 → ②赢得客户 → ③激活部署 → ④守住续约 → ⑤扩大收入 → ⑥规模化复制
                    ↕（每个业务段内部都要走一遍工程轨）
轨 B（工程实现 · 云厂 WAF + TOGAF + PMBOK + ISO 42001）——回答「把东西做出来的工程质量」
 Discover → Design → Architect → Data → Eval → Build → Test → Deploy → Accept → Operate → Iterate → Retire
                    ↕（贯穿两轨的质量线）
轨 C（企业治理 · Gartner/McKinsey/信通院）——回答「客户凭什么信我们、ROI 怎么算、怎么管」
 AI TRiSM 五支柱 · Gartner 5 级成熟度 · McKinsey 双段 ROI · 信通院四阶五层
```

**专业度 = 你说出的每句话都能指到这张图上的某个位置，且那个位置有权威出处（原厂/标准/权威机构）。**

## 二、轨 A：FDE 交付模式（三原厂一手权威）

> 权威源: Palantir 官方架构文档 · OpenAI Deployment Company 官方业务页 · Anthropic FDE 官方 JD
> **FDE 不是社区概念，是有原厂背书的官方交付模式**：
> - Palantir 定义「product development paradigm, human equivalent of backpropagation」（产品开发范式，人类版的反馈传播）
> - OpenAI 定义「FDE is how OpenAI brings AI into production」（FDE 是 OpenAI 把 AI 带进生产的方式）
> - Anthropic 设 FDE 岗「embed directly with strategic customers」（驻进战略客户现场）

| # | 阶段 | 做什么 | 权威佐证 |
|---|---|---|---|
| A1 | 解决正确的问题 | 客户现场识别真问题（先于方案） | OpenAI「从第一性原理出发，解决具体问题」 |
| A2 | 赢得客户 | 问题共识转可签合同 | Anthropic「推动变革性 AI 采用」 |
| A3 | 激活部署 | 30 天跑出第一个可测量价值 | OpenAI「先交付早期价值，再迭代到规模化」 |
| A4 | 守住续约 | 持续可见指标保住合同 | Palantir NDR 139%（现场工程师持续驻场） |
| A5 | 扩大收入 | 单点成功横扩 BU/地理 | OpenAI「识别可规模化的模式」 |
| A6 | 规模化复制 | 一个打法服务 N 客户 | Anthropic「把部署模式沉淀成团队可拥有的资产」 |
| A7 | 现场反馈环 | 共性需求反哺产品/平台 | Anthropic Managed Agents「Rakuten 案例：季度→双周」 |
| A8 | 职业道德边界 | 持客户凭证=极大信任极大风险 | Anthropic「自主操作…代表 Anthropic 最高水准」 |

## 三、轨 B：工程实现全流程（12 段 × 6 权威框架）

> 权威源: AWS WAF(+ML Lens) · Azure WAF(+AI Workload) · GCP WAF(+AI&ML) · TOGAF 10 ADM · PMBOK 8 · ISO/IEC 42001

| 阶段 | 强覆盖框架 | 缺口/洞察 |
|---|---|---|
| Discover | TOGAF ADM + ISO 42001 | 云厂 WAF 弱；需求方法学靠 REQ-001 |
| Design | 三云厂 WAF + TOGAF B/C | ✅ 覆盖足 |
| Architect | 三云厂 WAF + TOGAF C/D | ✅ 覆盖足 |
| Data | 三云厂 AI Lens + ISO 42001 | DATA-001 已补 |
| Eval | PMBOK + ISO 42001 | EVAL-004 已补 |
| Build | 三云厂 CI/CD | ✅ 覆盖足 |
| Test | 三云厂可靠性/混沌 | ✅ 覆盖足 |
| Deploy | 三云厂发布策略 | ✅ 覆盖足 |
| Accept | GCP WAF Review + ISO 审计 | ✅ 覆盖足 |
| Operate | 三云厂运营卓越 | ✅ 覆盖足 |
| Iterate | ISO 持续改进 + ML Lens 漂移监控 | MLOPS-001 已补 |
| Retire | TOGAF H 变更管理 + ISO 退役 | RETIRE-001 已补 |

## 四、轨 C：企业治理方法（权威数据与框架）

> 权威源: Gartner · McKinsey · BCG · MIT NANDA · Stanford HAI · 信通院 · 工信部

| 主题 | 权威内容 | 我们怎么用 |
|---|---|---|
| **失败率真相** | MIT 95% 试点无营收 / BCG 74% 难规模化 / Gartner 45% 高成熟度才撑 3 年 | 接单开场：「AI 项目失败不是技术问题」= 有据 |
| **成功要素** | 清晰战略 / 职能再设计 / 数据+ModelOps / 治理 / 领导层 | 交付方案必含「流程重设计」章节 |
| **治理框架** | Gartner AI TRiSM 五支柱（可解释/ModelOps/数据保护/应用安全/模型清单） | 方案治理章节直接挂 TRiSM |
| **成熟度** | Gartner 5 级（Awareness→Transformational） | 客户自评工具，决定补哪级 |
| **ROI** | McKinsey 双段法（单点节省 + EBIT 影响） | 报价必配双段 ROI 表 |
| **国内** | 信通院四阶五层 + 工信部 AI+ 政策 | 帮客户拿补贴/算力券 |

## 五、这张图对「你」意味着什么

**接客户时**：客户说「我们要上 AI」→ 打开轨 A 看现在走到哪段（多半还在 A1）→ 用 A1 的方法先解决正确问题 → 别急着写代码。

**交付时**：每个项目都要走轨 B 的 12 段（不是想到哪做到哪）→ 每段都有权威框架可查。

**报价时**：轨 C 的失败率数据 + TRiSM + 双段 ROI 表 = 你跟客户证明「这次不会重蹈 95% 覆辙」的弹药。

**这就是「把事先做对」的底图——不是靠感觉，是靠这张每个点都有出处的图。**

---

*完整版含 6 域 25 张方法卡挂载清单，见 Obsidian 34 号。*
