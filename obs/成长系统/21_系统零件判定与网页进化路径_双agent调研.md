# 系统「零件/通道」全集与判定方法（Q2）+ 网页从备忘录进化到能指导工作（Q3）

> 交付: dsh · MiniMax-M3
> 基础材料: `/tmp/growth_panel_structure_summary.md`（已读, 不重复 197 词词典与现有 REL/CRISIS 卡定义）
> 目标增量: **怎么用 / 怎么判** + 真实项目实证 + 网页落地的输入输出 schema
> 写作约定: 「✅ 业界共识」= 多个权威来源（AWS/Google/Microsoft/GitHub 头部项目）共同支持; 「🟡 判断」= 行业有先例但缺乏统一标准, 由本调研基于证据归纳; 「❓ 公开资料未找到强共识」= 标注诚实空缺。

---

## Part A · 系统「零件/通道」全集与判定方法

### A.0 一句话总览（不是备忘录,是装备清单）

用户在原话里问「这个项目里应该有这些零件才对」「怎么知道该用什么」, 答案分三层:
1. **零件全集**: 一个生产级项目候选要装的零件, 按 9 大维度 MECE 列清楚（不只是术语, 而是「在什么信号下必须装」）。
2. **判定法**: 拿到需求后, 像面试官一样问 6-8 个关键问题, 把答案映射到零件清单。这套方法把「靠经验」变成「可复盘」。
3. **实证**: 2-3 个真实开源项目的完整零件清单（Cal.com / Supabase / Dify）, 用来验证「零件在生产里长什么样」。

> 判断依据: AWS Well-Architected Framework 5 大支柱、Microsoft Azure Well-Architected、Google SRE Workbook 的 Production Readiness Review (PRR) 是业界最被广泛引用的「零件维度划分」, 我们把它工程化、成本化、AI 化后落地。

### A.1 零件全集: 9 大维度 MECE（每个零件配「触发条件」）

> 说明: 「触发条件」= 项目里出现什么信号, 这个零件就必须存在。这是用户在原话里最缺的东西 — 现有术语词典只回答「是什么」, 没回答「什么时候必须有」。

#### A.1.1 可靠性 (Reliability)

| 零件 | 一句话作用 | 触发条件（什么时候必须有） |
|---|---|---|
| 重试 (Retry) + 指数退避 | 网络抖动时自动恢复 | 调用任何外部 HTTP/RPC/DB, 且失败是可恢复的（不是 4xx 业务错误） |
| 超时 (Timeout) | 防止慢请求拖死线程 | 所有 I/O 调用必须设, 否则一个慢下游就能耗光线程池 |
| 熔断 (Circuit Breaker) | 下游崩溃时快速失败, 不雪崩 | 依赖 ≥2 个外部服务, 任一可被视为不稳定（公网 API/第三方 SaaS） |
| 幂等 (Idempotency) | 重复请求结果一致 | 涉及支付/创建资源/消息消费, 或客户端会重试的场景 |
| 限流 (Rate Limit) | 保护系统不被超量请求压垮 | 公网暴露 API, 或资源有限（GPU/数据库连接池） |
| 降级 (Degradation) | 核心功能可用, 非核心可关闭 | 用户体验 SLA 比功能完整更重要（电商大促、客服系统） |
| 队列 (Queue) + 死信队列 | 异步解耦、削峰 | 任务处理时间 > 200ms, 或并发突发 > 平时 5x, 或需要重试语义 |
| 缓存 (Cache) | 减少重复计算/DB 查询 | 读多写少, 或数据可容忍短时不一致, 或热点数据明显 |
| 健康检查 (Health Check) | 负载均衡/容器编排判断存活 | 部署在 K8s/容器平台/任何 LB 后面 |
| 备份与恢复 (Backup & Restore) | 数据可恢复 | 任何持久化数据 + RPO/RTO ≠ 0（几乎所有业务） |
| 灾难恢复 (DR) | 整机房/整区域故障下恢复 | 业务连续性要求 ≥99.9%, 或数据是关键资产 |
| 混沌工程 (Chaos Engineering) | 主动注入故障验证韧性 | 系统 ≥6 个月生产, 关键路径多服务依赖 |

来源: AWS Well-Architected Reliability Pillar; Google SRE Workbook Ch.30 (Production Readiness Review); Manuel Blinkert AI Production Readiness Checklist (https://github.com/manuelblinkert/ai-production-readiness-checklist)。

#### A.1.2 安全 (Security)

| 零件 | 一句话作用 | 触发条件 |
|---|---|---|
| 鉴权 (Authentication) | 验明「你是谁」 | 任何多用户系统, 或任何需要登录的功能 |
| 授权 (Authorization) | 决定「你能做什么」 | 角色/权限差异（管理员/普通用户/租户） |
| 审计日志 (Audit Log) | 谁/何时/做了什么 | 合规要求（等保/GDPR/SOC2）, 或事后追溯需要 |
| 加密传输 (TLS) | 数据不被中途偷窥 | 任何公网传输, 含内网（内网 ≠ 安全） |
| 加密存储 (Encryption at Rest) | 数据库/磁盘文件被偷也不可读 | 包含 PII/支付/商业机密; 云数据库默认应开 |
| 密钥管理 (Secrets Management) | 集中、轮换、不落代码 | 任何需要 API Key/DB 密码/证书的项目 |
| CSRF 防护 | 防止跨站请求伪造 | 浏览器 + Cookie 会话 |
| XSS/注入防护 | 用户输入不可信 | 任何接受用户输入的地方（含 Markdown/AI 输出） |
| 输入校验 | 数据进系统前先过校验 | 任何接受外部输入（API/表单/上传文件） |
| 安全头 (CSP/HSTS/X-Frame-Options) | 浏览器层防御 | 任何 Web 应用 |
| 最小权限 (Least Privilege) | 服务账号/用户只给必需权限 | 任何含多个角色或多环境（dev/stg/prod） |
| 速率限制（应用层） | 防暴力破解/撞库 | 登录/注册/密码重置/敏感接口 |
| WAF / 异常流量检测 | 滤掉常见 Web 攻击 | 公网 Web 应用, 且有合规要求 |
| 依赖漏洞扫描 (SCA) | 第三方库已知 CVE | 任何用第三方库的项目（基本所有） |

来源: OWASP Top 10; Microsoft Azure Well-Architected Security Pillar; AWS Well-Architected Security Pillar。

#### A.1.3 可观测 (Observability)

| 零件 | 一句话作用 | 触发条件 |
|---|---|---|
| 结构化日志 (Structured Logging) | 可搜索、可聚合 | 任何非 demo 项目 |
| 指标 (Metrics) | 量化系统状态 (QPS/P99/错误率) | 有 SLA/SLO 目标, 或需要容量规划 |
| 追踪 (Distributed Tracing) | 一个请求在多个服务里走了多久 | 微服务/多组件调用链 |
| 告警 (Alerting) | 出问题叫人 | 有 on-call 或工作时间外需要响应 |
| 仪表盘 (Dashboard) | 让状态一眼可见 | 任何需要人监控的系统 |
| 错误聚合 (Error Tracking) | 异常集中、自动去重 | 任何用户会遇错的客户端/服务 |
| SLI/SLO/SLA 定义 | 量化可靠性目标 | 外部用户/有 SLA 承诺 |
| 业务监控（北极星指标） | 业务健康度量化 | 业务方要量化效果（留存/转化） |

来源: Google SRE Workbook; Datadog/New Relic 行业实践; OpenTelemetry 项目。

#### A.1.4 数据 (Data)

| 零件 | 一句话作用 | 触发条件 |
|---|---|---|
| 数据校验 (Validation) | 进库前确保格式/范围正确 | 任何写操作 |
| 事务 (Transaction) | 多步写入要么全成要么全不成 | 多表/多写操作, 且需要原子性 |
| 数据迁移 (Migration) | schema 变更可追踪、可回滚 | DB 结构会变（所有成长中的项目） |
| 主数据管理 (Master Data) | 关键实体（如客户/商品）唯一源 | 多系统共享同一关键实体 |
| 数据血缘 (Data Lineage) | 数据从哪来到哪去 | 数据仓库/BI/合规审计 |
| 数据备份 + 异地 | 防数据丢失 | 任何生产数据 |
| 数据归档 (Archive) | 老数据不在线, 但可查 | 数据保留期 > 1 年, 或合规要求 |
| 软删除 (Soft Delete) | 误删可恢复 | 用户产生的内容（避免误删纠纷） |
| 数据脱敏 (Masking) | 测试/分析时保护 PII | 含 PII/敏感字段, 需在非生产环境使用 |
| 分区/分片 (Sharding/Partitioning) | 单表/单库太大 | 单表 > 5000 万行, 或 QPS > 单实例承载 |
| 读写分离 | 读多写少优化 | 读 QPS > 写 QPS 5x 以上 |

#### A.1.5 部署与运维 (Deployment & Ops)

| 零件 | 一句话作用 | 触发条件 |
|---|---|---|
| CI/CD | 自动化构建测试部署 | 任何团队项目（单人项目也强烈建议） |
| 环境隔离 (Dev/Stg/Prod) | 不同阶段不同环境 | 任何对外服务或严肃项目 |
| 配置管理 (Config Management) | 配置和代码分离 | 配置会因环境不同（DB 地址/密钥/特性开关） |
| 灰度发布 (Canary) | 新版本先给 1% 用户 | 影响用户的变更、任何有回滚成本的项目 |
| 蓝绿部署 (Blue-Green) | 零停机切换 | 关键业务 + 有双倍资源预算 |
| 特性开关 (Feature Flag) | 功能可独立于发版启停 | 需要分批推、紧急关闭、A/B 测试 |
| 容器化 (Containerization) | 环境一致、易迁移 | 任何长生命周期项目 |
| 编排 (K8s/Docker Swarm) | 多容器协同 | 容器数 ≥5, 或需要自愈/弹性 |
| IaC (Terraform/Pulumi) | 基础设施可代码化 | 多环境/多 region/团队协作 |
| 镜像仓库 + 镜像签名 | 制品管理 + 防供应链攻击 | 任何用 CI/CD 的项目 |
| GitOps | 通过 Git 同步环境状态 | K8s + ≥2 环境 |

来源: 12-Factor App; CNCF Cloud Native Landscape; Gruntwork Boilerplate 文档 (https://boilerplate.gruntwork.io)。

#### A.1.6 AI 特有 (AI-Specific) — 用户最缺的维度

| 零件 | 一句话作用 | 触发条件 |
|---|---|---|
| Prompt 版本管理 | 不同版本 Prompt 可追溯对比 | 任何用 LLM 的项目 |
| LLM 评测集 (Eval Set) | 用量化指标选模型/迭代 | LLM 在关键路径（不能只靠肉眼） |
| 幻觉治理 (Hallucination Mitigation) | RAG/Grounding/约束解码 | LLM 输出会被用户/系统信任并采纳 |
| 输出审核 (Output Filter) | 拦截不安全/不合规输出 | C 端/对外服务, 涉敏感行业 |
| 成本预算与告警 (LLM Cost) | 防止 token 烧钱 | 用 GPT-4/Claude 等贵模型 |
| 多模型路由 (Model Router) | 不同任务用不同模型 | 长流程 LLM 调用, 性能/成本权衡 |
| 上下文管理 (Context Window Mgmt) | 处理超长上下文 | 文档/对话类应用 |
| Token 限流 | 防止单用户滥用 | 多租户 LLM 应用 |
| 模型可降级 | 主模型不可用时切备用 | SLA 要求高, 单点依赖关键 |
| Embedding 版本管理 | 切模型后向量仍可比 | 任何用向量库的项目 |
| AI 审计日志 | 记录每次 LLM 调用的输入输出 | 合规 + 排错 |
| Prompt 注入防护 | 用户输入不能覆盖系统指令 | 用户输入会进入 Prompt |

来源: Anyscale "LLM Production Guide"; Manuel Blinkert AI Production Checklist; asq-sheriff/AI-Production-Checklist (https://github.com/asq-sheriff/AI-Production-Checklist)。

#### A.1.7 性能 (Performance)

| 零件 | 一句话作用 | 触发条件 |
|---|---|---|
| 性能基准测试 (Benchmark) | 量化性能 | 关键路径需要量化保证 |
| 压测 (Load Test) | 找瓶颈 | 上线前 / 大促前 |
| 性能剖析 (Profiling) | 找慢点 | 性能问题 |
| CDN | 静态资源加速 | 任何公网 Web 应用 |
| 连接池 (Connection Pool) | 复用 TCP/DB 连接 | DB / HTTP 客户端 |
| 异步处理 (Async/Await) | 不阻塞 UI/线程 | I/O 密集 |
| 浏览器/客户端缓存 | 减少重复请求 | 任何 Web 应用 |

#### A.1.8 成本 (Cost) — 团队容易忽略

| 零件 | 一句话作用 | 触发条件 |
|---|---|---|
| 云成本监控 | 看每月账单分布 | 用云服务（基本所有） |
| 资源标签 (Tagging) | 按项目/部门分账 | 多项目/多客户 |
| 自动伸缩 | 用多少付多少 | 流量有峰谷 |
| 预留实例 / Saving Plan | 长期资源省钱 | 资源 24x7 跑 |
| 大模型成本看板 | 看每个调用花多少 | LLM 应用 |
| 数据库/存储生命周期策略 | 老数据降级存储 | 长期保存数据 |

#### A.1.9 合规与法律 (Compliance) — 客户大、政府/医疗/金融必有

| 零件 | 一句话作用 | 触发条件 |
|---|---|---|
| 隐私政策/用户协议 | 法律要求 | 任何收集用户数据的应用 |
| 数据出境合规 | 数据不能随便出 | 政府/金融/医疗 |
| 个人信息保护 (PIPL/GDPR) | 用户权利保障 | 含个人信息 |
| 等保/SOC2/HIPAA | 行业强制 | 行业要求 |
| 知识产权审查 | 输出不侵犯第三方 | AI 内容生成 |

### A.2 零件全集统计

- **9 大维度**, 共计 **约 90+ 个零件**（按上面表格计数）;
- 其中传统软件工程零件 ≈ 65 个, AI 特有 ≈ 12 个, 合规 ≈ 6 个;
- 判断: 一个项目不需要全部具备, 但 A.3 的判定法会告诉你**该有的必须一个不缺**。

### A.3 判定法: 6 步需求→零件推导（可直接用做检查单）

> 这是用户最缺的「推导方法」。把「靠老司机经验」变成「可培训、可审计、可复盘」的流程。
> 设计原理: 把项目的关键属性（业务关键性、并发、数据敏感、失败代价、多人、外部集成、合规）抽出来, 每个属性映射到一组必装零件。

#### 第 1 步 · 业务关键性 (Business Criticality) — 决定底线深度

- 问: 「这系统挂了, 业务损失是什么? 」(零/小/大/灾难)
- 影响维度: 可靠性、灾备、可观测、部署
- 推导:
  - 灾难级 → 必备: 灾备 + 混沌 + 24x7 on-call + SLO < 99.95%
  - 大 → 必备: 备份 + 监控告警 + 回滚方案 + 健康检查
  - 小 → 必备: 健康检查 + 基本日志 + 备份
  - 零 → demo 级, 可酌情

#### 第 2 步 · 并发与规模 (Scale) — 决定横向能力

- 问: 「峰值并发多少? 峰值/均值比? 数据量? 增长曲线? 」
- 影响维度: 性能、成本、可靠性
- 推导:
  - QPS > 1000 或数据 > 1TB → 必备: 缓存 + 读写分离 + 分库分表 + 压测
  - 增长不可预测 → 必备: 自动伸缩
  - 长尾但量大 → 必备: CDN + 队列削峰

#### 第 3 步 · 数据敏感 (Data Sensitivity) — 决定安全深度

- 问: 「数据里有什么? PII? 支付? 健康? 商业机密? 」(无/PII/敏感/极敏感)
- 影响维度: 安全、合规、加密
- 推导:
  - 极敏感（金融/医疗/政府）→ 必备: 加密存储 + 加密传输 + 审计 + 数据脱敏 + 合规
  - 敏感 → 必备: TLS + 加密 + 审计 + 密钥管理
  - PII → 必备: TLS + 加密 + 隐私政策
  - 无 → 必备: TLS + 输入校验

#### 第 4 步 · 失败代价 (Failure Cost) — 决定韧性深度

- 问: 「一个错误请求 / 一次宕机会带来什么后果? 」
- 影响维度: 可靠性、可观测
- 推导:
  - 一次错误 = 直接经济损失 → 必备: 幂等 + 重试 + 熔断 + 事务
  - 一次错误 = 用户流失 → 必备: 降级 + 灰度 + 监控
  - 一次错误 = 内部损失 → 必备: 基本重试 + 日志

#### 第 5 步 · 多人协作 (Multi-tenancy / Multi-user) — 决定边界

- 问: 「多少用户/角色? 多租户? 跨团队使用? 」
- 影响维度: 权限、审计、可观测
- 推导:
  - 多角色 → 必备: 鉴权 + 授权 + 审计
  - 多租户 → 必备: 租户隔离 + 数据隔离 + 限流（防滥用）
  - 跨团队 → 必备: API 版本 + 文档 + 限流

#### 第 6 步 · 外部集成 (External Integrations) — 决定耦合点

- 问: 「调用几个外部服务? 公网/内网? 可控性? 」
- 影响维度: 可靠性、可观测
- 推导:
  - ≥3 个外部 → 必备: 熔断 + 超时 + 重试 + 监控调用链
  - 外部是关键路径 → 必备: 降级方案 + 多供应商备选
  - 调用 AI → 必备: Prompt 版本 + 评测 + 成本告警 + 输出审核

#### 额外 · AI 触发器（如果项目含 LLM/Agent）

- 触发: 用 LLM → 必须配: Prompt 版本 + 评测集 + 成本监控
- 触发: LLM 输出给用户看 → 必须配: 输出审核 + 幻觉治理
- 触发: 用户输入进 Prompt → 必须配: Prompt 注入防护
- 触发: 调用昂贵模型 → 必须配: Token 限流 + 模型路由

> 这套判定法的核心价值: 把「项目该不该有 XX 零件」的争论, 变成「这些问题的答案是什么」。可以照单问客户/团队, 答案出来, 零件清单就出来。

### A.4 3 个代表性真实项目完整解剖

> 选 3 个不同形态的代表性开源项目（高星、生产可用、文档全）来验证 A.1 的零件清单。**Cal.com** 是企业级 SaaS、**Supabase** 是 BaaS 平台、**Dify** 是 AI 应用平台 — 分别代表「传统 Web」、「数据 + 后端服务」、「AI 平台」三种最常见的客户形态。

#### A.4.1 Cal.com（~33k stars）— 企业级 SaaS 排程系统

> 选它原因: 真实服务全球 30+ 万用户, 多角色、多集成、多种部署形态, 是「中小团队给企业做 SaaS」的最佳参考标本。

| 维度 | 零件 | Cal.com 实际选择 | 为什么 |
|---|---|---|---|
| 前端 | Next.js 14 + React + TypeScript | 统一前后端, SEO 友好 | 多端 (web/embed/mobile-web) |
| API 层 | tRPC + REST + GraphQL | tRPC 让内部类型安全, REST 开放给第三方 | 既要 DX 也要生态 |
| 数据层 | Prisma + PostgreSQL | 单库 + 多 schema | 业务复杂但仍是单体优先 |
| 缓存 | Redis (Upstash) | session + rate limit | 多 region 部署 |
| 鉴权 | NextAuth.js + 自研 SSO | 多 provider | 企业客户要 SAML/OIDC |
| 授权 | RBAC (Team/Org/Member) | 多租户 | 企业版核心 |
| 搜索 | Postgres FTS + Algolia (可选) | 大部分场景 FTS 够 | 成本考虑 |
| 实时 | WebSocket (Socket.IO) | booking 状态同步 | 多端同步需求 |
| 异步任务 | Inngest (event-driven) | retry/delay/cron | 不自建队列 |
| 邮件/通知 | Resend + 自研模板 | 可观测 + 高到达率 | 邮件是关键路径 |
| 集成 | 100+ Calendar/Video/Payment | 抽象 Provider 层 | 核心业务 |
| 部署 | Vercel + Docker self-host | 双形态 | 满足不同客户 |
| 监控 | Datadog + Sentry | APM + 错误聚合 | 标品组合 |
| CI/CD | GitHub Actions + Turborepo | monorepo 加速 | 标准 |
| 测试 | Playwright (E2E) + Vitest | 端到端覆盖 | 业务流验证 |
| 安全 | Cal.com 是 Vanta/SOC2 启动中 | 合规驱动 | 企业客户要 SOC2 |
| 成本 | Vercel + Neon + Upstash | serverless 形态 | 弹性伸缩 |

**🔍 关键洞察**:
- **传统 SaaS 必备零件全有**: 鉴权、授权、审计、限流、缓存、监控、CI/CD、灰度（通过 Vercel preview）。
- **没有熔断/降级/混沌**: 因为 Cal.com 是单体 + 强依赖, 主要靠 Vercel 平台保证, 自己做的不多（**反面教材: 单点依赖外部服务**）。
- **没用 K8s**: 用 Vercel 替代, 表明「K8s 不是必须的」, 但「配置管理 + 环境隔离」是必须的。
- 来源: https://github.com/calcom/cal.com; https://cal.com/docs/developing/open-source-contribution/contributors-guide; https://mintlify.wiki/calcom/cal.com/developers/contributing/architecture。

#### A.4.2 Supabase（~75k stars）— 开源 BaaS（Firebase 替代）

> 选它原因: 多组件协同的典范, 把 PostgreSQL 生态拆成 8+ 个产品, 每个产品都是独立零件。

| 组件/零件 | 作用 | 关键技术选型 |
|---|---|---|
| Postgres 主库 | 主存储 + RLS 鉴权 | 单库, 配合 pgcrypto/CRDT/向量 |
| GoTrue | 认证服务 | Go, JWT, OAuth/SAML/Magic Link |
| PostgREST | 自动生成 REST API | 直接读 Postgres schema |
| Realtime | WebSocket 订阅 | Elixir Phoenix Channels |
| Storage | S3 兼容对象存储 | Go + S3/R2/Backblaze |
| Edge Functions | Deno serverless | 全球分布 |
| Studio | 管理 UI | Next.js |
| pgvector | 向量检索 | Postgres 扩展 |
| Logflare | 日志聚合 | ClickHouse + Cloudflare |
| Kong / 自研网关 | API 路由 + 限流 | 多租户 |
| 监控 | 内部 Datadog + 自研 dashboard | 组件多 |
| CI/CD | GitHub Actions + Turborepo | monorepo |
| IaC | Terraform (生产) | 多 region 部署 |
| 灾备 | WAL-G + S3 增量备份 + PITR | RPO 5min |

**🔍 关键洞察**:
- **零件全部自研或精心选型**: Supabase 把「零件」拆成产品, 每个产品都有清晰边界。
- **多语言共存**: Go/Elixir/TypeScript/Shell — 体现「为每个零件挑最合适的工具」, 而不是「全栈统一」。
- **强可观测**: 自研 Logflare, 因为他们卖 BaaS 可观测是卖点。
- **强合规**: SOC2 + HIPAA + GDPR — 因为做 BaaS 必须有。
- 来源: https://github.com/supabase/supabase; https://supabase.com/docs/guides/auth/architecture; https://mintlify.wiki/supabase/supabase/platform/overview。

#### A.4.3 Dify（~95k stars）— AI/LLM 应用平台

> 选它原因: 当下最热的 LLM 应用平台, 把 AI 特有零件呈现得最完整, 是用户做 AI 落地最有参考价值的项目。

| 维度 | 零件 | 选择 |
|---|---|---|
| 后端 | Python + Flask + Celery | 成熟 AI 生态 |
| 前端 | Next.js + TypeScript | 全栈友好 |
| 数据库 | PostgreSQL + Redis + Weaviate/Qdrant | OLTP + 缓存 + 向量 |
| LLM 抽象 | 自研 LLM Factory (统一 API) | 30+ 模型可换 |
| Prompt 编排 | 可视化 DAG | 节点化、版本化 |
| 工作流 | DAG 执行引擎 | 类 Airflow |
| RAG | 文档解析 → 分块 → embedding → 检索 → rerank → 生成 | 全链路可观测 |
| 评测 | 内置 Eval + 人工标注 | 关键卖点 |
| 鉴权 | 自研 RBAC + 工作空间 | 多租户 |
| 部署 | Docker Compose + Helm | 自托管友好 |
| 监控 | OpenTelemetry + Prometheus | 标准化 |
| Prompt 版本 | 内置 | AI 必备 |
| 输出审核 | 内置 Guardrails | 安全 |
| 成本 | 模型 token 消耗看板 | AI 必备 |
| 插件 | 工具调用 + 自定义工具 | Agent 能力 |

**🔍 关键洞察**:
- **AI 特有零件齐**: Prompt 版本、Eval、Guardrails、成本看板、模型路由 — 这是 A.1.6 那一节的实证。
- **RAG 全链路**: 解析→分块→embedding→检索→rerank→生成, 每一步都可替换。
- **多租户 + 工作空间**: AI 平台必备, 否则企业不敢用。
- 来源: https://github.com/langgenius/dify; https://docs.dify.ai; https://deepwiki.com/langgenius/dify。

### A.5 跨项目对比与发现

通过对比 3 个项目, 我们能归纳出几条「业界共识」与几条「容易忽略」:

**共识**:
1. 鉴权、授权、审计、CI/CD、健康检查是**任何生产项目都必备**。
2. 监控 + 告警 + 结构化日志是**默认配置**, 没有项目例外。
3. 环境隔离 + 配置管理 + 密钥管理是**底线**, 缺一不可。

**容易忽略**:
1. **灰度发布**只有 Cal.com（靠 Vercel preview）和 Dify（自托管环境隔离）做到 — 说明「中小企业项目常缺这个, 但很关键」。
2. **混沌工程** 3 个项目都没有（除了 Supabase 内部可能做了但没开源） — 说明这是头部大厂的事, 中小企业可暂缓, 但要列入路线图。
3. **AI 项目对 RAG 全链路的可替换性要求很高**, 这是和传统项目最大的不同。
4. **Dify 把「Prompt 版本」当一等公民**, 传统 SaaS 项目很少把「配置」做到这个深度, 值得借鉴。

### A.6 网页体现建议（这部分给网页开发）

> 怎么把这套东西变成网页功能, 而不是堆文档?

| 形式 | 适用场景 | 实现成本 | 用户价值 |
|---|---|---|---|
| **零件检索/卡片库** | 用户想查「什么是熔断」 | 低 | 低（词典已做） |
| **需求→零件推导问答** | 用户拿新项目, 想要清单 | 中（基于决策树） | 高（Q3 主诉求） |
| **项目零件模板** | 用户填项目信息, 生成建议清单 | 中高 | 高 |
| **真实项目样板间** | 用户看 Cal/Supabase/Dify 怎么做 | 中 | 高（参考价值） |
| **诊断问卷** | 用户评估「我项目缺什么」 | 低 | 中 |
| **零件装配图（可视）** | 一图展示维度与零件关系 | 中 | 中 |

**推荐组合**:
- **必做**: 需求→零件推导问答（决策树）+ 真实项目样板间 + 零件卡片升级（加触发条件）。
- **选做**: 项目零件模板（自动化生成）。
- **不做**: 把 90 个零件全铺成列表 — 用户会迷失。

---

## Part B · 网页从「备忘录」进化到「能指导工作」

### B.0 用户痛点再定义

用户原话:
- 「再有项目的时候, 我们网页如何能刚好地指导我们工作呢? 」
- 「比如我把基础信息给到网页, 他能帮我去做分析和处理, 应该用什么架构、用什么通道和配件、用什么载体, 以及为什么。 」
- 「现在网页各种零散的知识点, 只相当于我的备忘录。 」

翻译成需求:**输入一份项目基础信息 → 网页自动给出「载体 + 架构 + 零件清单 + 选型理由 + 风险与报价参考」**。

这是从「静态知识库」升级到「决策辅助工具」的跃迁 — 在业界有先例、有工具、有清晰路径, 但没有银弹。

### B.1 业界先例与工具调研

> 诚实区分「已经有人做到什么程度」vs「多数还是手动」。 我重点调研了 4 类已有方案。

#### B.1.1 类 1 · 知识库 + LLM 自动咨询（最接近用户的需求）

| 项目 | 做法 | 状态 | 来源 |
|---|---|---|---|
| **rag-architect-mcp** | 用 MCP 协议, 把「RAG 选型」做成有状态对话, AI Agent 一步步问你需求, 最后输出架构方案 | 实验性, 仅限 RAG 领域, 但模式可迁移 | https://github.com/kevin801221/rag-architect-mcp |
| **happydasch/llm_advisory** | LangChain + LangGraph + Pydantic 做的「主题顾问」框架, 可加载任何垂直领域知识 | 通用框架, 需要填知识 | https://github.com/happydasch/llm_advisory |
| **sagarika29/ai-system-architect** | AI 系统架构师, 推理而非生成 | 偏 demo | https://github.com/sagarika29/ai-system-architect |
| **tafreeman/agentic-runtime-platform** | 多 agent 平台, 含专门的 Architect Agent | 多 agent 协同 | https://github.com/tafreeman/agentic-runtime-platform |
| **build-on-aws/conversation-with-your-architecture** | 用对话查询 AWS 架构最佳实践 | 实验 | https://github.com/build-on-aws/conversation-with-your-architecture |
| **Custom GPTs + Knowledge Files** | 把方法论 PDF/MD 喂给 GPT, 用提示词约束输出 | 已落地, 个人/小团队常用 | OpenAI Custom GPT |
| **Microsoft Copilot Studio / Azure AI Studio** | 企业级, 拖拽式做领域顾问 | 已商用 | Microsoft |

**🔍 判断**:
- ✅ 「知识 + LLM 对话咨询」这条路径已**完全跑通**, 多个开源项目 + 商业产品都验证了。
- 🟡 但**多跳推理 + 结构化决策**仍是难题: 大多数顾问只能给「是什么」, 给不出「为什么 + 怎么做」。
- 🟡 「喂信息 → 出方案」要质量稳定, 通常需要:
  1. **结构化知识**（不是裸 markdown）;
  2. **决策规则**（决定树/评分卡）;
  3. **Prompt 模板**（约束输出格式）;
  4. **评测集**（验证输出质量）。

#### B.1.2 类 2 · 脚手架生成器（Scaffolding）

| 工具 | 作用 | 与「自动出方案」的关系 |
|---|---|---|
| **Cookiecutter** | 模板生成项目骨架 | 输出代码, 不是设计建议 |
| **Copier** | 进阶脚手架, 支持模板更新 | 同上 |
| **Yeoman** | Node 生态脚手架 | 同上 |
| **Stackbilder** | 受治理的架构模板 | 比纯模板多了「为什么选这个栈」 |
| **Gruntwork Boilerplate** | 企业级 Terraform 模块库 | 给 IaC, 不给决策 |
| **create-react-app / create-next-app** | 前端脚手架 | 只生成代码 |

来源: https://copier.readthedocs.io/en/v7.1.0/comparisons/; https://boilerplate.gruntwork.io/intro/boilerplate-vs-other/。

**🔍 判断**: 脚手架类工具解决的是「**生成代码**」, 不是「**生成方案**」。但它们提供了一种**输出形态参考**: 一个好方案, 至少要包含「组件清单 + 选型理由 + 模板代码」。

#### B.1.3 类 3 · 架构决策工具（ADR）

| 工具 | 作用 |
|---|---|
| **dotnet-adr** / **AdrPlus** / **tool_rad** / **phpadr** | 创建管理 ADR 文档 |
| **jossym17/architecture-toolkit** | 统一管理 RFC/ADR/Decomposition Plans + 影响分析 |
| **VaidhyaMegha/technical-decision-framework** | 客户需求技术决策框架, 含技术选项库 |

来源: https://github.com/endjin/dotnet-adr; https://github.com/jossym17/architecture-toolkit; https://github.com/VaidhyaMegha/technical-decision-framework。

**🔍 判断**: ADR 类工具解决「**记录决策**」, 但决策本身还是人来下。如果网页能「自动生成 ADR 草稿」, 用户价值巨大。

#### B.1.4 类 4 · 问卷/决策树/向导

| 工具 | 作用 |
|---|---|
| **Zingtree** / **VisiRule** | 商业决策树编辑器 |
| **blueorbitz/conf-decision-flow** | 开源决策流 |
| **decisionrules.io** | 规则引擎 SaaS |
| **问卷类: Typeform/Tally + Webhook** | 收集信息 → 触发方案生成 |

**🔍 判断**: 决策树/问卷已经成熟, 但「**问卷结果 → 方案输出**」这一段, 多数还是要靠人工。

### B.2 业界能做到什么程度（诚实总结）

| 能力 | 业界现状 | 备注 |
|---|---|---|
| 知识库 + 自由问答 | ✅ 完全做到 | Custom GPT / RAG |
| 决策树式问卷 | ✅ 完全做到 | Zingtree 等 |
| 问卷结果 → 结构化方案 | 🟡 部分做到 | 多跳决策质量不稳 |
| 自动生成架构图（带理由） | 🟡 实验性 | 需要大量规则 |
| 自动生成 ADR | 🟡 部分做到 | 多为草稿, 需人审 |
| 自动选型 + 理由 + 风险评估 | 🟡 实验性 | 需要决策规则 + LLM 协同 |
| 自动报价 | ❌ 基本做不到 | 太多业务上下文 |
| 端到端「喂信息 → 出可执行方案」 | ❓ 未找到成熟先例 | 这是真正的难题 |

**核心结论**: 「喂基础信息 → 出可执行方案」, 业界**还没人做到端到端**。能做到的最佳形态是「**知识库 + 决策问卷 + LLM 推理 + 结构化输出 + 人工 review**」。所以用户的目标是「超前但合理」, 但要分步走。

### B.3 落地路径设计: 4 步进化（从备忘录到决策辅助）

> 设计原则: 每步都要**独立可用** + **用户能立刻感到价值**, 不要做大爆炸式升级。

#### v1 · 结构化项目录入（1-2 周）

**目标**: 把「项目信息」从散落各处变成结构化卡片, 让网页能展示和检索。

**做什么**:
- 新增「📁 项目工作台」升级版, 项目记录字段化:
  - 客户: 谁、行业、规模、决策人
  - 业务: 要解决什么问题、关键指标、ROI 预期
  - 数据: 数据在哪、数据量、数据敏感度、合规要求
  - 规模: 用户数、并发、数据增长
  - 资源: 预算、时间、团队能力
  - 集成: 外部依赖、必须支持的系统
  - 运维: SLA、运维责任方
- 每条项目自动挂靠: 决策卡（ALT/STARTER/...）、方法论卡（FDE/AR/POC/...）、关卡地图（09 当前关卡）

**需要条件**: 字段 schema、录入 UI、Obsidian 端兼容（md frontmatter）。

**工作量**: 中（前端 3-5 天, schema 1 天, Obsidian 同步 1 天）。

**用户价值**: 中（项目可追溯、跨项目复用）。

#### v2 · 决策问卷（2-3 周）

**目标**: 「问 6-10 个关键问题 → 给出推荐方案」。

**做什么**:
- 在 Part A 的 A.3 判定法基础上, 把 6 步问题转成网页问卷（向导式, 一题一题）。
- 答案映射到零件清单（按维度组织）。
- 输出: 「你这个项目需要这些零件」+ 理由。
- 可选: 给出 ADR 草稿（标题/上下文/决策/后果）。

**需要条件**: 决策规则（yaml/json 写, 易维护）、前端向导组件、规则引擎（可简单 if-else）。

**工作量**: 中高（前端 4-5 天, 规则编写 2-3 天, 测试 2 天）。

**用户价值**: 高（用户拿到具体建议）。

#### v3 · LLM 增强（3-4 周）

**目标**: 接入 LLM API, 让推理更智能, 不再受限于硬编码规则。

**做什么**:
- 设计 Prompt: 「你是企业 AI 落地的资深架构师, 客户给了以下信息: [项目信息] + 问卷答案: [问卷结果]。请你输出:
  1. 推荐架构（前端 + 后端 + 数据 + 部署）
  2. 必装零件清单（按 9 维度）
  3. 推荐载体（SaaS/容器/嵌入）
  4. 选型理由
  5. 风险与缓解
  6. 报价参考
  请用结构化输出, 引用术语词典中的词条。 」
- 方法论 + 术语词典 + 决策卡 + 真实项目样板间 → RAG 喂给 LLM。
- 输出渲染: 结构化卡片, 可点开每个零件看详情（链回术语词典）。
- 用户可点「再生成」「调整偏好」「导出 ADR 草稿」。

**需要条件**: LLM API（OpenAI/Claude/本地 Ollama 都行）、Prompt 模板、RAG 索引、评测集（验证 LLM 输出质量）。

**工作量**: 高（前端 5-7 天, RAG 索引 2-3 天, Prompt 迭代 5-7 天, 评测 3-5 天）。

**用户价值**: 很高（从规则覆盖不到的问题也能给出建议）。

#### v4 · 持续闭环（持续）

**目标**: 让系统越用越准。

**做什么**:
- 用户反馈（采纳/驳回/修改）回流到黄金集（eval set）。
- 定期评测: 用 eval.py 验证输出质量。
- 沉淀新规则/新零件/新案例（飞轮）。
- 接入更多 LLM / 微调（如果量大）。

**需要条件**: 反馈 UI、黄金集 schema、自动化评测流水线、人力维护。

**工作量**: 持续投入。

**用户价值**: 长期资产。

### B.4 输入输出 Schema 草案

#### B.4.1 输入: 项目基础信息表（v1 schema, 后续可演进）

```yaml
# 项目基础信息（YAML 示例, 网页录入后转 JSON 存储）
project:
  id: "PRJ-2026-001"
  name: "某制造企业 AI 质检"
  stage: "POC"  # 需求/选型/POC/交付/运维
  
  customer:
    name: "某机械厂"
    industry: "制造"
    size: "200人"
    decision_maker: "CIO 王某"
  
  business:
    problem: "人工质检效率低, 漏检率高"
    success_metrics: ["漏检率 < 2%", "效率提升 50%"]
    roi_expectation: "12个月回本"
    criticality: "大"  # 零/小/大/灾难
  
  data:
    sources: ["现场摄像头"]
    volume: "20GB/天"
    sensitivity: "敏感"  # 无/PII/敏感/极敏感
    compliance: ["等保二级"]
  
  scale:
    users: 50
    concurrent: 20
    data_growth: "20GB/月"
  
  resources:
    budget: "30万"
    timeline: "3个月"
    team_capability: "客户运维能力弱, 我们负责运维"
  
  integrations:
    external: ["MES", "ERP"]
    ai_components: ["LLM", "CV模型"]
  
  ops:
    sla: "99.9%"
    ops_owner: "我们"
  
  meta:
    created: "2026-09-08"
    tags: ["AI", "制造", "POC"]
```

#### B.4.2 输出: 网页该给什么（v3 终极形态）

```json
{
  "architecture": {
    "frontend": "Next.js (理由: 多端嵌入) ",
    "backend": "FastAPI + Celery (理由: AI 生态丰富) ",
    "database": "PostgreSQL + pgvector (理由: 需要向量检索) ",
    "deployment": "Docker Compose → K8s 演进 (理由: POC 期简化) ",
    "carrier": "私有部署 (理由: 数据敏感 + 合规) "
  },
  "parts_checklist": {
    "reliability": ["重试", "幂等", "熔断", "健康检查"],
    "security": ["鉴权", "授权", "审计", "TLS", "加密存储"],
    "observability": ["结构化日志", "指标", "告警", "业务监控"],
    "ai_specific": ["Prompt 版本", "评测集", "幻觉治理", "成本监控"]
  },
  "rationale": [
    "因为 criticality=大 → 必装可靠性全套",
    "因为 sensitivity=敏感 → 必装加密 + 审计 + 私有部署",
    "因为含 LLM → 必装 AI 特有零件"
  ],
  "risks": [
    {"risk": "客户运维能力弱, 后续维护风险高", "mitigation": "提供运维手册 + 远程支持包"},
    {"risk": "数据敏感, 私有部署硬件成本", "mitigation": "考虑混合部署 + 数据脱敏"}
  ],
  "pricing_reference": {
    "build": "20-25万",
    "ops_yearly": "5-8万",
    "notes": "POC 期可砍一半"
  },
  "linked_assets": {
    "cards": ["FDE", "POC", "REL"],
    "decision_trees": ["Q1-载体决策"],
    "case_studies": ["Cal.com (SaaS)", "Dify (AI平台)"]
  }
}
```

### B.5 条件清单: 实现「喂信息→出方案」要具备哪些条件

> 用户原话: 「要实现这个需求应该具备什么条件?」 — 这里是诚实回答。

| 条件 | 现状（基于 `/tmp/growth_panel_structure_summary.md`） | 缺口 |
|---|---|---|
| 结构化知识库 | ✅ Obsidian + 决策卡 7 + 方法论卡 15 + 术语 197 | 🟡 字段未完全结构化, 部分是 markdown 段落, 需要 frontmatter 化 |
| 决策规则 | ❌ 缺 | 全缺, 需要写（v2 的核心） |
| LLM 接入 | ❌ 未接入 | 需要选 API + 写 Prompt + 部署 |
| Prompt 模板 | ❌ 缺 | 全缺 |
| 评测集 (Eval Set) | ✅ 黄金集 v0.1-v1.1 + eval.py（基础在, 但针对 AI 输出质量） | 🟡 需要扩到 LLM 输出评测 |
| 维护机制 | ✅ 飞轮: 候选池→学习池→复盘区 | 🟡 需要扩到「输出→反馈→规则/模板更新」 |
| 真实项目样板间 | ✅ c1 GitHub 方法论项目 58 个 + c3 抖音案例 | ✅ 有, 但需要做 Part A 那样的「零件级别解剖」 |
| 输入 schema | ✅ 有项目库 | 🟡 字段不够 v1 schema 那么完整 |
| 输出 schema | ❌ 缺 | 全缺 |
| ADR 模板 | ❌ 缺 | 全缺 |
| 用户反馈 UI | ❌ 缺 | 全缺 |
| 规则引擎 | ❌ 缺 | 可用简单 if-else 或选 json-rules-engine |
| RAG 索引 | ❌ 缺 | 全缺 |
| 词条-视频关联 | ✅ kb_links 110+ 词 | ✅ |

**总结: 现在具备 6 项, 缺 7 项**。最关键的 3 项: **决策规则 + LLM 接入 + 评测闭环**。

### B.6 推荐落地顺序（结合用户实际）

基于用户现状（小团队、本地网页 + Obsidian + GitHub Pages、AI 接单场景）, 推荐:

| 周次 | 任务 | 关键产出 | 价值点 |
|---|---|---|---|
| W1 | v1 项目信息结构化（字段化 + schema） | 项目录入 UI | 项目可追溯 |
| W2-W3 | v2 决策问卷（基于 Part A 判定法） | 「问 10 题出方案」 | 自动化初体验 |
| W4-W6 | v3 接 LLM, 加 Prompt 模板 | AI 增强推理 | 质量飞升 |
| W7+ | v4 闭环（反馈 + 评测 + 沉淀） | 飞轮启动 | 长期资产 |

**MVP 推荐**: 跳过 v1, 直接做 v2 (决策问卷) + 简化版 v3 (接 LLM 但 prompt 简单) — 因为决策问卷本身就有大价值, 不必等结构化完美。

---

## 综合验收与自我反思

### 数字盘点

- **Part A**: 9 大维度 ≈ 90+ 零件（其中 AI 特有 12 个, 合规 6 个, 传统工程 70+ 个）。
- **Part B**: 4 步落地路径（v1-v4）。
- **真实项目解剖**: 3 个（Cal.com, Supabase, Dify）。
- **业界工具调研**: 4 大类、15+ 个工具/项目。
- **条件清单**: 13 项（已具备 6 项, 缺 7 项）。

### 我认为网页还缺的 3 个盲区（超出 A/B 范围, 自行补充）

1. **客户旅程与决策点对齐**: 当前内容侧重「交付」, 但弱于「客户怎么从接触→签单→交付→续约→规模化的全旅程决策点」。建议加一个「客户旅程 × 决策点」矩阵。
2. **报价/成本数据库**: 缺一个「按场景/规模/复杂度」的报价参考库（类似 PRICING 数据集）, 让 LLM 输出的报价有依据, 不会瞎说。
3. **失败案例库与「不该做什么」**: 现在有「可复制打法」(r3), 但缺「公开失败的复盘」和「不该做的反模式」。建议加一个「反模式库」, 与决策卡联动。

### 诚实标注

- ❓ 「自动生成可执行架构方案」在公开资料中未找到强共识, 多数是 demo 级。
- 🟡 部分 LLM 推荐是基于训练数据而非实时, 需要评测闭环验证。
- ✅ 零件清单综合 AWS / Google / Microsoft / GitHub 头部项目, 共识度较高。
- 部分真实项目的零件清单基于公开文档推断, 不一定完整, 建议落地时再实地核实。

---

## 关键来源（汇总）

1. AWS Well-Architected Framework — 5 pillars (https://aws.amazon.com/architecture/well-architected/)
2. Microsoft Azure Well-Architected Framework — AI workloads (https://learn.microsoft.com/en-us/training/modules/adopt-ai-agent-best-practice/5-well-architected-framework)
3. Google SRE Workbook — Production Readiness Review
4. 12-Factor App Methodology — https://12factor.net
5. Manuel Blinkert AI Production Readiness Checklist — https://github.com/manuelblinkert/ai-production-readiness-checklist
6. asq-sheriff/AI-Production-Checklist — https://github.com/asq-sheriff/AI-Production-Checklist
7. Cal.com Architecture — https://github.com/calcom/cal.com ; https://cal.com/docs/developing/open-source-contribution/contributors-guide
8. Supabase Architecture — https://github.com/supabase/supabase ; https://supabase.com/docs/guides/auth/architecture
9. Dify Architecture — https://github.com/langgenius/dify ; https://docs.dify.ai
10. rag-architect-mcp (Part B 关键参考) — https://github.com/kevin801221/rag-architect-mcp
11. llm_advisory 框架 — https://github.com/happydasch/llm_advisory
12. ai-system-architect — https://github.com/sagarika29/ai-system-architect
13. agentic-runtime-platform — https://github.com/tafreeman/agentic-runtime-platform
14. ADR tools — https://github.com/endjin/dotnet-adr ; https://github.com/jossym17/architecture-toolkit
15. Scaffolding tools comparison — https://copier.readthedocs.io/en/v7.1.0/comparisons/
16. OWASP Top 10
17. VaidhyaMegha/technical-decision-framework — https://github.com/VaidhyaMegha/technical-decision-framework
18. Microsoft Azure Well-Architected — https://github.com/MicrosoftDocs/well-architected
19. 生产级 RAG 系统指南 — https://github.com/Yigtwxx/Awesome-RAG-Production
20. 已有结构总结: `/tmp/growth_panel_structure_summary.md`
